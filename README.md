# ByeByeBryan

**[Visit the live site →](https://dev.byebyebryan.com/)**

Source for my visual project showcase: games, graphics, simulation, desktop
tools, and desk displays. Built with Jekyll and published through GitHub Pages.

## Selected projects

| Project | Focus |
| --- | --- |
| Cubey | Procedural worlds, Vulkan rendering, and GPU fluids. |
| Powered Descent Lab | Rocket guidance and terrain-aware flight planning. |
| Gomoku2D | Gomoku, Renju, bots, and replay analysis. |
| Raster 90 | A bitmap watch face with its own pixel type and icons. |
| Codex Plus | Workers, watches, later checks, peer messages, and browser reports. |
| Desk displays | A USB notification panel and a live RLCD agent dashboard. |
| Observer Core | Mesh Plus, Tmux Observer, and Agent Observer. |
| Rofi Plus | SSH Plus, Tmux Plus, and Agent Plus. |

The homepage also has a small-tools strip. Observer Core and Rofi Plus are
showcase groupings; their components keep separate repositories and
responsibilities. Codex Plus and Raster 90 link to their own project sites.

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

## Editing the site

- [`index.md`](index.md) — project captions, ordering, and links.
- [`_layouts/`](_layouts) — page templates and project preview markup.
- [`assets/css/styles.css`](assets/css/styles.css) — layout and styling.
- [`assets/js/showcase.js`](assets/js/showcase.js) — motion controls and still fallbacks.
- [`assets/projects/`](assets/projects/) — media, provenance [manifest](assets/projects/manifest.json), and [license notices](assets/projects/LICENSES.txt).
- [`_config.yml`](_config.yml) and [`CNAME`](CNAME) — site settings and custom domain.

Keep project captions to one sentence and link directly to the code or demo.
Identify generated previews and fictional data in their captions. When replacing
media, update its manifest entry and hashes; update the asset version in the
template when changing a cached image or stylesheet.

## Media notes

- The RLCD dashboard operates on a real Observer/Mesh feed. Its showcase loop
  uses the production renderer with fictional conversations and virtual time.
- The notification panel and Raster 90 use generated UI previews.
- The flight clip is rendered from retained simulation telemetry using
  [`scripts/render-flight.py`](scripts/render-flight.py), with presentation
  styling and accelerated playback.

These previews are separate from physical-device footage. The Codex Plus,
Observer Core, and Rofi Plus cards use HTML overviews. Exact sources, revisions,
hashes, and media treatments are recorded in the manifest.

## Publishing

Pushes to `main` deploy through GitHub Pages to
[dev.byebyebryan.com](https://dev.byebyebryan.com/). Build locally before pushing,
then check the Pages deployment and live site. Generated `_site/` output stays
untracked.
