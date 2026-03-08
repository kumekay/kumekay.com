# AGENTS.md - Project Documentation for AI Agents

## Project Overview

Hugo-based personal blog for kumekay.com. Migrated from Ghost. Has 3 independent sections with unique designs.

## Site Sections

| Section | Path | Content | Stylesheet |
|---------|------|---------|------------|
| Main (posts) | `/` | English technical posts | `style.css` |
| utoolek | `/utoolek/` | Tools with GitHub links | `utoolek.css` (warm monochrome) |
| drozdi | `/drozdi/` | Russian informal posts | `drozdi.css` (pale pink/yellow) |

## Key Directories

- `content/posts/{YYYY-MM-DD-slug}/` - Main blog posts (English, technical)
- `content/utoolek/{YYYY-MM-DD-slug}/` - Tool entries with GitHub links
- `content/drozdi/{YYYY-MM-DD-slug}/` - Russian blog posts

**Important**: All post/tool directories must include a date prefix in `YYYY-MM-DD-slug` format. The date should match the `date` field in the frontmatter.

- `layouts/` - Hugo templates
- `layouts/utoolek/` - utoolek section templates (list.html, single.html, list.json)
- `layouts/drozdi/` - drozdi section templates (list.html, single.html)
- `layouts/partials/` - Reusable template components (head.html, header.html, footer.html, post-header.html)
- `static/css/` - Stylesheets (style.css, utoolek.css, drozdi.css)
- `static/js/fuse.search.js` - Fuse.js search for utoolek section
- `static/images/` - Global static images
- `scripts/telegram_notify.py` - Telegram auto-posting for drozdi
- `.github/workflows/telegram-notify.yml` - GitHub Actions workflow for Telegram

## Blog Post Structure (Page Bundles)

```text
content/posts/my-post/
├── index.md          # Post content with frontmatter
├── feature.jpg       # Feature image (referenced in frontmatter as `image: "feature.jpg"`)
└── other-images.png  # Additional images for the post
```

### Frontmatter Example

```yaml
---
title: "Post Title"
date: 2026-02-08
draft: false
slug: "post-slug"
tags: ["tag1", "tag2"]
author: "Author Name"
image: "feature.jpg"  # Relative to bundle directory
---
```

## Templates

### Image Processing

- Homepage/list images: `.Resize "1600x"` (preserves aspect ratio, 4K-friendly)
- Single post feature image: `.Resize "2400x"` (preserves aspect ratio, 4K-friendly)
- Use `.Resize` to preserve aspect ratio, not `.Fill` which crops

### Template Context in Loops

When inside a `range` loop with nested `with` blocks, save the page context:

```go
{{ range .Pages }}
  {{ $page := . }}
  {{ with .Resources.GetMatch .Params.image }}
    <a href="{{ $page.RelPermalink }}">...</a>
  {{ end }}
{{ end }}
```

## Styling

### CSS Variables

```css
--content-width: 720px;    /* Text content max-width */
--wide-width: 900px;       /* Images and container max-width */
--side-padding: 1.5rem;    /* Horizontal padding */
```

### Font

Uses "Forum" from Google Fonts (with Cyrillic support).

### Mobile Responsive

Media query at `max-width: 600px` adjusts layout for phones.

## Python Development

Use red/green TDD for all Python script changes:

1. **Red**: Write a failing test first
2. **Green**: Write minimal code to make the test pass
3. **Refactor**: Clean up while keeping tests green

Test command: `uv run --with pytest --with python-frontmatter pytest scripts/test_telegram_notify.py -v`

## Common Commands

```bash
hugo server -D          # Run dev server with drafts
hugo                    # Build static site
pre-commit run --all-files   # Run all linters (ruff + markdownlint)
```

## Migration Script

`migrate_ghost.py` - Converts Ghost JSON export to Hugo Page Bundles.

- Downloads images from kumekay.com
- Creates proper frontmatter
- Organizes images per-post
