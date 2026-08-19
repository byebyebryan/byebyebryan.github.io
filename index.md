---
layout: home
title: ByeByeBryan
lede: Building native tools, games, graphics experiments, and agent infrastructure.
eyebrow: dev.byebyebryan.com
sections:
  - title: Games, graphics, and simulation
    projects:
      - name: Gomoku2D
        description: A local-first browser Gomoku and Renju game with a Rust and WebAssembly rules core, configurable bots, tactical hints, and replay analysis.
        url: https://github.com/byebyebryan/gomoku2d
        image: /assets/projects/gomoku2d.gif
        image_alt: Gomoku2D local match in progress on a pixel-art board.
        links:
          - label: play
            url: https://gomoku2d.byebyebryan.com/
      - name: Cubey
        description: A native C++ and Vulkan GPU workbench for procedural graphics, simulation, and rendering experiments.
        url: https://github.com/byebyebryan/cubey
      - name: Raster 90
        description: A bitmap-first Wear OS 5 watch face for the OnePlus Watch 3, built from deterministic cell-matrix graphics with a fictional-hardware aesthetic.
        url: https://github.com/byebyebryan/wear-os
      - name: Powered Descent Lab
        description: A native-first lab for deterministic rocket flight, controller development, scenario design, evaluation, and replay analysis.
        url: https://github.com/byebyebryan/powered-descent-lab
  - title: Agent tools
    projects:
      - name: Workstream Navigator
        description: A native-workflow terminal navigator for persistent Codex and OpenCode workstreams across local and SSH hosts.
        url: https://github.com/byebyebryan/workstream-navigator
      - name: Agent Bookkeeper
        description: A reusable archive, transport, catalog, and provenance-aware search system for agent-session evidence.
        url: https://github.com/byebyebryan/agent-bookkeeper
      - name: DMS Agent Picker
        description: A DankMaterialShell launcher for resuming Codex, Claude Code, and OpenCode sessions across local and SSH hosts.
        url: https://github.com/byebyebryan/dms-agent-picker
  - title: Desktop and developer tools
    projects:
      - name: remote-chrome
        description: Launch Chrome on a remote Linux host over Waypipe, with optional YubiKey forwarding for WebAuthn prompts.
        url: https://github.com/byebyebryan/remote-chrome
      - name: lazy-serializable
        description: Header-only C++ serialization that declares fields once and supports JSON, binary, YAML, TOML, and more without code generation.
        url: https://github.com/byebyebryan/lazy-serializable
      - name: DMS Power Status
        description: An adaptive battery and power widget with live wattage, charge-aware ETA, a 24-hour history chart, and session statistics.
        url: https://github.com/byebyebryan/dms-power-status
      - name: DMS SSH Plus
        description: A DankMaterialShell SSH launcher that remembers successful hosts and can keep sessions alive across DMS restarts.
        url: https://github.com/byebyebryan/dms-ssh-plus
---
