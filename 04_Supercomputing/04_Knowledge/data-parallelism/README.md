---
created: 2026-02-22
updated: 2026-02-22
tags: [supercomputing, knowledge, beginner]
domain: supercomputing
status: active
source_url: "https://pytorch.org/docs/stable/notes/ddp.html"
kind: topic
---

# Data Parallelism

## Source
Original Source: [https://pytorch.org/docs/stable/notes/ddp.html](https://pytorch.org/docs/stable/notes/ddp.html)
Captured on 2026-02-22.

## Abstract
Created On: Jan 15, 2020 | Last Updated On: Jan 25, 2024 The implementation of torch.nn.parallel.DistributedDataParallel evolves over time. This dossier treats the material as a beginner-level knowledge and cross-checks it against corroborating sources.

## Context and Problem Framing
The source frames the problem around Distributed Data Parallel#, Example#, Internal Design#, Implementation#. The implementation of torch.nn.parallel.DistributedDataParallel evolves over time. This design note is written based on the state as of v1.4.

## Technical Approach
The synthesis compares claims across the primary source and additional references, then normalizes them into a systems-level narrative. torch.nn.parallel.DistributedDataParallel (DDP) transparently performs distributed data parallel training. This page describes how it works and reveals implementation details. Let us start with a simple torch.nn.parallel.DistributedDataParallel example.

## Main Findings
Created On: Jan 15, 2020 | Last Updated On: Jan 25, 2024 The implementation of torch.nn.parallel.DistributedDataParallel evolves over time. This design note is written based on the state as of v1.4. This example uses a torch.nn.Linear as the local model, wraps it with DDP, and then runs one forward pass, one backward pass, and an optimizer step on the DDP model. After that, parameters on the local model will be updated, and all models on different processes should be exactly the same.

## Critical Analysis
When used with TorchDynamo, apply the DDP model wrapper before compiling the model, such that torchdynamo can apply DDPOptimizer (graph-break optimizations) based on DDP bucket sizes. (See TorchDynamo DDPOptimizer for more information.) Conflicting assumptions across sources should be resolved through targeted experiments before production adoption.

## Application to This Cookbook
In this cookbook, this dossier should be connected to [[04_Supercomputing/Supercomputing Index]], [[01_MOCs/Supercomputing MOC]], and [[04_Supercomputing/04_Knowledge/Knowledge Index]]. Use this note as a foundation for implementation logs, benchmark deltas, and architecture decisions.

## Graph Connections
- [[04_Supercomputing/Supercomputing Index]]
- [[01_MOCs/Supercomputing MOC]]
- [[04_Supercomputing/04_Knowledge/Knowledge Index]]

## Bibliography
- [Distributed Data Parallel — PyTorch 2.10 documentation](https://pytorch.org/docs/stable/notes/ddp.html)
- [Horovod: fast and easy distributed deep learning in TensorFlow](https://arxiv.org/abs/1802.05799)
- [Seasonal modulation of seismicity: the competing/collaborative effect of the snow and ice load on the lithosphere](https://arxiv.org/abs/1702.06292)

## Research Notes
Record implementation evidence, benchmark outcomes, disagreements between sources, and open questions for follow-up.