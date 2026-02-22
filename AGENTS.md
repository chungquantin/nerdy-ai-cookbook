# AGENTS.md

Guidelines for humans and coding agents contributing to this cookbook.

## Goal

Keep this vault clean, link-rich, and graph-friendly so new knowledge is easy to revisit and connect.

## Rules for New Notes

1. Use one topic per note.
2. Include frontmatter (`created`, `updated`, `tags`, `domain`, `status`).
3. Add at least one outgoing `[[wikilink]]`.
4. Add the note to at least one MOC in `01_MOCs`.
5. If the note comes from a source, include a short source section.

## Note Structure (Default)

```md
# Title

## Summary

## Key Ideas

## Connections
- [[Related Note]]

## Sources
- URL / paper / talk

## Next Questions
```

## Naming

- Use concise, human-readable names.
- Prefer title case for permanent notes.
- Keep path placement consistent by domain.

## Domain Mapping

- Agents -> `02_Agents`
- AI -> `03_AI`
- Supercomputing -> `04_Supercomputing`
- Ongoing implementations -> `05_Projects`

## Agent Skills Notes

For agent skills, place notes in `02_Agents/Skills` and use the skill template in `99_Templates/Agent Skill Template.md`.

## URL Ingestion Skill

When a user provides a source URL, use:

`python scripts/add_knowledge_from_url.py "<URL>"`

Expected behavior:
1. Auto-classify into `agents`, `ai`, `supercomputing`, or `projects`.
2. Create/update a README-style note under that group's knowledge folder.
3. Write the resource README as a deep research-style article in prose paragraphs (not bullet-only summaries).
4. Include the original source as a markdown link in the note.
5. Upsert a checklist entry into that group's `Knowledge Index.md`.
