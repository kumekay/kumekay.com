---
title: "Vibetenance Mode: Maintaining Legacy Services with AI Agents"
date: 2026-01-28 22:59:09
draft: false
slug: "vibetenance-mode-maintaining-legacy-services-with-ai-agents"
tags: []
author: "Sergei Silnov"
image: "image-1-1.jpg"
---

This article can be summarized as: if there's a legacy service no one wants to maintain, doing it with an agent is a better option.

If you've used coding agents for some time, you already know what to do, and this note is only about introducing one more vibe-word.

But I'll still add a couple of details.

<!--more-->

## The Problem

Every single company I worked for had a number of old web services created at some point. It happened that the original authors were not around anymore.

These services are useful, but they are not mission critical. So they can stay silently functioning for years without anyone ever touching them.

Until decay takes them down. Some call this "maintenance" mode.

I believe that now, when coding agents are everywhere, there is a better alternative: **"vibetenance mode"**.

I suggest making this term known in your company as a shortcut for saying: "We will support it on a best-effort basis using a coding agent."

So you only spend a little effort preparing a project to be vibetained by a coding agent and then just use your Codex/GitHub Copilot/OpenCode for all the fixes and small features.

## How To Prepare Projects?

For small-to-midsize projects, a single `AGENTS.md` file in the root of your project is probably all you need.

Of course, you don't want to write it from scratch on your own.

You can use any agent system (Claude Code, Cursor, GitHub Copilot, OpenCode), but use it with the best model you have. Claude Opus 4.5 or Gemini 2.5 Pro will give you better results.

The prompt can be something like this:

```
Take your time to go through the entire codebase and document all important details of this project in the `AGENTS.md` file.

This project will be maintained by an engineer with medium proficiency and sometimes questionable taste. He also tends to use uncommon practices, but usually follows written guidelines. So, make the instructions in `AGENTS.md` sufficient to follow existing logic, procedures, and coding style. Help him maintain this project as well as possible and describe the onboarding process: how to set up the local development environment, run tests, and linters.

If during this discovery you find some weird details, then write them down to `review_notes.md`. But don't mention them in `AGENTS.md`. Use language clear to a person unfamiliar with the project.
```

You'll have two files to review:

* `AGENTS.md` — maintenance guide for the agent; keep it in the repo
* `review_notes.md` — useful to read; maybe apply some suggestions and throw away the rest

And I would also add a line to the README to make it fair:

```
The project is in 'Vibetenance mode.' Do not add any new features and ask the agent to make the fixes.
```