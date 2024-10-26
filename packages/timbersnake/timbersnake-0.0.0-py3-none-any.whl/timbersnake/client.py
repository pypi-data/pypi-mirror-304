import asyncio
import json
import ssl
import struct
import zlib


class Client:
    def __init__(self, endpoint, port, version=b"2", compression_level=-1, ssl=None):
        if version == b"2":
            self.pack_data_frame_fn = self.pack_json_data_frame
        elif version == b"1":
            self.pack_data_frame_fn = self.pack_data_frame
        else:
            raise ValueError(f"version must be one of b'1' or b'2'. Got {version}")
        self.version = version

        if type(compression_level) is not int or compression_level < -1 or compression_level > 9:
            raise ValueError(
                f"compression_level must be an integer between -1 and 9 inclusive. Got {compression_level}."
            )
        self.compression_level = compression_level

        self.endpoint = endpoint
        self.port = port
        self.ssl = ssl

    async def send(self, it):
        # TODO should reader and writer exist for longer than send()?
        # If so then we should implement a TTL or similar, I hate long running
        # network implementations that don't let go of sockets gracefully.
        self.reader, self.writer = await asyncio.open_connection(
            self.endpoint, self.port, ssl=self.ssl
        )
        sequence_num = 0

        # NOTE LS won't use our data unless we put a windowframe in the same
        # packet as the C frame. This isn't mentioned in the protocol docs.
        # TODO Actually set and use our window size
        buffer = self.pack_window_frame(3)
        # TODO window size for batch numbers
        # We should assume iterable can be infinite and still send sensibly
        for event in it:
            data = self.pack_data_frame_fn(event, sequence_num)
            sequence_num += 1
            buffer += data

        if self.compression_level == 0:
            await self._send(buffer)
        else:
            await self._send(self.pack_compressed_frame(buffer))

        # TODO optional ack
        ack_data = await self.reader.readexactly(6)
        print(f"got ack: {ack_data!r}")

        self.writer.close()
        await self.writer.wait_closed()

    async def _send(self, data):
        self.writer.write(data)
        await self.writer.drain()

    def pack_window_frame(self, window_size):
        return struct.pack("!ccI", self.version, b"W", window_size)

    def pack_compressed_frame(self, data):
        compressed_data = zlib.compress(data, level=self.compression_level)
        size = len(compressed_data)
        return struct.pack("!ccI", self.version, b"C", size) + compressed_data

    def pack_json_data_frame(self, event, sequence_num):
        data = json.dumps(event).encode()
        size = len(data)
        return struct.pack("!ccII", self.version, b"J", sequence_num, size) + data

    def pack_data_frame(self, event, sequence_num):
        raise NotImplementedError()


if __name__ == "__main__":

    async def main():
        endpoint = "127.0.0.1"
        port = 1337
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.load_verify_locations("./localhost.crt")

        client = Client(endpoint, port, ssl=ssl_context)
        events = [{"test": 1}, {"test": 2}, {"not a test": 3}]
        await client.send(events)

    asyncio.run(main())
