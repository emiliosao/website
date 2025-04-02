# My Personal Website

This is the source code for [my personal website](https://emiliosao.me), built with [Hugo](https://gohugo.io/) using the [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme.

## Features
- A minimalist landing page with an about section.
- A blog that aggregates content from Letterboxd and other sources.
- A CV page with an overview of education, skills, and experience.
- A tech radar page hosted in the `static/` folder.
- Automated updates for Letterboxd posts via GitHub Actions.

## Development

To run the website locally:

```bash
hugo server -D --disableFastRender --ignoreCache --baseURL http://localhost:1313/
```

## Deployment

The site is deployed automatically to GitHub Pages using GitHub Actions.

### How to Update

To manually update the site or Letterboxd posts:
1. Make changes locally and push to the `main` branch.
2. The GitHub Actions workflow will automatically build and deploy the site.

## License

MIT License

