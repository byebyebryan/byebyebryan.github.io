---
title: Read-only agent state across machines
description: Following a Codex observation from its native runtime to a utility, without turning a cached connection into fresh evidence.
categories: [tools]
social_image: /assets/projects/rlcd-roster.png
social_image_alt: Production dashboard renderer with fictional conversations; not physical footage.
social_image_width: 400
social_image_height: 300
---

A useful dashboard needs more than a list of conversations. It needs to know
where an observation came from, which identity it describes, whether coverage is
complete, and how long the underlying evidence remains useful.

[Agent Observer](https://dev.byebyebryan.com/fleet-plus/projects/agent-observer/)
provides that read-only foundation. The path from runtime to display has three
separate owners: Observer produces native facts, optional Mesh delivers cached
state, and a utility decides how to present it.

## Start at the owning runtime

Codex's owning daemon supplies runtime evidence. A terminal window or tmux pane
can show a client, but that alone cannot establish whether a conversation is
working, waiting, parked or gone.

Observer keeps saved history, logical session identity, runtime workers and
terminal attachment distinct. Consumers should use the public identities and
qualified fields rather than reconstructing state from titles, paths or PIDs.
Native managers retain conversation control.

For local use, a utility can consume a cached service hosted separately from
the reader. Mesh is optional. Reading does not start a missing native daemon or
silently turn a utility into a collector.

## Add delivery without changing the facts

For remote use, Mesh carries already published observations over explicitly
configured routes. The receiver gets delivery provenance and validity alongside
the producer's independently qualified evidence.

A healthy connection is useful information, but it does not make an old native
observation new. Heartbeats and copied views cannot renew the underlying work
state. Consumers need to preserve both kinds of freshness.

The [interactive read-path explanation](https://dev.byebyebryan.com/fleet-plus/projects/agent-observer/#follow-an-observation)
illustrates local reads, fleet delivery and partial evidence. It uses authored
examples and does not contact a runtime.

## A working set is not the whole saved inventory

The working-set path supplies admitted active membership and recent context;
the reviewed default recent window is 72 hours. Membership and scope coverage
have their own leases. Full diagnostic reads remain independently available.

An omitted row is ambiguous when membership is incomplete. A source that has
expired is unavailable, rather than proof that no work exists. Utilities should
show those conditions explicitly instead of converting them into idle or empty.

That distinction matters in real acceptance, too. The October 23 delivery
checkpoint retained an unresolved partial working-set membership result on one
host despite a ready full cached service. It did not establish a complete-empty
roster or identify a deployment regression. The [compatibility record](https://dev.byebyebryan.com/fleet-plus/compatibility/#known-bounds)
keeps that limit visible.

## Routes stay directional

Suppose Desk can read Tower and Laptop, while Tower and Laptop can read each
other. Neither peer has a route back to Desk. That is an intentional topology.

A machine appearing as a reader somewhere else does not grant reverse access.
Cached discovery also has to respect each endpoint's configured membership.
[The routing illustration](https://dev.byebyebryan.com/fleet-plus/architecture/#directional-host-access)
shows the three views using fictional host names.

## Turn the observations into something useful

![Production RLCD dashboard renderer showing fictional conversations and activity states]({{ '/assets/projects/rlcd-roster.png' | relative_url }})

*Production C renderer with fictional conversations and virtual time; this is a
UI preview, not physical panel footage. [Source and media provenance](https://github.com/byebyebryan/byebyebryan.github.io/blob/main/assets/projects/manifest.json).*

The RLCD dashboard is one consumer. Its row selection, labels, device transport
and physical readability belong to that project. Another utility might choose
a compact status summary or diagnostics, using the same read-only foundation.

The [bounded utility example](https://github.com/byebyebryan/agent-observer/blob/main/docs/utility-read-guide.md)
is a starting point for developers. It uses public local/Mesh interfaces, explicit
identity and endpoint inputs, bounded execution, and a content-free summary.
It keeps uncertainty and expiry visible instead of replacing them with guesses.
