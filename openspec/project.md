# Project Context

## Purpose
Personal blog at kumekay.com - migrating from self-hosted Ghost CMS to a static site built with Hugo. Goals:
- Write articles in markdown using Obsidian or VS Code
- Minimalist, fast-loading pages
- Preserve existing URLs from Ghost
- Custom template (no pre-built themes)

## Tech Stack
- Hugo v0.154+ (static site generator)
- Custom HTML/CSS templates (no themes, no frameworks)
- Atom feed for syndication
- Deployment: TBD

## Project Conventions

### Content Structure
```
content/posts/{slug}/
├── index.md           # Post content with front matter
└── media/             # Post-specific assets (images, scripts, HTML)
    └── header.jpg
```

### Front Matter Format
```yaml
---
title: "Post Title"
date: 2024-01-15
slug: "post-slug"           # URL slug (optional, defaults to directory name)
tags: ["tag1", "tag2"]
description: "Brief description for meta and feed"
header: "media/header.jpg"  # Static image header
# OR
headerHtml: |               # Custom HTML/WebGL header
  <canvas id="hero"></canvas>
  <script src="media/hero.js"></script>
---
```

### URL Structure
- Posts: `/{slug}/` (e.g., `/aeration-tube-for-dwc-hydroponics/`)
- Tags: `/tags/{tag}/`
- Feed: `/feed.atom`

### Code Style
- Minimal CSS, no frameworks (single style.css)
- No JavaScript unless required for specific post headers (WebGL/canvas)
- Semantic HTML5
- CSS custom properties for theming

### Architecture Patterns
- Hugo leaf bundles for posts (directory with index.md)
- Custom layouts in `layouts/` (no external themes)
- Page resources for post-specific media
- Partials for reusable template components

### File Organization
```
kumekay.com/
├── hugo.toml              # Site configuration
├── content/posts/         # Blog posts (leaf bundles)
├── layouts/
│   ├── _default/          # baseof.html, list.html, single.html
│   ├── partials/          # head, header, footer, post-header
│   └── index.html         # Homepage
├── static/css/style.css   # Global styles
└── docs/plans/            # Design documents
```

## Domain Context
- Blog migrated from Ghost CMS
- Must preserve all existing URLs for SEO
- Headers can be images or interactive HTML snippets (canvas/WebGL)
- Content is written in standard markdown

## Important Constraints
- URL preservation from Ghost is critical (no /posts/ prefix)
- Keep dependencies minimal (Hugo only)
- Fast page load times (no heavy JS frameworks)
- Raw HTML allowed in markdown for flexibility

## External Dependencies
- Hugo (static site generator)
- Ghost export JSON for data migration

## Git Workflow
- Main branch for production
- Feature branches for changes
- Commit messages: `type: brief description`
  - types: feat, fix, docs, style, refactor

## Testing Strategy
- `hugo server` for local preview
- `hugo --minify` for production build
- Verify URLs match Ghost sitemap after migration
