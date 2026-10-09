# ByeByeBryan

A compact, visual project showcase at `dev.byebyebryan.com`.

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
- [`assets/`](assets) contains the stylesheet, media controls and project captures.
- [`assets/projects/manifest.json`](assets/projects/manifest.json) records media sources, hashes and preview boundaries.
- [`CNAME`](CNAME) configures the custom domain.

Pushes to `main` are deployed by GitHub Pages and published at <https://dev.byebyebryan.com>.

## Content

The homepage features six projects and a short tools strip. Keep each project
caption to one sentence. Use project media and direct demo/code links; there are
no long-form project pages or required update schedule. Renderer previews and
simulated data must stay clearly identified.

The flight clip is rendered from retained telemetry with
[`scripts/render-flight.py`](scripts/render-flight.py); it does not rerun a
simulation. The Pylander-inspired vector animation uses `random-462` from
the October 8, 2026 procedural-terrain correction sweep, with receipt-checked
inputs and a verified target landing. The vehicle is an enlarged presentation
marker. White outlines on black use restrained red thrust, green landing pads
and a cyan flight trail. Source paths, playback speed and media treatments are
in the manifest.
