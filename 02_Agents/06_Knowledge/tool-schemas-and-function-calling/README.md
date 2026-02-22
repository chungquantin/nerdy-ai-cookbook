---
created: 2026-02-22
updated: 2026-02-22
tags: [agents, knowledge, intermediate]
domain: agents
status: active
source_url: "https://platform.openai.com/docs/guides/function-calling"
kind: topic
---

# Tool Schemas and Function Calling

## Source
Original Source: [https://platform.openai.com/docs/guides/function-calling](https://platform.openai.com/docs/guides/function-calling)
Captured on 2026-02-22.

## Abstract
Learn how function calling enables large language models to connect to external data and systems. This dossier treats the material as an intermediate-level knowledge and cross-checks it against corroborating sources.

## Context and Problem Framing
The source frames the problem around Get started, Core concepts, Agents, Tools. Give models access to new functionality and data they can use to follow instructions and respond to prompts. Function calling (also known as tool calling) provides a powerful and flexible way for OpenAI models to interface with external systems and access data outside their training data.

## Technical Approach
The synthesis compares claims across the primary source and additional references, then normalizes them into a systems-level narrative. This guide shows how you can connect a model to data and actions provided by your application. We’ll show how to use function tools (defined by a JSON schema) and custom tools which work with free form text inputs and outputs. Let’s begin by understanding a few key terms about tool calling.

## Main Findings
Learn how function calling enables large language models to connect to external data and systems. Give models access to new functionality and data they can use to follow instructions and respond to prompts. Function calling (also known as tool calling) provides a powerful and flexible way for OpenAI models to interface with external systems and access data outside their training data. After we have a shared vocabulary for tool calling, we’ll show you how it’s done with some practical examples. A function or tool refers in the abstract to a piece of functionality that we tell the model it has access to.

## Critical Analysis
As a model generates a response to a prompt, it may decide that it needs data or functionality provided by a tool to follow the prompt’s instructions. Or anything else you’d like the model to be able to know or do as it responds to a prompt. Conflicting assumptions across sources should be resolved through targeted experiments before production adoption.

## Application to This Cookbook
In this cookbook, this dossier should be connected to [[02_Agents/Agents Index]], [[01_MOCs/Agents MOC]], and [[02_Agents/06_Knowledge/Knowledge Index]]. Use this note as a foundation for implementation logs, benchmark deltas, and architecture decisions.

## Graph Connections
- [[02_Agents/Agents Index]]
- [[01_MOCs/Agents MOC]]
- [[02_Agents/06_Knowledge/Knowledge Index]]

## Bibliography
- [Function calling | OpenAI API](https://platform.openai.com/docs/guides/function-calling)
- [Creating your first schema](https://json-schema.org/learn/getting-started-step-by-step)
- [Tool use with Claude - Claude API Docs](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview)

## Research Notes
Record implementation evidence, benchmark outcomes, disagreements between sources, and open questions for follow-up.