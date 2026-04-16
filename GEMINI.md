# Gemini Project Context: jrhoun.com

This repository contains the source code, theme, and deployment configuration for **jrhoun.com**, powered by **Ghost CMS**. The project follows a containerized deployment strategy and includes custom theme development and content migration utilities.

## Project Overview

- **CMS:** Ghost (version 6.x)
- **Theme:** Custom Handlebars-based theme located in `custom-theme/`.
- **Deployment:** Docker Compose based, optimized for self-hosting (e.g., on a NAS or VPS).
- **History:** Includes a `legacy-hugo/` directory containing the previous site's Hugo source.

## Repository Structure

- `custom-theme/`: The custom Ghost theme.
  - `assets/css/screen.css`: Main stylesheet using modern CSS variables for design tokens.
  - `*.hbs`: Handlebars templates (index, post, page, author, tag, etc.).
  - `package.json`: Theme metadata and packaging scripts.
- `ghost-deploy/`: Docker deployment configuration.
  - `docker-compose.yml`: Defines `ghost` and `db` (MySQL 8.0) services.
  - `.env.template`: Template for required environment variables (DB passwords, Mailgun credentials).
- `scripts/`: Python and Node.js utility scripts.
  - `zip_theme.py` / `do_zip.py`: Packages the custom theme into a versioned `.zip` for Ghost upload.
  - `migrate.py`: A robust migration script that converts Hugo markdown content (from `legacy-hugo/`) into a Ghost-compatible JSON import file, including image handling and shortcode conversion.
- `legacy-hugo/`: Historical archive of the site when it was powered by Hugo.

## Building and Running

### Ghost Deployment (Self-Hosted)
1. Navigate to the deployment directory: `cd ghost-deploy`.
2. Prepare environment variables: `cp .env.template .env` and fill in the values.
3. Start the services:
   ```bash
   docker-compose up -d
   ```
4. Access the site at the URL specified in your `.env` (default configured for `https://www.jrhoun.com`).

### Custom Theme Development
- **Packaging:** To create a theme zip for uploading to the Ghost Admin panel:
  - From the root: `python3 scripts/zip_theme.py`
  - OR from `custom-theme/`: `npm run zip`
- **Styles:** Modify `custom-theme/assets/css/screen.css`. It uses custom properties defined in `:root` for colors and typography.

### Migration
If you need to re-run the migration from Hugo:
1. Ensure `legacy-hugo/content/posts` is populated.
2. Run the migration script: `python3 scripts/migrate.py`.
3. The script generates `ghost_import.zip` which can be imported via the Ghost Admin settings.

## Development Conventions

- **Aesthetic:** Minimalist, typography-focused design.
- **Typography:** Uses 'Inter' for body text and 'Outfit' for headings.
- **Dark Mode:** Implemented via a `dark` class on the `<html>` element, toggled via JavaScript and persisted in `localStorage`.
- **Ghost Integration:** Adheres to Ghost theme standards (Handlebars helpers like `{{ghost_head}}`, `{{ghost_foot}}`, `{{content}}`, etc.).
- **Content:** Posts are typically written in Markdown or via the Ghost editor. The migration script handles historical Hugo shortcodes (YouTube, figures, relrefs).
