# jrhoun.com

[![Netlify Status](https://api.netlify.com/api/v1/badges/891066e4-2293-4a7f-a1b4-21fe95a07f78/deploy-status)](https://app.netlify.com/sites/jr-houn-dot-com/deploys)

This repository uses [Hugo](www.gohugo.com) to build jrhoun.com.

## Building the Site Locally

### Setting up the Repo Locally

Checkout the site by running: `git clone https://github.com/jrhoun/jrhoun.com.git`

The site's theme is incorporated in the repo as a git submodule. See https://github.com/jrhoun/jrhoun.com/tree/master/themes. Cloning the repo does not automatically also checkout the submodule. In order to checkout the submodule run the following command in the root project directory:

`git submodule update --init --recursive`

Your repo should now have everything checked out.

### Installing Hugo

[Install Hugo](https://gohugo.io/getting-started/installing/)

#### Windows

On Windows I used [Chocolatey](https://chocolatey.org/) to install using gitbash.

`choco install hugo`

### WSL2

More recently I've begun using WSL2 + Ubuntu. To install:

`sudo apt install hugo`

Build and run the site locally with live updates by running:

`hugo server -D`

The site is accessible at `localhost:1313`.

### Site Configuration

See `conf.toml` for site configuration details.

The site uses a fork of the [hugo-vitae](https://github.com/dataCobra/hugo-vitae) theme as a base.

The fork is [here](https://github.com/jrhoun/hugo-vitae) and has a two notable patches:

* Ensure that the [full content of a blog entry appear in the RSS feed](https://github.com/jrhoun/hugo-vitae/commit/15405f2de992ceeafc24f63bb53e019e7b364f76). This patch was made primarily to enable automated newsletter generation using TinyLetter.
* [Enable symbols to be used in markdown links](https://github.com/jrhoun/hugo-vitae/commit/27ddab37c2702fa0c55aecbcff4c6ec419e65c89)

## Site Hosting

`jrhoun.com` is hosted using netlify.com and is configured to use Continuous Deployment. When new changes are pushed to the `jrhoun/jrhoun.com` master branch, Netlify automatically fetches the repo, builds the site using the `hugo` command, and publishes the updated site files (usually within minutes).

## Domain Registrar

The `jrhoun.com` is currently managed at hover.com.

## Writing Content

I'm still figuring this part out. The site's content is mostly going to be blog posts so new posts are added to the `/content/posts/` directory

To create a new blog post:

`hugo new posts/[blog-title-here].md`

This will create a new `.md` in the `/posts/` directory with title date, and draft status metadata.

## Automatically Generating Newsletters

To enable users to receive emails with blog content, I setup an automated job with [Zapier](https://zapier.com/) that monitors the blog's RSS feed for updates and then pushes new blog content to connected [TinyLetter](https://tinyletter.com/) account. The content appears as a draft that can be manually or automatically sent as a newsletter to subscriber's emails.

## Protected Photos / Encrypted Build Pipeline

This repository is public, images committed to `static/img/` are visible to the internet. To protect sensitive photos while preserving the open-source nature of this blog, I use a symmetrical-key build-time encryption pipeline via OpenSSL.

### Workflow for Adding Private Photos:
1. Place photos in the `static/img/protected/` folder (ignored by git).
2. Run `./scripts/encrypt-photos.sh`.
3. Enter the encryption password when prompted.
4. The script outputs an encrypted file at `static/protected-photos.enc`.
5. Run `git add static/protected-photos.enc` and commit.

### Netlify Automated Decryption:
During the build hook, Netlify reads the `PHOTO_DECRYPTION_KEY` from its private dashboard environment variables, unpacks the raw images strictly in its own isolated builder memory right before executing `hugo`, and uses its standard `.toml` routing to enforce login rules so the URLs are protected in production.
