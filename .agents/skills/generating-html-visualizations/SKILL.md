---
name: generating-html-visualizations
description: Use when creating standalone HTML files with patterns, graphics, or visualizations for blog posts
---

# Generating HTML Visualizations

## Overview

Create single, self-contained HTML files with visual elements (patterns, graphics, data visualizations) to embed in Hugo blog posts.

## Workflow

1. **Ask for article directory** - Must know which `content/posts/{slug}/` or `content/{section}/{slug}/` to place the file
2. **Generate single HTML file** - All code in one file (HTML + CSS + JS inline)
3. **Save to article directory** - File goes alongside `index.md`

## Constraints

- **Single file**: Everything inline (no external dependencies except CDNs)
- **Self-contained**: Must work when opened directly in browser
- **No external images**: Use inline SVG, data URIs, or pure CSS

## Common Patterns

### Inline SVG

```html
<svg width="100" height="100" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="40" fill="#3498db"/>
</svg>
```

### CSS Patterns

```html
<style>
  .pattern {
    background-image: repeating-linear-gradient(
      45deg, #000 0, #000 10px, #fff 10px, #fff 20px
    );
  }
</style>
```

### Canvas/JS Visualization

```html
<canvas id="canvas"></canvas>
<script>
  const ctx = document.getElementById('canvas').getContext('2d');
  // drawing code
</script>
```

## File Location

```text
content/posts/my-article/
├── index.md
├── feature.jpg
└── visualization.html    # Generated file goes here
```
