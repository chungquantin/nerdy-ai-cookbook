---
created: 2026-02-22
updated: 2026-02-22
tags: [agents, skills, automation]
domain: agents
status: active
---

# Link to Knowledge Skill

## Summary
Given a URL, automatically create a README-style knowledge note and file it into the correct track.

## Command
`python scripts/add_knowledge_from_url.py "https://example.com/article"`

## Behavior
- Fetch and parse page title/description/headings.
- Auto-classify group: `agents`, `ai`, `supercomputing`, or `projects`.
- Auto-tag level: `beginner`, `intermediate`, or `advanced`.
- Create or update `<group>/.../Knowledge/<slug>/README.md` (same URL updates existing note).
- Generate a deep research-style README in prose sections (`Abstract`, `Context`, `Technical Approach`, `Main Findings`, `Critical Analysis`, `Application`).
- Always include an explicit original-source markdown link in `## Source`.
- Upsert checklist entry in that group's `Knowledge Index.md`.

## Connections
- [[Agents Index]]
- [[Skills Index]]
