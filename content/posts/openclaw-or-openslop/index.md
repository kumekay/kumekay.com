---
title: "OpenClaw or OpenSlop"
date: 2026-02-03 18:36:54
draft: false
slug: "openclaw-or-openslop"
tags: []
author: "Sergei Silnov"
image: "openmess.jpg"
---

If you are a software developer in early 2026, you have probably heard of [OpenClaw](https://openclaw.ai) (known as ClawdBot or MoltBot just a few weeks ago).

So, what exactly is OpenClaw? It’s an agentic system that you can deploy on any of your machines. If you are using a Mac, it provides a helper app with a graphical interface that gives the agent access to your entire machine.

It comes with a zillion integrations and, notably, it can be easily connected to all popular chat applications—both personal (like WhatsApp and Telegram) and corporate (like Microsoft Teams and Mattermost).

It is a "nerdy" app (you have to use the terminal to install it) with the highest rate of adoption I’ve ever seen. I have never seen any other project gain more than 100k GitHub stars in a single week. (Last week it was at 50,000; right now, it has over 150,000).

There is a reason for this: it works surprisingly well. It solves problems. It can do things no other product can, and you only need a few minutes to install and configure it.

<!--more-->

Of course, I tried it myself. I deployed it on one of my unused computers. And wow, it works. It knows you. It has memory. It has its own personality. But it also has "hands" to actually help you—for example, it organized my [Obsidian](https://obsidian.md) notes and medical records. This is why I genuinely like it.

But at the same time, I **hate** it. I want to remove it and never open it again. Let me explain.

It is a piece of "slopware"—it has so many features, but all of them are half-baked. Unfortunately, this approach to building software is not sustainable.

## Security

First, it comes with zero security. It makes it super easy to allow the agent to automatically download "skills" or other documents. These are added to the context and interpreted as instructions by the same LLM that has access to your computer and private data (including tokens and credentials), which can then be sent to attackers. These three factors are dangerous when combined—a combination commonly known as the [lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/).

There is also an innovative related project called [Moltbook](https://moltbook.com), which is essentially a social network for agents. The interface resembles Reddit, but the idea is that only agents should post there. To add a skill, you **just** give your agent a link with the instruction: "Download this link and follow the instructions." The agent does the rest. It installs the skill and creates a scheduled job to check the markdown file from the site every four hours and execute it.

Think about that: you have a computer running an LLM agent that executes a markdown file written by someone else on a platform with no security audit. By default, it downloads and executes these instructions through a health-check mechanism from a site completely populated by agents. What could go wrong? It didn't take long for it to be [discovered](https://www.wiz.io/blog/exposed-moltbook-database-reveals-millions-of-api-keys) that the Moltbook database was unprotected, leaving all data publicly accessible for both reading and writing.

To me, this is just the first finding of its kind. My prediction is that in 2026, there will be an incident caused by prompt injection that will cost a company at least $100,000,000.

I truly believe that agents like this will arise and become super useful. There are security approaches, like [CaMeL](https://arxiv.org/abs/2503.18813), which can help protect private data and build secure systems. But there are not many implementations of these patterns yet. Until then, it’s just a ticking time bomb.

## Quality

In general, the code quality is a black box. The project has almost [9,000 commits](https://github.com/openclaw/openclaw/commits/main/) and a volume of code that is incomprehensible to a small group of people. The author himself admits he doesn't read most of the code, completely trusting agents to write it.

It has thousands of open pull requests on GitHub, but there are only a handful of people—and genuinely just one main contributor—who actively maintain the project. This has long-term consequences for the integrity of the project: how well it's designed, and how many features are left incomplete, unfinished, or duplicated.

Of course, this isn't unheard of in software developed by humans. But when a human is responsible for a particular part of a large application, there is a chance the issue will be fixed. Here, it’s just a mess, and perhaps only future generations of agents will be able to do something about it.

## Efficiency

If you add your paid API token for a decent model, be ready to pay $10–$20 a day even for light use. It bloats its context very quickly and burns millions of tokens just to say, "Hi Sergei, how are you doing today?". And it's more than possible to [spend $200](https://theagilevc.substack.com/p/i-used-clawdbot-openclaw-for-6-hours) in a single day. I believe it can be done in a fraction of this, if prompt optimization was better thought.

## Final Thoughts

I don't want to sound like I'm saying we should stop using agents for code generation. But it is important to understand their current limitations and not push them too far into production systems yet. It will be painful.

It's time to stop blindly giving private data and tools to agents and put more effort into finding sane ways to use them.

OpenClaw is a great project. It sets the frontier by showing what is possible. Just don't use it right now. Maybe you can build your own alternative with just one percent of the features—but ones that you actually use and understand.
