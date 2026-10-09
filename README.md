# Static Site Generator

A simple static site generator built with Python as a study project from [Boot.dev](https://www.boot.dev/).

The project parses Markdown files, converts them into an HTML node tree, and generates a static website from a template.

## Features

- Markdown block parsing
- Inline Markdown parsing
- Headings, paragraphs, lists, quotes, and code blocks
- Bold, italic, code, links, and images
- Recursive page generation
- Static asset copying
- Configurable base path for GitHub Pages
- Local development server
- GitHub Pages deployment

## Project Structure

```text
.
├── content/       # Markdown source files
├── docs/          # Generated website
├── src/           # Static site generator
├── static/        # Static assets
├── build.sh       # Production build
├── main.sh        # Local development server
└── template.html  # HTML template
```

## Local Development

Run:

```bash
./main.sh
```

The site will be available at:

```text
http://localhost:8888/
```

## Production Build

For GitHub Pages, run:

```bash
./build.sh
```

The generated website is placed in `docs/` and uses the repository's base path.

## Live Site

[View the published site](YOUR_GITHUB_PAGES_URL)

## About

This project was built as a study exercise from Boot.dev to learn how static site generators work, including Markdown parsing, HTML generation, filesystem traversal, and GitHub Pages deployment.
