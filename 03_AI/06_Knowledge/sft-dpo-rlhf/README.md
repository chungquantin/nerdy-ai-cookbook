---
created: 2026-02-22
updated: 2026-02-22
tags: [ai, knowledge, advanced]
domain: ai
status: active
source_url: "https://arxiv.org/abs/2203.02155"
kind: topic
---

# SFT DPO RLHF

## Source
Original Source: [https://arxiv.org/abs/2203.02155](https://arxiv.org/abs/2203.02155)
Captured on 2026-02-22.

## Abstract
Making language models bigger does not inherently make them better at following a user's intent. For example, large language models can generate outputs that are untruthful, toxic, or simply not helpful to the user. In other words, these models are not aligned with their users. In this paper, we show an avenue for aligning language models with user intent on a wide range of tasks by fine-tuning with human feedback. Starting with a set of labeler-written prompts and prompts submitted through the OpenAI API, we collect a dataset of labeler demonstrations of the desired model behavior, which we use to fine-tune GPT-3 using supervised learning. We then collect a dataset of rankings of model outputs, which we use to further fine-tune this supervised model using reinforcement learning from human feedback. We call the resulting models InstructGPT. In human evaluations on our prompt distribution, outputs from the 1.3B parameter InstructGPT model are preferred to outputs from the 175B GPT-3, despite having 100x fewer parameters. Moreover, InstructGPT models show improvements in truthfulness and reductions in toxic output generation while having minimal performance regressions on public NLP datasets. Even though InstructGPT still makes simple mistakes, our results show that fine-tuning with human feedback is a promising direction for aligning language models with human intent. This dossier treats the material as an advanced-level knowledge and cross-checks it against corroborating sources.

## Context and Problem Framing
The source frames the problem around Computer Science > Computation and Language, Title:Training language models to follow instructions with human feedback, Access Paper:, References & Citations. For example, large language models can generate outputs that are untruthful, toxic, or simply not helpful to the user. In other words, these models are not aligned with their users.

## Technical Approach
The synthesis compares claims across the primary source and additional references, then normalizes them into a systems-level narrative. In this paper, we show an avenue for aligning language models with user intent on a wide range of tasks by fine-tuning with human feedback. Starting with a set of labeler-written prompts and prompts submitted through the OpenAI API, we collect a dataset of labeler demonstrations of the desired model behavior, which we use to fine-tune GPT-3 using supervised learning. We call the resulting models InstructGPT.

## Main Findings
Making language models bigger does not inherently make them better at following a user's intent. For example, large language models can generate outputs that are untruthful, toxic, or simply not helpful to the user. In other words, these models are not aligned with their users. In human evaluations on our prompt distribution, outputs from the 1.3B parameter InstructGPT model are preferred to outputs from the 175B GPT-3, despite having 100x fewer parameters. Moreover, InstructGPT models show improvements in truthfulness and reductions in toxic output generation while having minimal performance regressions on public NLP datasets.

## Critical Analysis
Even though InstructGPT still makes simple mistakes, our results show that fine-tuning with human feedback is a promising direction for aligning language models with human intent. Conflicting assumptions across sources should be resolved through targeted experiments before production adoption.

## Application to This Cookbook
In this cookbook, this dossier should be connected to [[03_AI/AI Index]], [[01_MOCs/AI MOC]], and [[03_AI/06_Knowledge/Knowledge Index]]. Use this note as a foundation for implementation logs, benchmark deltas, and architecture decisions.

## Graph Connections
- [[03_AI/AI Index]]
- [[01_MOCs/AI MOC]]
- [[03_AI/06_Knowledge/Knowledge Index]]

## Bibliography
- [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155)
- [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290)
- [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073)

## Research Notes
Record implementation evidence, benchmark outcomes, disagreements between sources, and open questions for follow-up.