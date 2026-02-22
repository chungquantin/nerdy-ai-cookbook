---
created: 2026-02-22
updated: 2026-02-22
tags: [supercomputing, knowledge, beginner]
domain: supercomputing
status: active
source_url: "https://docs.nvidia.com/dgx/dgxa100-user-guide/introduction-to-dgxa100.html"
kind: topic
---

# GPU Cluster Architecture

## Source
Original Source: [https://docs.nvidia.com/dgx/dgxa100-user-guide/introduction-to-dgxa100.html](https://docs.nvidia.com/dgx/dgxa100-user-guide/introduction-to-dgxa100.html)
Captured on 2026-02-22.

## Abstract
The NVIDIA DGX™ A100 System is the universal system purpose-built for all AI infrastructure and workloads, from analytics to training to inference. The system is built on eight NVIDIA A100 Tensor Core GPUs. This dossier treats the material as a beginner-level knowledge and cross-checks it against corroborating sources.

## Context and Problem Framing
The source frames the problem around Introduction to the NVIDIA DGX A100 System#, Hardware Overview#, DGX A100 Models and Component Descriptions#, Mechanical Specifications#. The system is built on eight NVIDIA A100 Tensor Core GPUs. This document is for users and administrators of the DGX A100 system.

## Technical Approach
The synthesis compares claims across the primary source and additional references, then normalizes them into a systems-level narrative. This section provides information about the hardware in DGX A100. There are two models of the NVIDIA DGX A100 system: the NVIDIA DGX A100 640GB system and the NVIDIA DGX A100 320GB system. Second generation (2x faster than first generation)

## Main Findings
The NVIDIA DGX™ A100 System is the universal system purpose-built for all AI infrastructure and workloads, from analytics to training to inference. The system is built on eight NVIDIA A100 Tensor Core GPUs. This document is for users and administrators of the DGX A100 system. NVIDIA ConnectX-6 or ConnectX-7 IB/200 Gb/s Ethernet (Optional Add-on: Second dual- port 200 Gb/s Ethernet)

## Critical Analysis
1.92 TB NVMe M.2 SSD (ea) in RAID 1 array NVIDIA ConnectX-6 or ConnectX-7 Single Port InfiniBand (default): Up to 200Gbps Conflicting assumptions across sources should be resolved through targeted experiments before production adoption.

## Application to This Cookbook
In this cookbook, this dossier should be connected to [[04_Supercomputing/Supercomputing Index]], [[01_MOCs/Supercomputing MOC]], and [[04_Supercomputing/04_Knowledge/Knowledge Index]]. Use this note as a foundation for implementation logs, benchmark deltas, and architecture decisions.

## Graph Connections
- [[04_Supercomputing/Supercomputing Index]]
- [[01_MOCs/Supercomputing MOC]]
- [[04_Supercomputing/04_Knowledge/Knowledge Index]]

## Bibliography
- [Introduction to the NVIDIA DGX A100 System — NVIDIA DGX A100 User Guide](https://docs.nvidia.com/dgx/dgxa100-user-guide/introduction-to-dgxa100.html)
- [NVIDIA Collective Communication Library (NCCL) Documentation — NCCL 2.29.1 documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/index.html)
- [InfiniBand Trade Association](https://www.infinibandta.org/)

## Research Notes
Record implementation evidence, benchmark outcomes, disagreements between sources, and open questions for follow-up.