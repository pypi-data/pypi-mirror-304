import asyncio
import json
import logging
import ssl
import struct
import zlib

LOG = logging.getLogger("timbersnake")

FRAME_TYPE_COROS = {
    b"W": lambda reader, writer: window_frame(reader, writer),
    b"D": lambda reader, writer: data_frame(reader, writer),
    b"J": lambda reader, writer: json_frame(reader, writer),
    b"C": lambda reader, writer: compressed_frame(reader, writer),
}

FRAME_TYPE_FUNCS_STR = {
    "W": lambda s, pos: window_frame_str(s, pos),
    "D": lambda s, pos: data_frame_str(s, pos),
    "J": lambda s, pos: json_frame_str(s, pos),
    # NOTE Nested compressed frames can technically happen per the spec. In
    # practice, lmao.
    # b'C': lambda s, pos: compressed_frame_str(s, pos),
}

VERSION = b"2"


async def send_ack_frame(writer, sequence_num):
    frame_type = b"A"
    frame = struct.pack("!ccI", VERSION, frame_type, sequence_num)

    writer.write(frame)
    await writer.drain()


async def window_frame(reader, writer):
    # TODO We don't do anything with window frames yet. They can be used for
    # bulk window acks, see how EA/LS uses them
    window_size_data = await reader.readexactly(4)
    window_size = struct.unpack("!I", window_size_data)

    print(f"recv WINDOW: {window_size}")


def window_frame_str(s, pos=0):
    # NOTE As above, we don't use window sizes for anything yet.
    # window_size_data = s[pos:pos+4]
    pos += 4
    # window_size = struct.unpack("!I", window_size_data)

    return pos, None


async def json_frame(reader, writer):
    header_data = await reader.readexactly(8)
    sequence_num, size = struct.unpack("!II", header_data)

    json_data = await reader.readexactly(size)
    event = json.parse(json_data)

    LOG.debug("recv JSON: %s", event)

    await send_ack_frame(writer, sequence_num)


def json_frame_str(s, pos=0):
    header_data = s[pos : pos + 8]
    pos += 8
    sequence_num, size = struct.unpack("!II", header_data)

    json_data = s[pos : pos + size]
    pos += size
    event = json.loads(json_data)

    LOG.debug("recv JSON: %s", event)

    return pos, sequence_num


async def data_frame(reader, writer):
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

    await send_ack_frame(writer, sequence_num)


def data_frame_str(s, pos=0):
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


async def compressed_frame(reader, writer):
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

        LOG.debug("In compressed frame, got frame version %s, frame type %s", version, frame_type)

        try:
            frame_fn = FRAME_TYPE_FUNCS_STR[frame_type]
        except KeyError:
            # TODO Handle error better
            LOG.debug("Invalid frame type %s from peer", frame_type)
            break
        else:
            pos, sequence_num = frame_fn(payload, pos)

    await send_ack_frame(writer, sequence_num)


async def _handle_client_callback(reader, writer):
    while True:
        header_data = await reader.readexactly(2)
        # TODO filebeat 8.15 uses the character '2' to denote version. Do ver 1 versions?
        version, frame_type = struct.unpack("!cc", header_data)
        LOG.debug("In main client loop, got frame version %s, frame type %s", version, frame_type)

        try:
            frame_coro = FRAME_TYPE_COROS[frame_type]
        except KeyError:
            LOG.debug("Invalid frame type %s from peer", frame_type)
        else:
            await frame_coro(reader, writer)


async def handle_client_callback(reader, writer):
    try:
        await _handle_client_callback(reader, writer)
    except asyncio.IncompleteReadError:
        LOG.info("Client disconnected")
        print(reader)
        print(reader.__dict__)
    finally:
        writer.close()
        await writer.wait_closed()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    async def main():
        endpoint = "127.0.0.1"
        port = 1337
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain("./localhost.crt", "./localhost.key")

        server = await asyncio.start_server(handle_client_callback, endpoint, port, ssl=ssl_context)
        print(f"Serving on ({endpoint},{port})")
        async with server:
            await server.serve_forever()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped server")
