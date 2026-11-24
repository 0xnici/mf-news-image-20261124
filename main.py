#!/usr/bin/env python3
"""Stdlib-only grader entrypoint.

The PNG is rendered ahead of time and committed beside this file. At runtime
we only validate those bytes and copy them into the output directory. No
network, no Pillow, no subprocess, and /output is never removed.
"""
import hashlib
import os
import pathlib
import struct
import sys
import tempfile

EXPECTED_SHA256 = "ab5e4ccde4921dc1ce9bbccb2e48989ea2f4416c3104df7b6ee104597d7d2e00"
MAX_BYTES = 1048576
WIDTH = 1024
HEIGHT = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
IHDR_TYPE = b"IHDR"
IDAT_TYPE = b"IDAT"
IEND_TYPE = b"IEND"
IHDR_LENGTH = 13
EXPECTED_BIT_DEPTH = 8
EXPECTED_COLOR_TYPE = 2  # truecolour RGB, as written by the renderer


def fail(message):
    print("main.py: " + message, file=sys.stderr)
    raise SystemExit(1)


def crc32(payload):
    """Pure-Python CRC-32 so the runtime needs no extra imports."""
    crc = 0xFFFFFFFF
    for byte in payload:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ (0xEDB88320 if crc & 1 else 0)
    return crc ^ 0xFFFFFFFF


def check_chunks(data):
    """Walk every chunk to IEND, checking declared length and stored CRC."""
    offset = 8
    seen_idat = False
    while offset + 12 <= len(data):
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        end = offset + 12 + length
        if end > len(data):
            fail("truncated PNG chunk %r" % kind)
        payload = data[offset + 8:offset + 8 + length]
        stored = struct.unpack(">I", data[offset + 8 + length:end])[0]
        if crc32(kind + payload) != stored:
            fail("bad CRC in PNG chunk %r" % kind)
        if kind == IDAT_TYPE:
            seen_idat = True
        offset = end
        if kind == IEND_TYPE:
            if offset != len(data):
                fail("trailing bytes after IEND chunk")
            if not seen_idat:
                fail("PNG has no IDAT chunk, so it holds no image data")
            return
    fail("PNG has no IEND chunk; the image is incomplete")


def validate(data):
    if len(data) > MAX_BYTES:
        fail("entry.png is larger than 1048576 bytes")
    if not data.startswith(PNG_SIGNATURE):
        fail("entry.png has no PNG signature")
    if len(data) < 33 or data[12:16] != IHDR_TYPE:
        fail("entry.png has no IHDR chunk")
    ihdr_length = struct.unpack(">I", data[8:12])[0]
    if ihdr_length != IHDR_LENGTH:
        fail("entry.png has an invalid IHDR length: %d" % ihdr_length)
    if data[24] != EXPECTED_BIT_DEPTH or data[25] != EXPECTED_COLOR_TYPE:
        fail("entry.png must be 8-bit RGB, got depth %d colour %d"
             % (data[24], data[25]))
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (WIDTH, HEIGHT):
        fail("entry.png must be 1024x1024, got %dx%d" % (width, height))
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        fail("entry.png SHA-256 mismatch: " + digest)
    check_chunks(data)


def write_output(data):
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    destination = pathlib.Path(out_dir) / "entry.png"
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=out_dir, prefix=".entry-", suffix=".png", delete=False
        ) as handle:
            temporary = handle.name
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
        temporary = None
    finally:
        if temporary is not None and os.path.exists(temporary):
            os.unlink(temporary)
    with open(destination, "rb") as handle:
        written = handle.read()
    if written != data or hashlib.sha256(written).hexdigest() != EXPECTED_SHA256:
        fail("output is not byte-identical to entry.png")


def main():
    source = pathlib.Path(__file__).resolve().parent / "entry.png"
    try:
        data = source.read_bytes()
    except OSError as error:
        print("main.py: cannot read entry.png: %s" % error, file=sys.stderr)
        raise SystemExit(1)
    validate(data)
    write_output(data)
    print("wrote %d bytes to entry.png" % len(data))


if __name__ == "__main__":
    main()
