#!/usr/bin/env python3
"""Create a new article in the specified section.

Usage:
    uv run scripts/new_post.py "My Article Title" --section drozdi --date 2026-02-24
    uv run scripts/new_post.py "New Tool" -s utoolek
"""

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

SECTION_MAP = {
    "blog": "posts",
    "posts": "posts",
    "utoolek": "utoolek",
    "drozdi": "drozdi",
}


def title_to_slug(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def main():
    parser = argparse.ArgumentParser(description="Create a new article")
    parser.add_argument("title", help="Article title")
    parser.add_argument(
        "-s",
        "--section",
        choices=["blog", "utoolek", "drozdi"],
        default="drozdi",
        help="Section to create post in (default: drozdi)",
    )
    parser.add_argument(
        "-d",
        "--date",
        type=lambda x: date.fromisoformat(x),
        default=date.today(),
        help="Post date (YYYY-MM-DD, default: today)",
    )
    args = parser.parse_args()

    content_dir = SECTION_MAP[args.section]
    slug = title_to_slug(args.title)
    date_str = args.date.isoformat()

    path = f"{content_dir}/{date_str}-{slug}/index.md"

    result = subprocess.run(
        ["hugo", "new", "content", path],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    created_path = Path("content") / path
    content = created_path.read_text()
    content = re.sub(
        r'^title: ".*"$', f'title: "{args.title}"', content, flags=re.MULTILINE
    )
    content = re.sub(r'^slug: ".*"$', f'slug: "{slug}"', content, flags=re.MULTILINE)
    created_path.write_text(content)
    print(created_path)


if __name__ == "__main__":
    main()
