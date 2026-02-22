---
created: 2026-02-22
updated: 2026-02-22
tags: [agents, knowledge, advanced]
domain: agents
status: active
source_url: "https://arxiv.org/abs/2308.03688"
kind: topic
---

# Agent Evaluation

## Source
Original Source: [https://arxiv.org/abs/2308.03688](https://arxiv.org/abs/2308.03688)
Captured on 2026-02-22.

## Abstract
The potential of Large Language Model (LLM) as agents has been widely acknowledged recently. Thus, there is an urgent need to quantitatively \textit{evaluate LLMs as agents} on challenging tasks in interactive environments. We present AgentBench, a multi-dimensional benchmark that consists of 8 distinct environments to assess LLM-as-Agent's reasoning and decision-making abilities. Our extensive test over \num API-based and open-sourced (OSS) LLMs shows that, while top commercial LLMs present a strong ability of acting as agents in complex environments, there is a significant disparity in performance between them and many OSS competitors that are no larger than 70B. We identify the typical reasons of failures in environments and LLMs, showing that poor long-term reasoning, decision-making, and instruction following abilities are the main obstacles for developing usable LLM agents. Improving instruction following and training on high quality multi-round alignment data could improve agent performance. And different from existing assumptions, training on code present ambivalent impacts on different agent tasks. Datasets, environments, and an integrated evaluation package for AgentBench are released at https://github.com/THUDM/AgentBench. This dossier treats the material as an advanced-level knowledge and cross-checks it against corroborating sources.

## Context and Problem Framing
The source frames the problem around Computer Science > Artificial Intelligence, Title:AgentBench: Evaluating LLMs as Agents, Access Paper:, References & Citations. Thus, there is an urgent need to quantitatively \textit{evaluate LLMs as agents} on challenging tasks in interactive environments. We present AgentBench, a multi-dimensional benchmark that consists of 8 distinct environments to assess LLM-as-Agent's reasoning and decision-making abilities.

## Technical Approach
The synthesis compares claims across the primary source and additional references, then normalizes them into a systems-level narrative. Our extensive test over \num API-based and open-sourced (OSS) LLMs shows that, while top commercial LLMs present a strong ability of acting as agents in complex environments, there is a significant disparity in performance between them and many OSS competitors that are no larger than 70B. We identify the typical reasons of failures in environments and LLMs, showing that poor long-term reasoning, decision-making, and instruction following abilities are the main obstacles for developing usable LLM agents. Improving instruction following and training on high quality multi-round alignment data could improve agent performance.

## Main Findings
The potential of Large Language Model (LLM) as agents has been widely acknowledged recently. Thus, there is an urgent need to quantitatively \textit{evaluate LLMs as agents} on challenging tasks in interactive environments. We present AgentBench, a multi-dimensional benchmark that consists of 8 distinct environments to assess LLM-as-Agent's reasoning and decision-making abilities. And different from existing assumptions, training on code present ambivalent impacts on different agent tasks. Datasets, environments, and an integrated evaluation package for AgentBench are released at https://github.com/THUDM/AgentBench.

## Critical Analysis
Some claims are context-sensitive and may not transfer directly without environment-specific benchmarking. Conflicting assumptions across sources should be resolved through targeted experiments before production adoption.

## Application to This Cookbook
In this cookbook, this dossier should be connected to [[02_Agents/Agents Index]], [[01_MOCs/Agents MOC]], and [[02_Agents/06_Knowledge/Knowledge Index]]. Use this note as a foundation for implementation logs, benchmark deltas, and architecture decisions.

## Graph Connections
- [[02_Agents/Agents Index]]
- [[01_MOCs/Agents MOC]]
- [[02_Agents/06_Knowledge/Knowledge Index]]

## Bibliography
- [AgentBench: Evaluating LLMs as Agents](https://arxiv.org/abs/2308.03688)
- [SWE-bench Leaderboards](https://www.swebench.com/)
- [GAIA: a benchmark for General AI Assistants](https://arxiv.org/abs/2311.12983)

## Research Notes
Record implementation evidence, benchmark outcomes, disagreements between sources, and open questions for follow-up.