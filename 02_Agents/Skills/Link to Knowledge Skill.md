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
- Create `<group>/.../Knowledge/<slug>/README.md`.
- Append checklist entry to that group's `Knowledge Index.md`.

## Connections
- [[Agents Index]]
- [[Skills Index]]

