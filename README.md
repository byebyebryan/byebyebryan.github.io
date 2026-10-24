# ByeByeBryan

**[Visit the live site →](https://dev.byebyebryan.com/)**

Jekyll site hosted on GitHub Pages.

## Local development

Requires Ruby 3.4.10 (or another version supported by the locked dependencies)
and Bundler 4.x. Install dependencies and start a local preview:

```sh
bundle install
bundle exec jekyll serve
```

Open <http://localhost:4000>. Jekyll rebuilds the preview when source files change.

Build the site into a temporary directory without touching the ignored `_site/` directory:

```sh
bundle exec jekyll build --destination /tmp/byebyebryan-site
```

## Repository layout

- [`index.md`](index.md) — homepage content and front matter.
- [`notes.md`](notes.md) and [`_posts/`](_posts) — development-note index and dated articles.
- [`_layouts/`](_layouts) — page templates.
- [`assets/css/styles.css`](assets/css/styles.css) — layout and styling.
- [`assets/js/showcase.js`](assets/js/showcase.js) — motion controls and still fallbacks.
- [`assets/projects/`](assets/projects/) — media, provenance [manifest](assets/projects/manifest.json), and [license notices](assets/projects/LICENSES.txt).
- [`scripts/`](scripts/) — asset-generation helpers, excluded from the site build.
- [`Gemfile`](Gemfile) and [`Gemfile.lock`](Gemfile.lock) — Ruby dependencies.
- [`_config.yml`](_config.yml) and [`CNAME`](CNAME) — site settings and custom domain.

## Updating assets

Record media sources and hashes in the manifest, and retain applicable license
notices. When replacing a cached image or stylesheet, update its version in the
template. Keep still fallbacks available for paused and reduced-motion viewing.

## Publishing

Add development notes under `_posts/YYYY-MM-DD-slug.md` with a title,
description and categories in YAML front matter. The notes index lists them
automatically. Keep evolving setup instructions in the owning project guides;
articles describe decisions and evidence at their publication date.

Pushes to `main` deploy through GitHub Pages to
[dev.byebyebryan.com](https://dev.byebyebryan.com/). Build locally before pushing,
then check the Pages deployment and live site. Generated `_site/` output stays
untracked.
