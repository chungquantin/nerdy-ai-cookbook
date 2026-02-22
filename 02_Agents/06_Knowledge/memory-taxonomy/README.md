---
created: 2026-02-22
updated: 2026-02-22
tags: [agents, knowledge, intermediate]
domain: agents
status: active
source_url: "https://arxiv.org/abs/2310.08560"
kind: topic
---

# Memory Taxonomy

## Source
Original Source: [https://arxiv.org/abs/2310.08560](https://arxiv.org/abs/2310.08560)
Captured on 2026-02-22.

## Abstract
Large language models (LLMs) have revolutionized AI, but are constrained by limited context windows, hindering their utility in tasks like extended conversations and document analysis. To enable using context beyond limited context windows, we propose virtual context management, a technique drawing inspiration from hierarchical memory systems in traditional operating systems that provide the appearance of large memory resources through data movement between fast and slow memory. Using this technique, we introduce MemGPT (Memory-GPT), a system that intelligently manages different memory tiers in order to effectively provide extended context within the LLM's limited context window, and utilizes interrupts to manage control flow between itself and the user. We evaluate our OS-inspired design in two domains where the limited context windows of modern LLMs severely handicaps their performance: document analysis, where MemGPT is able to analyze large documents that far exceed the underlying LLM's context window, and multi-session chat, where MemGPT can create conversational agents that remember, reflect, and evolve dynamically through long-term interactions with their users. We release MemGPT code and data for our experiments at https://memgpt.ai. This dossier treats the material as an intermediate-level knowledge and cross-checks it against corroborating sources.

## Context and Problem Framing
The source frames the problem around Computer Science > Artificial Intelligence, Title:MemGPT: Towards LLMs as Operating Systems, Access Paper:, References & Citations. The central challenge is balancing capability, reliability, and cost under real operating constraints.

## Technical Approach
The synthesis compares claims across the primary source and additional references, then normalizes them into a systems-level narrative. Methodologically, the source progresses from conceptual framing to implementation-oriented guidance.

## Main Findings
The main findings emphasize concrete design patterns and measurable engineering tradeoffs. Across sources, the strongest consensus concerns explicit tradeoffs between scalability, control, and safety.

## Critical Analysis
Some claims are context-sensitive and may not transfer directly without environment-specific benchmarking. Conflicting assumptions across sources should be resolved through targeted experiments before production adoption.

## Application to This Cookbook
In this cookbook, this dossier should be connected to [[02_Agents/Agents Index]], [[01_MOCs/Agents MOC]], and [[02_Agents/06_Knowledge/Knowledge Index]]. Use this note as a foundation for implementation logs, benchmark deltas, and architecture decisions.

## Graph Connections
- [[02_Agents/Agents Index]]
- [[01_MOCs/Agents MOC]]
- [[02_Agents/06_Knowledge/Knowledge Index]]

## Bibliography
- [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560)
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)
- [Redirecting...](https://langchain-ai.github.io/langgraph/concepts/memory/)

## Research Notes
Record implementation evidence, benchmark outcomes, disagreements between sources, and open questions for follow-up.