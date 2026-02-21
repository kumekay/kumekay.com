#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-frontmatter",
# ]
# ///
"""Send new drozdi posts to Telegram when pushed.

Run with: uv run scripts/telegram_notify.py
"""

import json
import os
import re
import subprocess
import urllib.request
from pathlib import Path

import frontmatter

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
SITE_URL = os.environ.get("SITE_URL", "https://kumekay.com").rstrip("/")

TELEGRAM_TEXT_LIMIT = 4096


def get_changed_drozdi_files():
    """Find markdown files changed under content/drozdi/ in the last commit."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        capture_output=True,
        text=True,
    )
    files = []
    for line in result.stdout.strip().splitlines():
        if line.startswith("content/drozdi/") and line.endswith(".md"):
            if line == "content/drozdi/_index.md":
                continue
            files.append(line)
    return files


def parse_frontmatter(content):
    """Parse YAML frontmatter and return (metadata_dict, body).

    Uses python-frontmatter for robust YAML parsing (handles lists,
    booleans, nested values, etc.).
    """
    post = frontmatter.loads(content)
    return dict(post.metadata), post.content


def markdown_to_telegram_html(text):
    """Convert basic markdown to Telegram-compatible HTML."""
    # Remove image references first (before link conversion)
    text = re.sub(r"!\[([^\]]*?)\]\([^)]+?\)", "", text)

    # Escape HTML entities
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")

    # Bold: **text** or __text__
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"__(.+?)__", r"<b>\1</b>", text)

    # Italic: *text* or _text_
    text = re.sub(r"(?<!\w)\*([^*]+?)\*(?!\w)", r"<i>\1</i>", text)
    text = re.sub(r"(?<!\w)_([^_]+?)_(?!\w)", r"<i>\1</i>", text)

    # Strikethrough: ~~text~~
    text = re.sub(r"~~(.+?)~~", r"<s>\1</s>", text)

    # Inline code: `text`
    text = re.sub(r"`([^`]+?)`", r"<code>\1</code>", text)

    # Links: [text](url)
    text = re.sub(r"\[([^\]]+?)\]\(([^)]+?)\)", r'<a href="\2">\1</a>', text)

    # Remove heading markers
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)

    # Clean up excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def truncate_html(html, limit):
    """Truncate HTML text to fit within a character limit, preserving tags."""
    if len(html) <= limit:
        return html
    truncated = html[: limit - 3]
    # Close any open tags naively by removing the last partial tag
    last_open = truncated.rfind("<")
    last_close = truncated.rfind(">")
    if last_open > last_close:
        truncated = truncated[:last_open]
    return truncated.rstrip() + "..."


def format_message(title, body_html, post_url):
    """Format the full Telegram message."""
    link_line = f'<a href="{post_url}">Читать на kumekay.com</a>'
    return f"<b>{title}</b>\n\n{body_html}\n\n{link_line}"


def telegram_send_message(text):
    """Send a text message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = json.dumps(
        {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
        }
    ).encode()

    req = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def process_post(filepath):
    """Process a single post file and send it to Telegram."""
    path = Path(filepath)
    if not path.exists():
        print(f"File not found (possibly deleted): {filepath}")
        return

    content = path.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(content)

    title = metadata.get("title", path.parent.name)
    slug = path.parent.name
    post_url = f"{SITE_URL}/drozdi/{slug}/"

    body_html = markdown_to_telegram_html(body)
    full_message = format_message(title, body_html, post_url)

    text = truncate_html(full_message, TELEGRAM_TEXT_LIMIT)
    telegram_send_message(text)
    print(f"Sent message for: {title}")


def main():
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set")
        return

    changed_files = get_changed_drozdi_files()
    if not changed_files:
        print("No drozdi posts changed in this commit.")
        return

    print(f"Found {len(changed_files)} changed drozdi file(s):")
    for f in changed_files:
        print(f"  - {f}")

    for filepath in changed_files:
        process_post(filepath)


if __name__ == "__main__":
    main()
