#!/usr/bin/env python3
"""
clean-md-separators.py

Removes markdown separator blocks consisting of a single '---'
surrounded by blank lines in all *.md files under the repository tree.

Usage:
    python ./tools/clean-md-separators.py
"""

import pathlib
import re

# Match: two or more newlines, then optional spaces, then '---', then optional spaces, then two or more newlines
SEPARATOR_PATTERN = re.compile(r"\n\s*\n\s*---\s*\n\s*\n", flags=re.MULTILINE)

def clean_file(path: pathlib.Path) -> bool:
    """Replace matching separators in a single markdown file."""
    text = path.read_text(encoding="utf-8")
    new_text = SEPARATOR_PATTERN.sub("\n\n", text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False

def main():
    root = pathlib.Path(__file__).resolve().parents[1]
    md_files = list(root.rglob("*.md"))
    modified = 0

    for md in md_files:
        if clean_file(md):
            modified += 1
            print(f"cleaned: {md.relative_to(root)}")

    print(f"\n{modified} file(s) cleaned." if modified else "\nNo changes needed.")

if __name__ == "__main__":
    main()
