---
title: From tmux sessions to native shared runtimes
description: How native agent managers changed the roles of six related tools—and why their repositories remain separate.
categories: [tools]
social_image: /assets/projects/rlcd-roster.png
social_image_alt: Production dashboard renderer with fictional conversations; not physical footage.
social_image_width: 400
social_image_height: 300
---

Agent Plus used to be the centre of this collection. SSH Plus supplied hosts,
Tmux Plus supplied terminal sessions, and Agent Plus used that foundation to
provide agent-session control. The relationship between the launchers and their
backends was comparatively easy to draw.

Native agent runtimes changed the useful boundary. A continuing Codex
conversation belongs to its owning daemon. Terminal clients can come and go;
their presence is not the conversation's lifetime. Native managers also became
the useful place to switch between conversations and control work.

That left a practical design question: what should the surrounding tools own?

## Let native managers own conversations

Agent Plus became a smaller convenience tool. It discovers Codex and Claude
environments, opens native TUIs on the right host and focuses the exact windows
it owns. Conversations, authentication, work and runtime management stay with
the native tools.

This reduced its dependencies. Agent Plus uses the public Host Mesh interface
for routes and its own host helper for entry. It no longer needs Observer
conversation state or a tmux layer. Its environment/window inventory answers
a different question from a conversation monitor.

Tmux remains useful independently: browse a shell session, attach to useful
context, or use explicit guarded actions. Tmux Observer and Tmux Plus retain
those workflows. They no longer define the agent runtime model.

## Observation became more useful on its own

Agent Observer shifted toward read-only Codex facts: identity, runtime/activity,
coverage and freshness. Those facts are useful well beyond a launcher.

The [RLCD agent dashboard](https://github.com/byebyebryan/esp32-rlcd/tree/main/projects/agent-dashboard)
is a concrete consumer. It chooses what belongs on a desk display while Observer
owns native semantics and Mesh owns remote delivery. A diagnostic CLI or another
utility can consume the same public boundaries without adopting that display.

Current Observer support concentrates on Codex. Claude native entry remains
available in Agent Plus, independently of retired Claude observation. Opening
a TUI and interpreting background conversation state have different requirements.

Observer writes and standalone active-only delivery are now retired. Working-set
reads cover admitted active membership plus recent context, while full diagnostics
retain their own route. Native tools own conversation actions.

## The relationships are no longer a ladder

| Project | Current responsibility |
| --- | --- |
| Agent Observer | Read-only Codex observations for dashboards and utilities |
| Mesh Plus | Host authority and bounded cached-state delivery |
| SSH Plus | SSH picker and public Host Mesh interface |
| Agent Plus | Native TUI discovery, launch and window focus |
| Tmux Observer | Generic tmux facts, prepared views and separate action clients |
| Tmux Plus | Tmux browsing and explicit user intent |

Mesh and SSH remain a reusable multi-host backbone. Observer's local core stays
independent of networking. The launchers have their own purposes and interfaces.
Grouping them as frontend/backend pairs would hide these differences.

## One presentation home, independent projects

[Fleet Plus](https://dev.byebyebryan.com/fleet-plus/) gives the collection a shared
overview and direct product pages. Agent Observer gets the strongest showcase
because it now enables the most interesting utilities. Each other tool remains
an independent entry point.

The six source repositories remain separate. A shared site addresses the immediate
documentation and discovery problem. A monorepo could help atomic changes across
projects, but it would also bring migration and release coordination work. That
decision should follow recurring development friction, rather than the old
dependency diagram.

The [architecture guide](https://dev.byebyebryan.com/fleet-plus/architecture/)
shows the current boundaries. The [dated compatibility guide](https://dev.byebyebryan.com/fleet-plus/compatibility/)
links to the October 23 public-delivery checkpoint; it keeps source, release,
installed roles and consumer acceptance distinct.
