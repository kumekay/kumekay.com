# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pytest",
#     "python-frontmatter",
# ]
# ///
"""Tests for telegram_notify.py - TDD approach.

Run with: uv run pytest scripts/test_telegram_notify.py -v
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch


from telegram_notify import (
    format_message,
    get_changed_drozdi_files,
    markdown_to_telegram_html,
    parse_frontmatter,
    process_post,
    telegram_send_message,
    truncate_html,
)


# --- parse_frontmatter tests ---


class TestParseFrontmatter:
    """Tests for parse_frontmatter using python-frontmatter library.

    PR review comment: regex parser can't handle list values like tags: ["meta"].
    """

    def test_simple_frontmatter(self):
        content = '---\ntitle: "Hello World"\ndate: 2026-01-01\n---\nBody text here.'
        metadata, body = parse_frontmatter(content)
        assert metadata["title"] == "Hello World"
        assert body == "Body text here."

    def test_frontmatter_with_list_tags(self):
        """PR comment: regex parser can't handle list values like tags: ["meta"]."""
        content = '---\ntitle: "Test"\ntags: ["meta", "test"]\n---\nBody.'
        metadata, body = parse_frontmatter(content)
        assert metadata["tags"] == ["meta", "test"]

    def test_frontmatter_with_yaml_list_syntax(self):
        content = "---\ntitle: Test\ntags:\n  - one\n  - two\n---\nBody."
        metadata, body = parse_frontmatter(content)
        assert metadata["tags"] == ["one", "two"]

    def test_frontmatter_with_boolean_values(self):
        content = "---\ntitle: Test\ndraft: false\n---\nBody."
        metadata, body = parse_frontmatter(content)
        assert metadata["draft"] is False

    def test_no_frontmatter(self):
        content = "Just some text without frontmatter."
        metadata, body = parse_frontmatter(content)
        assert metadata == {}
        assert body == "Just some text without frontmatter."

    def test_empty_body(self):
        content = "---\ntitle: Test\n---\n"
        metadata, body = parse_frontmatter(content)
        assert metadata["title"] == "Test"
        assert body == ""

    def test_frontmatter_with_nested_values(self):
        """Regex parser would fail on nested YAML."""
        content = '---\ntitle: "Post"\nauthor:\n  name: "Alice"\n  email: "a@b.com"\n---\nBody.'
        metadata, body = parse_frontmatter(content)
        assert metadata["author"]["name"] == "Alice"
        assert metadata["author"]["email"] == "a@b.com"

    def test_frontmatter_with_quoted_colons(self):
        content = '---\ntitle: "Hello: World"\n---\nBody.'
        metadata, body = parse_frontmatter(content)
        assert metadata["title"] == "Hello: World"

    def test_multiline_body(self):
        content = "---\ntitle: Test\n---\nLine 1.\n\nLine 2.\n\nLine 3."
        metadata, body = parse_frontmatter(content)
        assert "Line 1." in body
        assert "Line 3." in body

    def test_russian_content(self):
        """Drozdi section uses Russian text."""
        content = '---\ntitle: "Первый пост"\ntags: ["мета"]\n---\nТекст на русском.'
        metadata, body = parse_frontmatter(content)
        assert metadata["title"] == "Первый пост"
        assert metadata["tags"] == ["мета"]
        assert body == "Текст на русском."

    def test_image_field(self):
        content = '---\ntitle: Test\nimage: "feature.jpg"\n---\nBody.'
        metadata, body = parse_frontmatter(content)
        assert metadata["image"] == "feature.jpg"


# --- markdown_to_telegram_html tests ---


class TestMarkdownToTelegramHtml:
    def test_bold_asterisks(self):
        assert "<b>bold</b>" in markdown_to_telegram_html("**bold**")

    def test_bold_underscores(self):
        assert "<b>bold</b>" in markdown_to_telegram_html("__bold__")

    def test_italic_asterisk(self):
        assert "<i>italic</i>" in markdown_to_telegram_html("*italic*")

    def test_italic_underscore(self):
        assert "<i>italic</i>" in markdown_to_telegram_html("_italic_")

    def test_strikethrough(self):
        assert "<s>struck</s>" in markdown_to_telegram_html("~~struck~~")

    def test_inline_code(self):
        assert "<code>code</code>" in markdown_to_telegram_html("`code`")

    def test_link(self):
        result = markdown_to_telegram_html("[click](https://example.com)")
        assert '<a href="https://example.com">click</a>' in result

    def test_image_removal(self):
        result = markdown_to_telegram_html("![alt text](image.png)")
        assert "alt text" not in result
        assert "image.png" not in result

    def test_heading_removal(self):
        result = markdown_to_telegram_html("## Heading")
        assert result == "Heading"

    def test_html_escaping(self):
        result = markdown_to_telegram_html("a < b & c > d")
        assert "&lt;" in result
        assert "&amp;" in result
        assert "&gt;" in result

    def test_excessive_newlines_collapsed(self):
        result = markdown_to_telegram_html("a\n\n\n\n\nb")
        assert "\n\n\n" not in result


# --- truncate_html tests ---


class TestTruncateHtml:
    def test_short_text_unchanged(self):
        assert truncate_html("hello", 100) == "hello"

    def test_long_text_truncated(self):
        text = "a" * 200
        result = truncate_html(text, 100)
        assert len(result) <= 100
        assert result.endswith("...")

    def test_partial_tag_removed(self):
        text = "hello <b>world" + "d" * 200
        result = truncate_html(text, 20)
        # Should not end with a partial tag
        assert "<b" not in result or ">" in result[result.rfind("<") :]


# --- format_message tests ---


class TestFormatMessage:
    def test_format_includes_title_and_link(self):
        msg = format_message("Title", "body html", "https://kumekay.com/drozdi/test/")
        assert "Title" in msg
        assert "https://kumekay.com/drozdi/test/" in msg

    def test_format_includes_body(self):
        msg = format_message("T", "some body", "https://example.com")
        assert "some body" in msg

    def test_format_structure(self):
        url = "https://kumekay.com/drozdi/test/"
        msg = format_message("Title", "body", url)
        assert msg == "Title\n\nhttps://kumekay.com/drozdi/test/\n\nbody"


# --- telegram_send_message tests ---


class TestTelegramSendMessage:
    """Test that telegram_send_message sends correct payload."""

    @patch("telegram_notify.urllib.request.urlopen")
    @patch("telegram_notify.urllib.request.Request")
    def test_sends_html_message(self, mock_request_cls, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.read.return_value = b'{"ok": true}'
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        with patch.dict(
            "os.environ",
            {"TELEGRAM_BOT_TOKEN": "test-token", "TELEGRAM_CHAT_ID": "123"},
        ):
            # Re-import to pick up env vars (module-level constants)
            import telegram_notify

            telegram_notify.TELEGRAM_BOT_TOKEN = "test-token"
            telegram_notify.TELEGRAM_CHAT_ID = "123"
            telegram_send_message("<b>Hello</b>")

        # Verify the Request was constructed correctly
        call_args = mock_request_cls.call_args
        url = call_args[0][0] if call_args[0] else call_args[1].get("url", "")
        assert "sendMessage" in url
        assert "test-token" in url

        # Verify payload
        payload = json.loads(
            call_args[1]["data"] if "data" in call_args[1] else call_args[0][1]
        )
        assert payload["chat_id"] == "123"
        assert payload["parse_mode"] == "HTML"
        assert payload["text"] == "<b>Hello</b>"


# --- process_post tests ---


class TestProcessPost:
    """Test the main post processing logic."""

    def test_process_nonexistent_file(self, tmp_path, capsys):
        """Should print message and return gracefully for missing files."""
        process_post(str(tmp_path / "nonexistent" / "index.md"))
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower() or "deleted" in captured.out.lower()

    @patch("telegram_notify.telegram_send_message")
    def test_process_post_sends_message(self, mock_send, tmp_path):
        """A valid post should result in a single sendMessage call."""
        post_dir = tmp_path / "test-post"
        post_dir.mkdir()
        post_file = post_dir / "index.md"
        post_file.write_text(
            '---\ntitle: "Test Post"\n---\nHello world.',
            encoding="utf-8",
        )

        process_post(str(post_file))

        mock_send.assert_called_once()
        sent_text = mock_send.call_args[0][0]
        assert "Test Post" in sent_text
        assert "kumekay.com" in sent_text

    @patch("telegram_notify.telegram_send_message")
    def test_process_post_single_call_with_image(self, mock_send, tmp_path):
        """Even with an image in the bundle, should send a single message (not two)."""
        post_dir = tmp_path / "image-post"
        post_dir.mkdir()
        (post_dir / "index.md").write_text(
            '---\ntitle: "Image Post"\nimage: "photo.jpg"\n---\nBody text.',
            encoding="utf-8",
        )
        (post_dir / "photo.jpg").write_bytes(b"\xff\xd8")

        process_post(str(post_dir / "index.md"))

        # Should be exactly 1 call - no separate photo + text
        assert mock_send.call_count == 1

    @patch("telegram_notify.telegram_send_message")
    def test_process_post_uses_pathlib_consistently(self, mock_send, tmp_path):
        """PR review: use pathlib throughout, not os.path."""
        post_dir = tmp_path / "pathlib-test"
        post_dir.mkdir()
        (post_dir / "index.md").write_text(
            '---\ntitle: "Pathlib"\n---\nBody.',
            encoding="utf-8",
        )

        # Should work with Path objects
        process_post(post_dir / "index.md")
        mock_send.assert_called_once()


# --- get_changed_drozdi_files tests ---


class TestGetChangedDrozdiFiles:
    @patch("telegram_notify.subprocess.run")
    def test_filters_drozdi_files(self, mock_run):
        mock_run.return_value = MagicMock(
            stdout="content/drozdi/post1/index.md\ncontent/posts/other.md\nREADME.md\n",
            returncode=0,
        )
        result = get_changed_drozdi_files()
        assert result == ["content/drozdi/post1/index.md"]

    @patch("telegram_notify.subprocess.run")
    def test_excludes_section_index(self, mock_run):
        mock_run.return_value = MagicMock(
            stdout="content/drozdi/_index.md\ncontent/drozdi/post1/index.md\n",
            returncode=0,
        )
        result = get_changed_drozdi_files()
        assert "content/drozdi/_index.md" not in result
        assert "content/drozdi/post1/index.md" in result


# --- Script metadata tests ---


class TestScriptMetadata:
    """Verify PEP 723 inline script metadata is present."""

    def test_has_pep723_metadata(self):
        script_path = Path(__file__).parent / "telegram_notify.py"
        content = script_path.read_text()
        assert "# /// script" in content
        assert "# ///" in content

    def test_declares_frontmatter_dependency(self):
        script_path = Path(__file__).parent / "telegram_notify.py"
        content = script_path.read_text()
        assert "python-frontmatter" in content


# --- No sendPhoto / multipart code ---


class TestNoSendPhoto:
    """The script should NOT have sendPhoto or multipart logic.

    All posts are sent via sendMessage with link preview for image.
    """

    def test_no_send_photo_function(self):
        import telegram_notify

        assert not hasattr(telegram_notify, "telegram_send_photo")

    def test_no_build_multipart_function(self):
        import telegram_notify

        assert not hasattr(telegram_notify, "build_multipart")

    def test_no_find_image_function(self):
        import telegram_notify

        assert not hasattr(telegram_notify, "find_image_in_bundle")
