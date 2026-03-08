---
title: "monitoradlo"
slug: "monitoradlo"
github: "https://github.com/kumekay/monitoradlo"
tags: ["gui", "linux", "wayland", "go"]
date: 2026-03-05
image: "monitoradlo.png"
---

I'm using Niri as my Wayland compositor, and Kanshi to manage monitor layouts. However, editing Kanshi's config files by handis annoying (though I like to practice mental math a bit).

I wanted a more visual way to manage my monitor profiles.
A GUI application for editing Kanshi monitor layout profiles with live preview via Niri IPC.

Drag monitors on an canvas, edit properties, save to your kanshi config, and preview changes live on your displays — all from a single binary.

It's agentically engineered in Go with Wails (I like it!) and works fine for me, but for sure not all corner cases are covered. If you happen to use Niri with Kanshi, decided to try it out - ping me on GitHub if you have any issues or suggestions.

<!--more-->

## Install

```bash
sudo pacman -S webkit2gtk-4.1 go
go install github.com/wailsapp/wails/v2/cmd/wails@latest

git clone https://github.com/kumekay/monitoradlo.git
cd monitoradlo
wails build -tags webkit2_41
cp build/bin/monitoradlo ~/.local/bin/
cp monitoradlo.desktop ~/.local/share/applications/
```

## Requirements

- [Niri](https://github.com/YaLTeR/niri) compositor
- [Kanshi](https://sr.ht/~emersion/kanshi/)
- `webkit2gtk-4.1`
