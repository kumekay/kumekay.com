# AGENTS.md - Project Documentation for AI Agents

## Project Overview
Hugo-based personal blog for kumekay.com. Migrated from Ghost.

## Key Directories
- `content/posts/{slug}/` - Blog posts as Hugo Page Bundles (index.md + images)
- `layouts/` - Hugo templates
- `layouts/partials/` - Reusable template components (head.html, header.html, footer.html)
- `static/css/style.css` - Main stylesheet
- `static/images/` - Global static images

## Blog Post Structure (Page Bundles)
```
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
- Single post header: `.Resize "2400x"` (preserves aspect ratio, 4K-friendly)
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

## Common Commands
```bash
hugo server -D          # Run dev server with drafts
hugo                    # Build static site
```

## Migration Script
`migrate_ghost.py` - Converts Ghost JSON export to Hugo Page Bundles.
- Downloads images from kumekay.com
- Creates proper frontmatter
- Organizes images per-post