# ByeByeBryan

This is the legacy GitHub Pages site for `dev.byebyebryan.com`.

## Prerequisites

- Ruby 3.4.10 (or another Ruby version supported by the locked dependencies)
- Bundler 4.x

## Local development

Install the locked dependencies:

```sh
bundle install
```

Serve the site locally at <http://localhost:4000>:

```sh
bundle exec jekyll serve
```

Build the site into a temporary directory without touching the ignored `_site/` directory:

```sh
bundle exec jekyll build --destination /tmp/byebyebryan-site
```

## Source locations

- [`_config.yml`](_config.yml) contains the Jekyll configuration.
- [`index.md`](index.md) contains the homepage content.
- [`_layouts/`](_layouts) contains the page templates.
- [`assets/`](assets) contains the stylesheet and project media.
- [`CNAME`](CNAME) configures the custom domain.

Pushes to `main` are deployed by GitHub Pages and published at <https://dev.byebyebryan.com>.
