---
created: 2026-02-22
updated: 2026-02-22
tags: [agents, knowledge, advanced]
domain: agents
status: active
source_url: "https://arxiv.org/abs/2302.04761"
kind: topic
---

# Tool Use and API Calling

## Source
Original Source: [https://arxiv.org/abs/2302.04761](https://arxiv.org/abs/2302.04761)
Captured on 2026-02-22.

## Abstract
Language models (LMs) exhibit remarkable abilities to solve new tasks from just a few examples or textual instructions, especially at scale. They also, paradoxically, struggle with basic functionality, such as arithmetic or factual lookup, where much simpler and smaller models excel. In this paper, we show that LMs can teach themselves to use external tools via simple APIs and achieve the best of both worlds. We introduce Toolformer, a model trained to decide which APIs to call, when to call them, what arguments to pass, and how to best incorporate the results into future token prediction. This is done in a self-supervised way, requiring nothing more than a handful of demonstrations for each API. We incorporate a range of tools, including a calculator, a Q\&A system, two different search engines, a translation system, and a calendar. Toolformer achieves substantially improved zero-shot performance across a variety of downstream tasks, often competitive with much larger models, without sacrificing its core language modeling abilities. This dossier treats the material as an advanced-level knowledge and cross-checks it against corroborating sources.

## Context and Problem Framing
The source frames the problem around Happy Open Access Week from arXiv!, Computer Science > Computation and Language, Title:Toolformer: Language Models Can Teach Themselves to Use Tools, Access Paper:. The central challenge is balancing capability, reliability, and cost under real operating constraints.

## Technical Approach
The synthesis compares claims across the primary source and additional references, then normalizes them into a systems-level narrative. Methodologically, the source progresses from conceptual framing to implementation-oriented guidance.

## Main Findings
Tell us why you support #openaccess and give to arXiv this week to help keep science open for all. Across sources, the strongest consensus concerns explicit tradeoffs between scalability, control, and safety.

## Critical Analysis
Some claims are context-sensitive and may not transfer directly without environment-specific benchmarking. Conflicting assumptions across sources should be resolved through targeted experiments before production adoption.

## Application to This Cookbook
In this cookbook, this dossier should be connected to [[02_Agents/Agents Index]], [[01_MOCs/Agents MOC]], and [[02_Agents/06_Knowledge/Knowledge Index]]. Use this note as a foundation for implementation logs, benchmark deltas, and architecture decisions.

## Graph Connections
- [[02_Agents/Agents Index]]
- [[01_MOCs/Agents MOC]]
- [[02_Agents/06_Knowledge/Knowledge Index]]

## Bibliography
- [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761)
- [Function calling | OpenAI API](https://platform.openai.com/docs/guides/function-calling)
- [Tool use with Claude - Claude API Docs](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview)

## Research Notes
Record implementation evidence, benchmark outcomes, disagreements between sources, and open questions for follow-up.