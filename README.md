# Nerdy AI Cookbook

A structured AI learning archive inspired by [mlabonne/llm-course](https://github.com/mlabonne/llm-course), built for long-term note growth in Obsidian.

## Purpose

This vault is for continuously learning and organizing knowledge about:
- Agents
- AI/LLMs
- Supercomputing
- Applied projects

## Module Progression Rules

1. Complete all `Beginner` items in a track before starting `Intermediate`.
2. Complete all `Intermediate` items before starting `Advanced`.
3. Mark a checkbox only after you wrote or updated the linked note.
4. Every completed note must have at least one `[[wikilink]]` connection.

## Learning Roadmap (Checklist)

### Agents

Start at [Agents Index](02_Agents/Agents%20Index.md)

#### Beginner
- [x] [Single-Agent vs Multi-Agent](02_Agents/01_Architectures/Single-Agent%20vs%20Multi-Agent.md)
- [x] [System Prompt Design](02_Agents/02_Prompting/System%20Prompt%20Design.md)
- [x] [Prompt Engineering](02_Agents/Skills/Prompt%20Engineering.md)

#### Intermediate
- [x] [Tool Schemas and Function Calling](02_Agents/03_Tooling/Tool%20Schemas%20and%20Function%20Calling.md)
- [x] [Memory Taxonomy](02_Agents/04_Memory/Memory%20Taxonomy.md)
- [x] [Memory and Retrieval](02_Agents/Skills/Memory%20and%20Retrieval.md)
- [x] [Planning and Reflection](02_Agents/Skills/Planning%20and%20Reflection.md)

#### Advanced
- [x] [Agent Evaluation](02_Agents/05_Evaluation/Agent%20Evaluation.md)
- [x] [Tool Use and API Calling](02_Agents/Skills/Tool%20Use%20and%20API%20Calling.md)
- [x] [Link to Knowledge Skill](02_Agents/Skills/Link%20to%20Knowledge%20Skill.md)

### AI / LLMs

Start at [AI Index](03_AI/AI%20Index.md)

#### Beginner
- [x] [Linear Algebra for ML](03_AI/01_Foundations/Linear%20Algebra%20for%20ML.md)
- [x] [Probability and Statistics for ML](03_AI/01_Foundations/Probability%20and%20Statistics%20for%20ML.md)

#### Intermediate
- [x] [Transformer Architecture](03_AI/02_Modeling/Transformer%20Architecture.md)
- [x] [RAG Basics](03_AI/04_RAG/RAG%20Basics.md)

#### Advanced
- [x] [SFT DPO RLHF](03_AI/03_Post-Training/SFT%20DPO%20RLHF.md)
- [x] [LLM Evaluation Metrics](03_AI/05_Evaluation/LLM%20Evaluation%20Metrics.md)

### Supercomputing

Start at [Supercomputing Index](04_Supercomputing/Supercomputing%20Index.md)

#### Beginner
- [x] [GPU Cluster Architecture](04_Supercomputing/01_Infrastructure/GPU%20Cluster%20Architecture.md)
- [x] [Data Parallelism](04_Supercomputing/02_Distributed-Training/Data%20Parallelism.md)

#### Intermediate
- [x] [Tensor and Pipeline Parallelism](04_Supercomputing/02_Distributed-Training/Tensor%20and%20Pipeline%20Parallelism.md)

#### Advanced
- [x] [Profiling and Bottlenecks](04_Supercomputing/03_Optimization/Profiling%20and%20Bottlenecks.md)

## Link -> Knowledge Automation Skill

When you provide a URL, this skill will:
- Fetch the page.
- Infer the correct group (`agents`, `ai`, `supercomputing`, `projects`).
- Infer progression level (`beginner`, `intermediate`, `advanced`).
- Create or update a README-style knowledge note or topic dossier under that group.
- Generate a deep research-style article note in prose (not bullet-only summaries).
- Include the original source as a markdown link.
- Enforce `>=3` bibliography citations by default.
- Upsert a checkbox entry in that group knowledge index, including citation count.

### Command

```bash
python scripts/add_knowledge_from_url.py "https://example.com/article"
```

### Optional flags

```bash
# Force target group
python scripts/add_knowledge_from_url.py "https://example.com/article" --group agents

# Force level
python scripts/add_knowledge_from_url.py "https://example.com/article" --level beginner

# Override title
python scripts/add_knowledge_from_url.py "https://example.com/article" --title "My Custom Title"

# Topic dossier mode
python scripts/add_knowledge_from_url.py "https://primary-source.example" \
  --kind topic \
  --topic-id transformer-architecture \
  --group ai \
  --level intermediate \
  --extra-source "https://second-source.example" \
  --extra-source "https://third-source.example"

# Minimum citations (default: 3)
python scripts/add_knowledge_from_url.py "https://example.com/article" --min-citations 4

# Force overwrite of target note
python scripts/add_knowledge_from_url.py "https://example.com/article" --overwrite

# Preview only
python scripts/add_knowledge_from_url.py "https://example.com/article" --dry-run
```

## Vault Structure

```text
.
├── 00_Inbox/
├── 01_MOCs/
├── 02_Agents/
│   ├── 01_Architectures/
│   ├── 02_Prompting/
│   ├── 03_Tooling/
│   ├── 04_Memory/
│   ├── 05_Evaluation/
│   ├── 06_Knowledge/
│   ├── Skills/
│   └── Agents Index.md
├── 03_AI/
│   ├── 01_Foundations/
│   ├── 02_Modeling/
│   ├── 03_Post-Training/
│   ├── 04_RAG/
│   ├── 05_Evaluation/
│   ├── 06_Knowledge/
│   └── AI Index.md
├── 04_Supercomputing/
│   ├── 01_Infrastructure/
│   ├── 02_Distributed-Training/
│   ├── 03_Optimization/
│   ├── 04_Knowledge/
│   └── Supercomputing Index.md
├── 05_Projects/
│   ├── Knowledge/
│   └── Projects Index.md
├── 99_Templates/
└── scripts/
    └── add_knowledge_from_url.py
```

## Obsidian Compatibility

1. Use `[[wikilinks]]` in each permanent note.
2. Keep frontmatter fields (`created`, `updated`, `tags`, `domain`, `status`).
3. Update related index pages when adding new notes.
4. Keep one main idea per note for cleaner graph nodes.

## Main Entry Points

- [Home MOC](01_MOCs/Home.md)
- [Agents MOC](01_MOCs/Agents%20MOC.md)
- [AI MOC](01_MOCs/AI%20MOC.md)
- [Supercomputing MOC](01_MOCs/Supercomputing%20MOC.md)
- [Agents Index](02_Agents/Agents%20Index.md)
- [Skills Index](02_Agents/Skills/Skills%20Index.md)
- [AI Index](03_AI/AI%20Index.md)
- [Supercomputing Index](04_Supercomputing/Supercomputing%20Index.md)
- [Projects Index](05_Projects/Projects%20Index.md)
