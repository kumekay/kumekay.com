## Context
Migrating kumekay.com from self-hosted Ghost CMS (database-driven) to Hugo static site generator (file-based) to enable markdown-based authoring, faster page loads, and simpler hosting.

## Goals / Non-Goals
- Goals:
  - Write articles in markdown (Obsidian/VS Code)
  - Preserve all existing URLs from Ghost
  - Minimalist, fast-loading pages
  - Support header images or HTML snippets (canvas/WebGL)
  - Tag-based categorization
  - Atom RSS feed
- Non-Goals:
  - Support for Ghost Admin interface
  - Database-driven content management
  - Dynamic content generation beyond Hugo's built-ins

## Decisions
- Static Site Generator: Hugo
  - Fast build times, mature ecosystem, minimal dependencies
  - Single binary, easy deployment
- Content Structure: Leaf bundles
  - Each post in `content/posts/{slug}/` with `index.md` and `media/` folder
  - Keeps post assets together, easier management
- Feed Format: Atom
  - More modern than RSS 2.0, well-supported
  - Better defined specification
- Theme Approach: Custom templates (no theme)
  - Full control over HTML output
  - Avoids theme bloat and dependencies
- CSS Framework: None
  - Minimalism, fast loads
  - Full control over styling
- Permalink Structure: `/:slug/`
  - Preserves Ghost URL structure exactly
- Taxonomies: Tags only
  - Simpler than categories + tags
  - Matches current Ghost setup

## Risks / Trade-offs
- Risk: URL preservation during migration
  - Mitigation: Verify generated URLs against Ghost sitemap
  - Rollback: Keep Ghost running in parallel until verified
- Risk: Content quality during HTML→markdown conversion
  - Mitigation: Manual review of key posts, automated formatting checks
- Trade-off: Loss of Ghost Admin WYSIWYG editor
  - Benefit: Markdown is plain text, version control friendly
- Trade-off: No built-in comments (Ghost had them)
  - Acceptable: External service can be added later if needed

## Migration Plan
### Steps
1. Export content from Ghost (JSON format)
2. Run migration script:
   - Parse Ghost JSON
   - Create directory structure: `content/posts/{slug}/`
   - Convert HTML content to markdown
   - Download and save images to `media/` directories
   - Generate Hugo front matter (title, date, tags, header)
3. Verify URLs against Ghost sitemap
4. Test locally with `hugo server`
5. Deploy to staging for final verification
6. Switch DNS to new site

### Rollback
- Keep Ghost instance running until migration verified
- DNS can be pointed back to Ghost if issues arise
- Version control preserves all markdown content

## Open Questions
- Comment system: Use external service (Disqus, Utterances) or build custom?
- Image optimization: Use Hugo image processing or pre-optimize?
- Analytics: Preserve Ghost analytics or switch to new solution?
