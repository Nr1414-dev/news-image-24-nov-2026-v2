#!/usr/bin/env python3
"""Entry program for news-image-20261124 (Python 3.13, stdlib only).

Copies the pre-drawn entry.png beside this file to the output
directory, as /output/entry.png. Outside the grader's container,
MAKEFUN_OUTPUT_DIR stands in for /output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", OUT / "entry.png")
