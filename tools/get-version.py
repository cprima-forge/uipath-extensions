#!/usr/bin/env python3
"""
get-version.py

Reads the version from pyproject.toml and outputs it.

Usage:
    python ./tools/get-version.py
"""

import sys
import tomllib
from pathlib import Path


def get_version() -> str:
    """Read version from pyproject.toml"""
    root = Path(__file__).resolve().parents[1]
    pyproject_path = root / "pyproject.toml"

    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    return data["project"]["version"]


if __name__ == "__main__":
    try:
        print(get_version())
    except Exception as e:
        print(f"Error reading version: {e}", file=sys.stderr)
        sys.exit(1)
