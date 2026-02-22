---
created: 2026-02-22
updated: 2026-02-22
tags: [ai, knowledge, intermediate]
domain: ai
status: active
source_url: "https://arxiv.org/abs/2005.11401"
kind: topic
---

# RAG Basics

## Source
Original Source: [https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)
Captured on 2026-02-22.

## Abstract
Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit non-parametric memory can overcome this issue, but have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) -- models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, the other can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline. This dossier treats the material as an intermediate-level knowledge and cross-checks it against corroborating sources.

## Context and Problem Framing
The source frames the problem around Computer Science > Computation and Language, Title:Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, Access Paper:, References & Citations. The central challenge is balancing capability, reliability, and cost under real operating constraints.

## Technical Approach
The synthesis compares claims across the primary source and additional references, then normalizes them into a systems-level narrative. Methodologically, the source progresses from conceptual framing to implementation-oriented guidance.

## Main Findings
The main findings emphasize concrete design patterns and measurable engineering tradeoffs. Across sources, the strongest consensus concerns explicit tradeoffs between scalability, control, and safety.

## Critical Analysis
Some claims are context-sensitive and may not transfer directly without environment-specific benchmarking. Conflicting assumptions across sources should be resolved through targeted experiments before production adoption.

## Application to This Cookbook
In this cookbook, this dossier should be connected to [[03_AI/AI Index]], [[01_MOCs/AI MOC]], and [[03_AI/06_Knowledge/Knowledge Index]]. Use this note as a foundation for implementation logs, benchmark deltas, and architecture decisions.

## Graph Connections
- [[03_AI/AI Index]]
- [[01_MOCs/AI MOC]]
- [[03_AI/06_Knowledge/Knowledge Index]]

## Bibliography
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)
- [LangChain overview - Docs by LangChain](https://python.langchain.com/docs/concepts/rag/)
- [Introduction to RAG | LlamaIndex Python Documentation](https://docs.llamaindex.ai/en/stable/understanding/rag/)

## Research Notes
Record implementation evidence, benchmark outcomes, disagreements between sources, and open questions for follow-up.