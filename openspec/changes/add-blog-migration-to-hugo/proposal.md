# Change: Migrate blog from Ghost CMS to Hugo static site

## Why
Migrate from self-hosted Ghost CMS to Hugo for markdown-based authoring, faster page loads, and simpler hosting without database dependencies.

## What Changes
- Initialize Hugo site structure with custom minimalist templates
- Add support for markdown-based content authoring
- Implement URL preservation from Ghost
- Add Atom RSS feed generation
- Support header images and interactive HTML headers (canvas/WebGL)
- Create Ghost to Hugo migration script
- **BREAKING**: Changes content management from Ghost Admin to markdown files

## Impact
- Affected specs: blog
- Affected code: Site architecture, templates, content format
