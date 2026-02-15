#!/usr/bin/env python3
"""Send new drozdi posts to Telegram when pushed."""

import json
import os
import re
import subprocess
import urllib.request
import uuid
from pathlib import Path

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
SITE_URL = os.environ.get("SITE_URL", "https://kumekay.com").rstrip("/")

TELEGRAM_TEXT_LIMIT = 4096
TELEGRAM_CAPTION_LIMIT = 1024


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
            # Skip the section index page
            if line == "content/drozdi/_index.md":
                continue
            files.append(line)
    return files


def parse_frontmatter(content):
    """Parse YAML frontmatter and return (metadata_dict, body)."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if not match:
        return {}, content

    frontmatter_str = match.group(1)
    body = match.group(2).strip()

    metadata = {}
    for line in frontmatter_str.splitlines():
        m = re.match(r'^(\w+)\s*:\s*"?(.*?)"?\s*$', line)
        if m:
            key, value = m.group(1), m.group(2)
            metadata[key] = value

    return metadata, body


def markdown_to_telegram_html(text):
    """Convert basic markdown to Telegram-compatible HTML."""
    # Escape HTML entities first (but preserve what we'll convert)
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")

    # Bold: **text** or __text__
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"__(.+?)__", r"<b>\1</b>", text)

    # Italic: *text* or _text_ (but not inside words with underscores)
    text = re.sub(r"(?<!\w)\*([^*]+?)\*(?!\w)", r"<i>\1</i>", text)
    text = re.sub(r"(?<!\w)_([^_]+?)_(?!\w)", r"<i>\1</i>", text)

    # Strikethrough: ~~text~~
    text = re.sub(r"~~(.+?)~~", r"<s>\1</s>", text)

    # Inline code: `text`
    text = re.sub(r"`([^`]+?)`", r"<code>\1</code>", text)

    # Links: [text](url)
    text = re.sub(r"\[([^\]]+?)\]\(([^)]+?)\)", r'<a href="\2">\1</a>', text)

    # Remove image references: ![alt](src)
    text = re.sub(r"!\[([^\]]*?)\]\([^)]+?\)", "", text)

    # Remove heading markers
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)

    # Clean up excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def truncate_html(html, limit):
    """Truncate HTML text to fit within a character limit, preserving tags."""
    if len(html) <= limit:
        return html
    # Leave room for an ellipsis
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
    message = f"<b>{title}</b>\n\n{body_html}\n\n{link_line}"
    return message


def build_multipart(fields, files):
    """Build multipart/form-data body and content-type header.

    fields: dict of {name: value}
    files: list of (field_name, filename, data, content_type)
    """
    boundary = uuid.uuid4().hex
    lines = []

    for key, value in fields.items():
        lines.append(f"--{boundary}".encode())
        lines.append(f'Content-Disposition: form-data; name="{key}"'.encode())
        lines.append(b"")
        lines.append(value.encode() if isinstance(value, str) else value)

    for field_name, filename, data, content_type in files:
        lines.append(f"--{boundary}".encode())
        lines.append(
            f'Content-Disposition: form-data; name="{field_name}"; '
            f'filename="{filename}"'.encode()
        )
        lines.append(f"Content-Type: {content_type}".encode())
        lines.append(b"")
        lines.append(data)

    lines.append(f"--{boundary}--".encode())
    lines.append(b"")

    body = b"\r\n".join(lines)
    content_type = f"multipart/form-data; boundary={boundary}"
    return body, content_type


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


def telegram_send_photo(photo_path, caption=""):
    """Send a photo with optional caption via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"

    with open(photo_path, "rb") as f:
        photo_data = f.read()

    filename = os.path.basename(photo_path)
    ext = os.path.splitext(filename)[1].lower()
    content_type_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    ct = content_type_map.get(ext, "image/jpeg")

    fields = {
        "chat_id": TELEGRAM_CHAT_ID,
        "parse_mode": "HTML",
    }
    if caption:
        fields["caption"] = caption

    body, content_type = build_multipart(fields, [("photo", filename, photo_data, ct)])

    req = urllib.request.Request(url, data=body, headers={"Content-Type": content_type})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def find_image_in_bundle(bundle_dir):
    """Find an image file in the post bundle directory."""
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    bundle_path = Path(bundle_dir)
    if not bundle_path.exists():
        return None

    for f in sorted(bundle_path.iterdir()):
        if f.suffix.lower() in image_extensions:
            return str(f)
    return None


def process_post(filepath):
    """Process a single post file and send it to Telegram."""
    path = Path(filepath)
    if not path.exists():
        print(f"File not found (possibly deleted): {filepath}")
        return

    content = path.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(content)

    title = metadata.get("title", path.parent.name)
    # Slug from directory name
    slug = path.parent.name

    post_url = f"{SITE_URL}/drozdi/{slug}/"
    body_html = markdown_to_telegram_html(body)
    full_message = format_message(title, body_html, post_url)

    bundle_dir = str(path.parent)

    # Check for image from frontmatter or scan directory
    image_path = None
    if metadata.get("image"):
        candidate = os.path.join(bundle_dir, metadata["image"])
        if os.path.exists(candidate):
            image_path = candidate
    if not image_path:
        image_path = find_image_in_bundle(bundle_dir)

    if image_path:
        # Try to send photo with caption
        if len(full_message) <= TELEGRAM_CAPTION_LIMIT:
            telegram_send_photo(image_path, caption=full_message)
            print(f"Sent photo with caption for: {title}")
        else:
            # Caption too long: send photo with short caption, then full text
            short_caption = f"<b>{title}</b>"
            telegram_send_photo(image_path, caption=short_caption)

            # Send full text as follow-up
            text = truncate_html(full_message, TELEGRAM_TEXT_LIMIT)
            telegram_send_message(text)
            print(f"Sent photo + follow-up text for: {title}")
    else:
        # No image, send text only
        text = truncate_html(full_message, TELEGRAM_TEXT_LIMIT)
        telegram_send_message(text)
        print(f"Sent text message for: {title}")


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
