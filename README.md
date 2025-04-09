# My Personal Website

This is the source code for [my personal website](https://emiliosao.me), built with [Hugo](https://gohugo.io/) using a customized version of the [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme.

## Features
- A minimalist landing page with an about section
- A blog that aggregates content from Letterboxd
- A CV page with an overview of education, skills, and experience
- A tech radar page hosted in the `static/` folder
- Automated updates for Letterboxd posts via GitHub Actions

## Repository Structure
- `content/`: Source markdown files for site content
  - `content/blog/`: Blog posts including automatically updated Letterboxd diary entries
- `themes/papermod/`: Customized PaperMod theme
- `scripts/`: Automation scripts for blog posts
- `static/`: Static assets like icons, PDFs, and the tech radar
- `.github/workflows/`: Automation workflows
  - `deploy.yml`: Deploys the site to GitHub Pages
  - `update_letterboxd.yml`: Fetches new Letterboxd entries

## Development

To run the website locally:

```bash
hugo server -D --disableFastRender --ignoreCache --baseURL http://localhost:1313/
```
## Automation
The site features two main automated workflows:

1. **Letterboxd Updates**: Runs daily to check for new Letterboxd entries and adds them to the blog
2. **Site Deployment**: Automatically builds and deploys the site when changes are pushed to main

## Deployment
The site is deployed automatically to GitHub Pages using GitHub Actions.

## How to Update
To manually update the site or Letterboxd posts:

1. Make changes locally and push to the main branch
2. The GitHub Actions workflow will automatically build and deploy the site
3. Alternatively, trigger the workflows manually from the Actions tab in GitHub
