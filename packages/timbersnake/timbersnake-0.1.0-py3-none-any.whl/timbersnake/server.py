import asyncio
import json
import logging
import ssl
import struct
import zlib

LOG = logging.getLogger("timbersnake")


class Server:
    def __init__(self, endpoint, port, ssl=None, version=b"2"):
        self.endpoint = endpoint
        self.port = port
        self.ssl = ssl
        self.version = version

        self.frame_type_coros = {
            b"W": self.window_frame,
            b"C": self.compressed_frame,
        }

        if version == b"2":
            self.frame_type_coros[b"J"] = self.json_frame
        elif version == b"1":
            self.frame_type_coros[b"D"] = self.data_frame
        else:
            raise ValueError(f'Invalid version {version}. Must be b"1" or b"2"')

        self.frame_type_funcs_str = {
            "W": self.window_frame_str
            # NOTE Nested compressed frames can technically happen per the spec. :v)
            # 'C': compressed_frame_str
        }

        if version == b"2":
            self.frame_type_funcs_str["J"] = self.json_frame_str
        elif version == b"1":
            self.frame_type_funcs_str["D"] = self.data_frame_str
        else:
            raise ValueError(f'Invalid version {version}. Must be b"1" or b"2"')

        print(self.frame_type_funcs_str)

    async def start_and_serve_forever(self):
        serv = await asyncio.start_server(
            self.handle_client_callback, self.endpoint, self.port, ssl=self.ssl
        )
        async with serv:
            await serv.serve_forever()

    async def send_ack_frame(self, writer, sequence_num):
        frame_type = b"A"
        frame = struct.pack("!ccI", self.version, frame_type, sequence_num)

        writer.write(frame)
        await writer.drain()

    async def window_frame(self, reader, writer):
        # TODO We don't do anything with window frames yet. They can be used for
        # bulk window acks, see how EA/LS uses them
        window_size_data = await reader.readexactly(4)
        window_size = struct.unpack("!I", window_size_data)

        LOG.debug("recv WINDOW: %i", window_size)

    def window_frame_str(self, s, pos=0):
        # NOTE As above, we don't use window sizes for anything yet.
        # window_size_data = s[pos:pos+4]
        pos += 4
        # window_size = struct.unpack("!I", window_size_data)

        return pos, None

    async def json_frame(self, reader, writer):
        header_data = await reader.readexactly(8)
        sequence_num, size = struct.unpack("!II", header_data)

        json_data = await reader.readexactly(size)
        event = json.parse(json_data)

        LOG.debug("recv JSON: %s", event)

        await self.send_ack_frame(writer, sequence_num)

    def json_frame_str(self, s, pos=0):
        header_data = s[pos : pos + 8]
        pos += 8
        sequence_num, size = struct.unpack("!II", header_data)

        json_data = s[pos : pos + size]
        pos += size
        event = json.loads(json_data)

        LOG.debug("recv JSON: %s", event)

        return pos, sequence_num

    async def data_frame(self, reader, writer):
        header_data = await reader.readexactly(8)
        LOG.debug("data_frame header: %s", header_data)
        sequence_num, pair_count = struct.unpack("!II", header_data)

        event = {}
        for _ in range(pair_count):
            key_size_data = await reader.readexactly(4)
            key_size = struct.unpack("!I", key_size_data)[0]
            key_data = await reader.readexactly(key_size)
            key = key_data.decode()

            val_size_data = await reader.readexactly(4)
            val_size = struct.unpack("!I", val_size_data)[0]
            val_data = await reader.readexactly(val_size)
            val = val_data.decode()

            event[key] = val

        LOG.debug("recv DATA: %s", event)

        await self.send_ack_frame(writer, sequence_num)

    def data_frame_str(self, s, pos=0):
        header_data = s[pos : pos + 8]
        pos += 8
        sequence_num, pair_count = struct.unpack("!II", header_data)

        event = {}
        for _ in range(pair_count):
            key_size_data = s[pos : pos + 4]
            pos += 4
            key_size = struct.unpack("!I", key_size_data)[0]
            key_data = s[pos : pos + key_size]
            pos += key_size
            key = key_data.decode()

            val_size_data = s[pos : pos + 4]
            pos += 4
            val_size = struct.unpack("!I", val_size_data)[0]
            val_data = s[pos : pos + val_size]
            pos += key_size
            val = val_data.decode()

            event[key] = val

        LOG.debug("recv DATA: %s", event)

        return pos, sequence_num

    async def compressed_frame(self, reader, writer):
        size_data = await reader.readexactly(4)
        size = struct.unpack("!I", size_data)[0]

        compressed_data = await reader.readexactly(size)
        payload = zlib.decompress(compressed_data)

        LOG.debug("recv COMPRESSED: %s", payload)

        pos = 0
        payload_len = len(payload)
        sequence_num = 0
        while pos < payload_len:
            version = chr(payload[pos])
            frame_type = chr(payload[pos + 1])
            pos += 2

            LOG.debug(
                "In compressed frame, got frame version %s, frame type %s", version, frame_type
            )

            try:
                frame_fn = self.frame_type_funcs_str[frame_type]
            except KeyError:
                # TODO How does LS handle invalid frame types? Spec doesn't specify
                LOG.warning("In compressed frame, invalid frame type %s from peer", frame_type)
                LOG.debug("Valid frame types: %s", self.frame_type_funcs_str.keys())
                return
            else:
                pos, sequence_num = frame_fn(payload, pos)

        await self.send_ack_frame(writer, sequence_num)

    async def _handle_client_callback(self, reader, writer):
        while True:
            header_data = await reader.readexactly(2)
            # TODO validate client version. How does LS say that client has wrong ver?
            version, frame_type = struct.unpack("!cc", header_data)
            LOG.debug(
                "In main client loop, got frame version %s, frame type %s", version, frame_type
            )

            try:
                frame_coro = self.frame_type_coros[frame_type]
            except KeyError:
                LOG.warning("Invalid frame type %s from peer", frame_type)
                LOG.debug("Valid frame types: %s", self.frame_type_coros.keys())
                break
            else:
                await frame_coro(reader, writer)

    async def handle_client_callback(self, reader, writer):
        try:
            await self._handle_client_callback(reader, writer)
        except asyncio.IncompleteReadError:
            LOG.info("Client disconnected")
        finally:
            writer.close()
            await writer.wait_closed()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    async def main():
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain("./localhost.crt", "./localhost.key")

        server = Server("127.0.0.1", 1337, ssl=ssl_context)

        print(f"Serving on ({server.endpoint},{server.port})")
        await server.start_and_serve_forever()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped server")
