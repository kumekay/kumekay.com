## ADDED Requirements

### Requirement: Hugo Site Structure
The system SHALL provide a Hugo static site generator configuration with content, layout, and static asset directories organized for minimalist blog publishing.

#### Scenario: Site initialization
- **WHEN** Hugo site is initialized
- **THEN** the system has content/posts/, layouts/, and static/ directories

### Requirement: Markdown Content Format
The system SHALL support blog posts authored in markdown files with front matter for metadata including title, date, tags, description, and header configuration.

#### Scenario: Post with header image
- **GIVEN** a markdown post with header field pointing to media/header.jpg
- **WHEN** the post is rendered
- **THEN** the header image is displayed above post content

#### Scenario: Post with HTML header
- **GIVEN** a markdown post with headerHtml field containing canvas and script tags
- **WHEN** the post is rendered
- **THEN** the HTML header is injected and rendered above post content

### Requirement: URL Preservation
The system SHALL generate URLs in the format `/:slug/` to preserve existing Ghost CMS URLs.

#### Scenario: Post URL generation
- **GIVEN** a post with slug "aeration-tube-for-dwc-hydroponics"
- **WHEN** the site is built
- **THEN** the post is accessible at `/aeration-tube-for-dwc-hydroponics/`

### Requirement: Tag-based Categorization
The system SHALL support tag-based categorization with URLs in the format `/tags/{tag-name}/`.

#### Scenario: Tag page generation
- **GIVEN** multiple posts tagged "hydroponics"
- **WHEN** the site is built
- **THEN** `/tags/hydroponics/` lists all hydroponics posts

### Requirement: Atom RSS Feed
The system SHALL generate an Atom RSS feed at `/index.atom` for all published posts.

#### Scenario: Feed generation
- **GIVEN** published blog posts
- **WHEN** the site is built
- **THEN** an Atom feed is available with all posts sorted by date

### Requirement: Ghost to Hugo Migration
The system SHALL provide a migration script that converts Ghost CMS JSON exports to Hugo markdown format preserving URLs, dates, tags, and media.

#### Scenario: Migration script execution
- **GIVEN** a Ghost JSON export file
- **WHEN** the migration script runs
- **THEN** Hugo markdown files are created in content/posts/{slug}/ directories
- **AND** images are downloaded to media/ subdirectories
- **AND** front matter includes title, date, tags, and header fields

#### Scenario: Content conversion
- **GIVEN** Ghost post with HTML content
- **WHEN** the migration script runs
- **THEN** HTML is converted to markdown format
- **AND** markdown is saved in index.md

#### Scenario: URL verification
- **GIVEN** completed migration
- **WHEN** URL verification runs
- **THEN** generated URLs match Ghost sitemap
- **AND** any mismatches are reported

### Requirement: Minimalist Templates
The system SHALL provide custom Hugo templates with minimal HTML and CSS for fast page loads.

#### Scenario: Base template
- **WHEN** a page is rendered
- **THEN** it includes head, header, main content block, and footer partials

#### Scenario: Single post template
- **WHEN** a single post is rendered
- **THEN** it displays post header (image or HTML) followed by content

### Requirement: Leaf Bundle Structure
The system SHALL organize posts as leaf bundles with content in index.md and assets in media/ subdirectory.

#### Scenario: Post assets
- **GIVEN** a post with header.jpg and diagram.png
- **WHEN** the post is organized
- **THEN** index.md contains the post content
- **AND** header.jpg and diagram.png are in media/ subdirectory
