---
title: Keeping Codex sessions in view
description: A quick check, a closer investigation, or a terminal dashboard that stays open—locally and across machines.
categories: [tools]
social_image: /assets/projects/observer-terminal-wide.png
social_image_alt: Agent Observer's released terminal dashboard rendered from fictional cached Codex sessions.
social_image_width: 1680
social_image_height: 576
---

While you are working inside a Codex conversation, the native session list is
out of view. A separate terminal can keep an overview visible while you continue
working in the native TUI, including when your sessions span several machines.

Agent Observer now supplies that terminal view: one command for a quick check,
session commands for investigation, and a dashboard that stays open beside your
work. It brings the read-only foundation described in the
[earlier observation article]({% post_url 2026-10-23-read-only-agent-state-across-machines %})
into a tool you can use directly while working.

Native Codex continues to own the conversations. Observer reads the configured
sources and keeps session state and source health visible together.

![Agent Observer terminal dashboard overview showing fictional Codex sessions across configured hosts, with source health and repository context.]({{ '/assets/projects/observer-terminal-wide.png' | relative_url }})

*Released a14 terminal application rendered from fictional cached sources.*

[Open the full-size dashboard]({{ '/assets/projects/observer-terminal-wide.png' | relative_url }}) ·
[See the compact layout]({{ '/assets/projects/observer-terminal-compact.png' | relative_url }}) ·
[Watch the terminal demo](https://dev.byebyebryan.com/fleet-plus/assets/observer-terminal-demo.mp4) ·
[Media provenance](https://dev.byebyebryan.com/fleet-plus/assets/provenance.json)

## Three ways to look

A quick check should finish with the answer. Bare `agent-observer` prints a
compact overview with up to ten rows and a coverage summary, then exits.

For a closer look, `sessions list` shows all matching sessions and full IDs.
Filters and metadata search help narrow the view; `sessions show` inspects an
exact identity on its host and home. `sessions sources` shows the health of the
selected sources. Scripts can use terminal JSON interface 1 instead of parsing
the human table.

```sh
agent-observer
agent-observer sessions list --query renderer
agent-observer sessions sources
agent-observer sessions list --format json
```

`agent-observer dashboard` keeps the view open. It has search, display filters,
source health and selected-session details. Workspace details put the reported
working directory and repository root near the session summary. In a14,
dashboard search also covers current cached repository roots, shared Git
directories and paths relative to a repository. It reads admitted metadata
without inspecting the filesystem or searching conversation content.

The short demo follows one fictional working set: overview, repository search,
session details, then back to the overview. The compact still shows the same
scenario in a narrower terminal.

## Make the source setup explicit

The reader uses existing working-set publishers/bridges. Installing the CLI or
opening the dashboard does not start them. This prerequisite belongs at the
start of onboarding: a reader needs a source to read.

The [sessions CLI guide](https://github.com/byebyebryan/agent-observer/blob/main/docs/guides/sessions-cli.md)
owns the published installation pair and the private `terminal.toml` setup.
Each source entry names an existing host/home, Mesh source, namespace and
route/socket. That working-set bridge endpoint is distinct from the collector's
Service 4 socket. The [working-set prerequisites](https://github.com/byebyebryan/agent-observer/blob/main/docs/guides/working-set.md#bounded-inspection)
describe the required running sources; arrange their hosting before reader setup.

Once configured, check the file without connecting, then read source health:

```sh
agent-observer sessions sources --configured
agent-observer sessions sources
```

The [dashboard guide](https://github.com/byebyebryan/agent-observer/blob/main/docs/guides/dashboard.md)
adds the optional terminal UI dependencies and reuses the same configuration.
The shared site links to those owner instructions so artifact hashes and install
pins have one maintained home. Public setup does not require the maintainer's
private chezmoi configuration.

## Keep uncertainty in the view

A working set contains admitted active membership and recent context. It is a
bounded view of configured sources. Membership, runtime and phase remain separate
facts; a waiting phase does not by itself mean a response is required.

Source health remains visible while filters are applied or details are open.
A disconnected source cannot turn an empty result into proof of an empty fleet.
Delivery heartbeats cannot renew expired native facts. This was part of the
public-read foundation, and it remains part of the terminal experience.

The images demonstrate the released application's rendering with fictional
inputs. They add no native accuracy, sustained capacity or physical-device
acceptance. The owner's [qualification boundary](https://github.com/byebyebryan/agent-observer/blob/main/docs/guides/dashboard.md#qualification-boundary)
keeps those measurements and limits separate. The
[current compatibility guide](https://dev.byebyebryan.com/fleet-plus/compatibility/)
also distinguishes the a14 reader from a11 producers and independent consumers.

## One collection, independent tools

[Fleet Plus](https://dev.byebyebryan.com/fleet-plus/) now leads with the terminal
product while keeping the collection's other entry points clear. Mesh and SSH
Plus serve host access independently. Agent Plus opens or focuses native
Codex/Claude TUIs without Observer or Tmux. The Tmux pair remains useful for
generic sessions and explicit actions.

The RLCD dashboard is a separate hardware consumer with its own presentation,
package selection and physical acceptance. Observer's public reads remain useful
for that display, diagnostics and other utilities. Codex is its only native
observation adapter; Claude monitoring, Observer writes and standalone active-only
hosting remain retired.

For the terminal path, [start with the reader setup](https://dev.byebyebryan.com/fleet-plus/start/)
and follow the current component guides from there.
