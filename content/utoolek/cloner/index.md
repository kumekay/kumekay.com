---
title: "cloner"
github: "https://github.com/kumekay/cloner"
tags: ["cli", "git", "python"]
date: 2026-02-15
---

I just want to keep some structure of the repositories I check out locally.
So it just does this. Clones GitHub repos to worspace/[owner]/[repo] and other sources (i.e. GitLab) to prefixed with service name.
And then changes directory to the cloned repo. It is a simple wrapper around `git clone` with some path management.

<!--more-->

## Installation

```bash
uv tool install git+https://github.com/kumekay/cloner.git
```

## Usage

```bash
cloner https://github.com/user/repo
```
