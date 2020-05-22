# jrhoun.com

This repository uses the static site tool [Hugo](www.gohugo.com) to build jrhoun.com.

## Building the Site Locally

Checkout the site by running: `git clone https://github.com/jrhoun/jrhoun.com.git`

[Install Hugo](https://gohugo.io/getting-started/installing/)

I'm on Windows and used [Chocolatey](https://chocolatey.org/) to install using gitbash.

`choco install hugo`

Build and run the site locally with live updates by running:

`hugo server -D`

The site is accessible at `localhost:1313`.

### Site Configuration

See `conf.toml` for site configuration details.

The site uses the [hugo-vitae](https://github.com/dataCobra/hugo-vitae) theme as a base.

## Writing Content

I'm still figuring this part out. The site's content is mostly going to be blog posts so new posts are added to the `/content/posts/` directory

To create a new blog post:

`hugo new posts/[blog-title-here].md`

This will create a new `.md` in the `/posts/` directory with title date, and draft status metadata.