# jrhoun.com

> [!NOTE]
> **AI Disclosure**: This repository—including its structure, theme refinements, and deployment automation—is maintained and organized with the assistance of **Antigravity**, an AI coding assistant.

This repository contains the source code, theme, and deployment configuration for jrhoun.com, powered by **Ghost CMS**.

## Repository Structure

- `custom-theme/`: The custom Ghost theme (Handlebars).
- `ghost-deploy/`: Docker Compose configuration for self-hosting Ghost.
- `scripts/`: Utility scripts for theme packaging and migration.
- `legacy-hugo/`: Archive of the previous Hugo-powered site.

## Ghost Deployment

The site is self-hosted using Docker. The configuration is located in the `ghost-deploy/` directory.

### Prerequisites
- Docker and Docker Compose
- A reverse proxy (e.g., Synology Reverse Proxy, Nginx, or Caddy) for SSL termination.

### Setup
1. Copy `ghost-deploy/.env.template` to `ghost-deploy/.env`.
2. Fill in your specific environment variables (URL, Database passwords, Mailgun credentials).
3. Run the deployment:

   ```bash
   cd ghost-deploy
   docker-compose up -d
   ```

## Custom Theme Development

The custom theme is located in `custom-theme/`.

### Packaging the Theme

To create a zip file for uploading to Ghost, use the provided script:
```bash
python3 scripts/zip_theme.py
```
This will generate a versioned zip file in the `custom-theme/` directory.

## Legacy Site
The previous Hugo-based site has been archived in the `legacy-hugo/` directory for historical reference. The original `content/`, `themes/`, and `config.toml` are preserved there.

