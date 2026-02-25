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
image: "feature.jpg"  # Optional: feature image (place in same directory)
---

Write your post content here in markdown.
EOF
```

### Front Matter Fields

- `title` (required): Post title
- `date` (required): Publication date (YYYY-MM-DD)
- `tags` (optional): Array of tag strings for categorization
- `description` (optional): Meta description for SEO
- `image` (optional): Feature image filename relative to post directory

### Adding Media

Place images directly in the post directory:

```bash
content/posts/your-post-slug/
├── index.md
├── feature.jpg    # Referenced as image: "feature.jpg"
└── diagram.png    # Additional images
```

Reference images in markdown using relative paths:

```markdown
![Alt text](diagram.png)
```

### Tag Pages

Tag pages are automatically generated at `/tags/{tag-name}/`. Posts are automatically categorized by their `tags` front matter.

### Atom Feed

The Atom feed is available at `/index.atom` and includes all published posts sorted by date.

## Project Structure

```text
kumekay.com/
├── config.toml                 # Hugo configuration
├── content/
│   ├── _index.md               # Homepage content
│   └── posts/
│       └── {slug}/
│           ├── index.md        # Post content
│           └── *.jpg, *.png    # Post images
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
