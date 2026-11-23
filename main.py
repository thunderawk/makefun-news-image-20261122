#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261122.

Writes the pre-rendered front-page image (entry.png, in this repo) to
/output/entry.png. Stdlib only, no network, deterministic. Verifies the
source is a real PNG (magic bytes) and prints its sha256 before copying.
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    src = os.path.join(HERE, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    if data[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG (bad magic bytes)")
    print("entry.png sha256=%s (%d bytes)"
          % (hashlib.sha256(data).hexdigest(), len(data)))
    os.makedirs(OUT, exist_ok=True)
    shutil.copyfile(src, os.path.join(OUT, "entry.png"))


if __name__ == "__main__":
    main()
