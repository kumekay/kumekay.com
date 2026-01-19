# kumekay.com

Personal blog built with Hugo static site generator.

## Quick Start

```bash
# Install Hugo (if not already installed)
# macOS: brew install hugo
# Linux: snap install hugo

# Run local development server
hugo server -D

# Build for production
hugo

# Serve production build
hugo server --renderToMemory
```

## Blog Workflow

### Creating a New Post

Create a new post as a leaf bundle:

```bash
# Create post directory
mkdir -p content/posts/your-post-slug

# Create index.md with front matter
cat > content/posts/your-post-slug/index.md << 'EOF'
---
title: "Your Post Title"
date: 2026-01-19
tags: ["tag1", "tag2"]
description: "Brief description for SEO and social sharing"
header: "media/header.jpg"  # Optional: header image
# OR for interactive headers:
headerHtml: |
  <canvas id="hero"></canvas>
  <script src="media/hero.js"></script>
---

Write your post content here in markdown.
EOF
```

### Front Matter Fields

- `title` (required): Post title
- `date` (required): Publication date (YYYY-MM-DD)
- `tags` (optional): Array of tag strings for categorization
- `description` (optional): Meta description for SEO
- `header` (optional): Path to header image relative to post directory
- `headerHtml` (optional): HTML snippet for interactive headers (canvas/WebGL)

### Adding Media

Place images and other media in the `media/` subdirectory of your post:

```bash
content/posts/your-post-slug/
├── index.md
└── media/
    ├── header.jpg
    ├── diagram.png
    └── hero.js
```

Reference images in markdown using relative paths:

```markdown
![Alt text](media/diagram.png)
```

### Interactive Headers

For WebGL or canvas headers:

```yaml
---
headerHtml: |
  <canvas id="hero"></canvas>
  <script src="media/hero.js"></script>
---
```

The HTML is rendered directly above the post content. Place your WebGL/canvas initialization code in `media/hero.js`.

### Tag Pages

Tag pages are automatically generated at `/tags/{tag-name}/`. Posts are automatically categorized by their `tags` front matter.

### Atom Feed

The Atom feed is available at `/index.atom` and includes all published posts sorted by date.

## Project Structure

```
kumekay.com/
├── config.toml                 # Hugo configuration
├── content/
│   ├── _index.md               # Homepage content
│   └── posts/
│       └── {slug}/
│           ├── index.md        # Post content
│           └── media/          # Post assets
├── layouts/                    # Custom Hugo templates
├── static/                     # Static assets (CSS, favicon)
└── public/                     # Generated site (not in git)
```

## Development

### Local Development

```bash
# Run dev server with drafts
hugo server -D

# Run dev server without drafts
hugo server

# Build production site
hugo

# Clean build cache
hugo --cleanDestinationDir
```

### Adding New Features

For significant changes to the blog functionality:
1. Create an OpenSpec proposal: `openspec/changes/{change-id}/`
2. Validate: `openspec validate {change-id} --strict --no-interactive`
3. Get approval before implementation
4. Track progress in the change's `tasks.md`

See `openspec/changes/add-blog-migration-to-hugo/` for an example.

## Deployment

```bash
# Build for production
hugo --minify

# Deploy contents of public/ directory
# (deployment method depends on hosting platform)
```

## OpenSpec

This project uses OpenSpec for spec-driven development. See `openspec/AGENTS.md` for AI agent instructions and documentation on the spec workflow.
