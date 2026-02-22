#!/usr/bin/env python3
"""Ingest a web URL into this Obsidian-compatible knowledge vault.

The script fetches a URL, extracts lightweight page metadata, classifies the page
into a group (agents/ai/supercomputing/projects), generates a README-style
knowledge note, and appends it to the right group Knowledge Index.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
TODAY = dt.date.today().isoformat()
ENTRY_RE = re.compile(
    r"^- \[ \] \[(?P<title>.+?)\]\((?P<path>.+?)\) - level: (?P<level>[a-z]+) - source: (?P<source>.+)$"
)
NOISE_PATTERNS = [
    "javascript is disabled",
    "supported browsers",
    "start typing and press enter to search",
    "sign in",
    "log in",
    "cookie",
    "privacy policy",
    "subscribe to receive notifications",
    "newsletter",
    "the cloudflare blog",
]
HTML_TAG_RE = re.compile(r"<[^>]+>")


@dataclass(frozen=True)
class GroupConfig:
    domain: str
    knowledge_dir: Path
    group_index: Path
    moc: Path
    knowledge_index: Path


GROUPS: Dict[str, GroupConfig] = {
    "agents": GroupConfig(
        domain="agents",
        knowledge_dir=Path("02_Agents/06_Knowledge"),
        group_index=Path("02_Agents/Agents Index.md"),
        moc=Path("01_MOCs/Agents MOC.md"),
        knowledge_index=Path("02_Agents/06_Knowledge/Knowledge Index.md"),
    ),
    "ai": GroupConfig(
        domain="ai",
        knowledge_dir=Path("03_AI/06_Knowledge"),
        group_index=Path("03_AI/AI Index.md"),
        moc=Path("01_MOCs/AI MOC.md"),
        knowledge_index=Path("03_AI/06_Knowledge/Knowledge Index.md"),
    ),
    "supercomputing": GroupConfig(
        domain="supercomputing",
        knowledge_dir=Path("04_Supercomputing/04_Knowledge"),
        group_index=Path("04_Supercomputing/Supercomputing Index.md"),
        moc=Path("01_MOCs/Supercomputing MOC.md"),
        knowledge_index=Path("04_Supercomputing/04_Knowledge/Knowledge Index.md"),
    ),
    "projects": GroupConfig(
        domain="project",
        knowledge_dir=Path("05_Projects/Knowledge"),
        group_index=Path("05_Projects/Projects Index.md"),
        moc=Path("01_MOCs/Home.md"),
        knowledge_index=Path("05_Projects/Knowledge/Knowledge Index.md"),
    ),
}

GROUP_KEYWORDS = {
    "agents": [
        "agent",
        "multi-agent",
        "tool use",
        "function calling",
        "prompt",
        "reasoning",
        "memory",
        "planning",
    ],
    "ai": [
        "llm",
        "language model",
        "transformer",
        "fine-tuning",
        "rlhf",
        "dpo",
        "embedding",
        "rag",
        "dataset",
        "inference",
    ],
    "supercomputing": [
        "hpc",
        "supercomputing",
        "cuda",
        "gpu",
        "cluster",
        "distributed",
        "nccl",
        "mpi",
        "slurm",
        "throughput",
    ],
    "projects": [
        "implementation",
        "case study",
        "build",
        "demo",
        "project",
        "repository",
    ],
}

LEVEL_KEYWORDS = {
    "beginner": ["beginner", "intro", "introduction", "basics", "101", "overview"],
    "intermediate": ["practical", "implementation", "applied", "workflow", "guide"],
    "advanced": ["advanced", "research", "optimization", "scaling", "benchmark", "sota"],
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._capture_tag: str | None = None
        self._buffer: List[str] = []
        self.title = ""
        self.description = ""
        self.headings: List[str] = []
        self.paragraphs: List[str] = []
        self.list_items: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str | None]]) -> None:
        attrs_dict = {k.lower(): (v or "") for k, v in attrs}
        if tag == "meta":
            key = (attrs_dict.get("name") or attrs_dict.get("property") or "").lower()
            if key in {"description", "og:description", "twitter:description"} and not self.description:
                self.description = clean_text(attrs_dict.get("content", ""))
        if tag in {"title", "h1", "h2", "h3", "p", "li"}:
            self._capture_tag = tag
            self._buffer = []

    def handle_data(self, data: str) -> None:
        if self._capture_tag:
            self._buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._capture_tag != tag:
            return
        text = clean_text("".join(self._buffer))
        if not text:
            self._capture_tag = None
            self._buffer = []
            return

        if tag == "title" and not self.title:
            self.title = text
        elif tag in {"h1", "h2", "h3"} and len(self.headings) < 20:
            self.headings.append(text)
        elif tag == "p" and len(self.paragraphs) < 60:
            self.paragraphs.append(text)
        elif tag == "li" and len(self.list_items) < 80:
            self.list_items.append(text)

        self._capture_tag = None
        self._buffer = []


def clean_text(raw: str) -> str:
    text = unescape(raw)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def slugify(text: str) -> str:
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s_-]+", "-", slug)
    slug = slug.strip("-")
    return slug[:72] or "untitled-source"


def derive_title_from_url(parsed: urllib.parse.ParseResult) -> str:
    host = parsed.netloc.lower()
    parts = [p for p in parsed.path.split("/") if p]

    if host in {"x.com", "twitter.com"} and len(parts) >= 3 and parts[1] == "status":
        user = parts[0]
        status_id = parts[2]
        return f"X Post by {user} ({status_id})"

    tail = Path(parsed.path).name.replace("-", " ").replace("_", " ").strip()
    if tail:
        return tail.title()
    return parsed.netloc


def has_x_js_block_page(parsed: urllib.parse.ParseResult, parser: "PageParser") -> bool:
    host = parsed.netloc.lower()
    if host not in {"x.com", "twitter.com"}:
        return False
    haystack = " ".join([parser.title, parser.description, *parser.paragraphs]).lower()
    return "javascript is disabled" in haystack


def fetch_x_oembed(url: str) -> Optional[Dict[str, str]]:
    endpoint = "https://publish.twitter.com/oembed?url=" + urllib.parse.quote(url, safe="")
    try:
        req = urllib.request.Request(endpoint, headers={"User-Agent": "Mozilla/5.0 (knowledge-ingestor)"})
        raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="replace")
        data = json.loads(raw)
    except Exception:
        return None

    html = clean_text(data.get("html", ""))
    text = clean_text(HTML_TAG_RE.sub(" ", html))
    return {
        "author_name": clean_text(data.get("author_name", "")),
        "author_url": clean_text(data.get("author_url", "")),
        "provider_name": clean_text(data.get("provider_name", "")),
        "embed_text": text,
    }


def is_noise(text: str) -> bool:
    lower = text.lower()
    return any(pattern in lower for pattern in NOISE_PATTERNS)


def split_sentences(text: str) -> List[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [clean_text(p) for p in parts if clean_text(p)]


def extract_content_sentences(description: str, paragraphs: List[str], list_items: List[str]) -> List[str]:
    sentences: List[str] = []
    for block in [description, *paragraphs, *list_items]:
        if not block or is_noise(block):
            continue
        for sentence in split_sentences(block):
            if len(sentence) < 35 or len(sentence) > 340:
                continue
            if is_noise(sentence):
                continue
            if sentence.endswith(":"):
                continue
            sentences.append(sentence)

    deduped: List[str] = []
    seen = set()
    for sentence in sentences:
        key = sentence.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(sentence)
    return deduped


def choose_summary(description: str, sentences: List[str], access_limited: bool) -> str:
    if access_limited:
        return (
            "Content could not be fully fetched in this environment because the source requires "
            "JavaScript/authenticated rendering. Add the post text manually."
        )
    if description and not is_noise(description):
        if len(description) < 90 and sentences:
            extra = next((s for s in sentences if s.lower() != description.lower()), "")
            if extra:
                return f"{description} {extra}"
        return description
    if sentences:
        return sentences[0]
    return "Add a short summary of the source."


def pick_distinct_sentences(sentences: List[str], count: int) -> List[str]:
    picked: List[str] = []
    seen_tokens: set[str] = set()
    for sentence in sentences:
        tokens = set(re.findall(r"[a-z]{4,}", sentence.lower()))
        if not tokens:
            continue
        overlap = len(tokens & seen_tokens) / max(len(tokens), 1)
        if overlap > 0.65:
            continue
        picked.append(sentence)
        seen_tokens |= tokens
        if len(picked) >= count:
            break
    return picked


def fetch_page(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (knowledge-ingestor)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.read().decode(charset, errors="replace")
    except urllib.error.URLError as exc:
        reason = getattr(exc, "reason", None)
        if isinstance(reason, ssl.SSLCertVerificationError):
            insecure_ctx = ssl.create_default_context()
            insecure_ctx.check_hostname = False
            insecure_ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(req, timeout=30, context=insecure_ctx) as resp:
                charset = resp.headers.get_content_charset() or "utf-8"
                return resp.read().decode(charset, errors="replace")
        raise


def classify_group(text: str) -> str:
    haystack = text.lower()
    scores: Dict[str, int] = {}
    for group, keywords in GROUP_KEYWORDS.items():
        scores[group] = sum(haystack.count(keyword) for keyword in keywords)

    best_group, best_score = max(scores.items(), key=lambda item: item[1])
    return best_group if best_score > 0 else "ai"


def classify_level(text: str) -> str:
    haystack = text.lower()
    scores: Dict[str, int] = {}
    for level, keywords in LEVEL_KEYWORDS.items():
        scores[level] = sum(haystack.count(keyword) for keyword in keywords)

    best_level, best_score = max(scores.items(), key=lambda item: item[1])
    return best_level if best_score > 0 else "intermediate"


def unique_note_dir(base_dir: Path, slug: str) -> Path:
    candidate = base_dir / slug
    if not candidate.exists():
        return candidate

    i = 2
    while True:
        candidate = base_dir / f"{slug}-{i}"
        if not candidate.exists():
            return candidate
        i += 1


def ensure_knowledge_index(group: str, cfg: GroupConfig) -> None:
    index_path = ROOT / cfg.knowledge_index
    index_path.parent.mkdir(parents=True, exist_ok=True)
    if index_path.exists():
        return

    title = f"{group.title()} Knowledge Index"
    content = "\n".join(
        [
            "---",
            f"created: {TODAY}",
            f"updated: {TODAY}",
            f"tags: [{cfg.domain}, knowledge, index]",
            f"domain: {cfg.domain}",
            "status: active",
            "---",
            "",
            f"# {title}",
            "",
            f"- [[{cfg.group_index.with_suffix('').as_posix()}]]",
            f"- [[{cfg.moc.with_suffix('').as_posix()}]]",
            "",
            "## Entries",
            "",
        ]
    )
    index_path.write_text(content, encoding="utf-8")


def find_existing_entry_by_source(source_url: str) -> Optional[Tuple[str, GroupConfig, Path, str, str]]:
    for group, cfg in GROUPS.items():
        index_path = ROOT / cfg.knowledge_index
        if not index_path.exists():
            continue
        lines = index_path.read_text(encoding="utf-8").splitlines()
        for line in lines:
            match = ENTRY_RE.match(line.strip())
            if not match:
                continue
            if match.group("source").strip() != source_url:
                continue
            rel_path = Path(match.group("path"))
            note_path = (index_path.parent / rel_path).resolve()
            return (
                group,
                cfg,
                note_path,
                match.group("title"),
                match.group("level"),
            )
    return None


def upsert_knowledge_index_entry(cfg: GroupConfig, title: str, note_dir: Path, level: str, source_url: str) -> None:
    index_path = ROOT / cfg.knowledge_index
    rel = note_dir.relative_to(index_path.parent)
    line = f"- [ ] [{title}]({rel.as_posix()}/README.md) - level: {level} - source: {source_url}\n"

    lines = index_path.read_text(encoding="utf-8").splitlines()
    replaced = False
    new_lines: List[str] = []
    for current in lines:
        match = ENTRY_RE.match(current.strip())
        if match and match.group("source").strip() == source_url:
            new_lines.append(line.strip())
            replaced = True
        else:
            new_lines.append(current)

    updated = "\n".join(new_lines).rstrip()
    if not replaced:
        if "## Entries" not in updated:
            updated = updated + "\n\n## Entries\n"
        updated = updated + "\n" + line.strip()

    index_path.write_text(updated + "\n", encoding="utf-8")


def build_note_content(
    cfg: GroupConfig,
    title: str,
    url: str,
    level: str,
    description: str,
    headings: List[str],
    paragraphs: List[str],
    list_items: List[str],
    access_limited: bool,
    oembed_info: Optional[Dict[str, str]] = None,
) -> str:
    content_sentences = extract_content_sentences(description, paragraphs, list_items)
    selected = pick_distinct_sentences(content_sentences, 16)
    summary = choose_summary(description, content_sentences, access_limited)
    clean_headings = [h for h in headings if not is_noise(h)]
    heading_overview = ", ".join(clean_headings[:4]) if clean_headings else "core concepts and implementation details"
    level_article = "an" if level[:1].lower() in {"a", "e", "i", "o", "u"} else "a"

    def synth(start: int, take: int, fallback: str) -> str:
        chunk = selected[start : start + take]
        if chunk:
            return " ".join(chunk)
        return fallback

    if access_limited:
        author = (oembed_info or {}).get("author_name", "")
        author_url = (oembed_info or {}).get("author_url", "")
        embed_text = (oembed_info or {}).get("embed_text", "")
        provider = (oembed_info or {}).get("provider_name", "")
        author_fragment = f" by {author}" if author else ""
        author_link_fragment = f" ({author_url})" if author_url else ""

        abstract = (
            "This resource is archived as a reference node, but full content extraction failed because the source "
            "requires JavaScript or authenticated rendering in this environment."
        )
        context = (
            f"Even with blocked rendering, metadata from {provider or 'the platform'} indicates this is a social post{author_fragment}{author_link_fragment}. "
            "Preserving this entry keeps the knowledge graph complete and makes later manual enrichment straightforward."
        )
        method = (
            "The ingestion process captured canonical source metadata and linked this note to its topic hubs. "
            "When available, oEmbed metadata was used as secondary evidence for authorship and post context."
        )
        findings = (
            f"Available fallback metadata: {embed_text}" if embed_text else
            "No trustworthy detailed claims were extracted automatically from the page payload. Any substantive summary, "
            "technical claims, or caveats should be added by reading the source directly."
        )
        critique = (
            "Dynamic platform rendering and auth walls limit reproducible extraction. "
            "For high-value social references, manually copy the post body and linked resource context into this note."
        )
    else:
        abstract = (
            f"{summary} This note frames the source as {level_article} {level}-level reference in the `{cfg.domain}` track and "
            "captures its technical contribution in research-article form for later retrieval and synthesis."
        )
        context = (
            f"The source positions its discussion around {heading_overview}. "
            f"{synth(1, 2, 'It emphasizes practical trade-offs that appear during real-world deployment rather than toy examples.')}"
        )
        method = (
            "The material uses a systems-oriented explanatory approach: it introduces a constraint, maps design "
            "choices to execution behavior, and then demonstrates how those choices affect operational outcomes. "
            f"{synth(3, 3, 'Its structure suggests a progression from conceptual framing to implementation-level guidance.')}"
        )
        findings = (
            f"{synth(0, 3, 'The source highlights concrete technical claims worth validating in follow-up experiments.')} "
            f"{synth(6, 2, 'A recurring theme is the tension between capability, efficiency, and reliability under constraints.')}"
        )
        critique = (
            f"{synth(8, 2, 'A key caveat is that headline claims may depend on assumptions not fully visible without deeper benchmarking context.')} "
            "Treat this summary as a research waypoint; validate claims against additional sources, benchmarks, or implementation experiments before operational adoption."
        )

    application = (
        f"In this vault, the resource should be studied alongside [[{cfg.group_index.with_suffix('').as_posix()}]], "
        f"[[{cfg.moc.with_suffix('').as_posix()}]], and [[{cfg.knowledge_index.with_suffix('').as_posix()}]]. "
        "Add implementation notes, disagreements, and follow-up experiments to convert this archive entry into actionable knowledge."
    )
    graph_connections = (
        f"Related graph nodes: [[{cfg.group_index.with_suffix('').as_posix()}]], "
        f"[[{cfg.moc.with_suffix('').as_posix()}]], and [[{cfg.knowledge_index.with_suffix('').as_posix()}]]."
    )

    lines = [
        "---",
        f"created: {TODAY}",
        f"updated: {TODAY}",
        f"tags: [{cfg.domain}, knowledge, {level}]",
        f"domain: {cfg.domain}",
        "status: seed",
        f"source_url: \"{url}\"",
        "---",
        "",
        f"# {title}",
        "",
        "## Source",
        f"Original URL: [{url}]({url})",
        "",
        f"Captured on {TODAY}.",
        "",
        "## Abstract",
        abstract,
        "",
        "## Context and Problem Framing",
        context,
        "",
        "## Technical Approach",
        method,
        "",
        "## Main Findings",
        findings,
        "",
        "## Critical Analysis",
        critique,
        "",
        "## Application to This Cookbook",
        application,
        "",
        "## Graph Connections",
        graph_connections,
        "",
        "## Research Notes",
        "Use this space for your own deeper synthesis, replication notes, contradictions with other sources, and concrete follow-up experiments.",
    ]
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest a URL into the cookbook knowledge vault.")
    parser.add_argument("url", help="Source URL to ingest.")
    parser.add_argument(
        "--group",
        choices=["auto", *GROUPS.keys()],
        default="auto",
        help="Target group. Defaults to auto classification.",
    )
    parser.add_argument(
        "--level",
        choices=["auto", "beginner", "intermediate", "advanced"],
        default="auto",
        help="Difficulty/progression level tag for checklist tracking.",
    )
    parser.add_argument("--title", default="", help="Optional manual title override.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print decisions without writing files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    parsed = urllib.parse.urlparse(args.url)
    if not parsed.scheme or not parsed.netloc:
        print("Error: URL must include scheme and host, for example https://example.com/article")
        return 1

    parser = PageParser()
    try:
        html = fetch_page(args.url)
        parser.feed(html)
    except urllib.error.URLError as exc:
        if not args.dry_run:
            print(f"Error: could not fetch URL: {exc}")
            return 2

    combined_text = "\n".join(
        [
            parser.title,
            parser.description,
            *parser.headings,
            *parser.paragraphs,
            args.url,
        ]
    )

    existing_entry = find_existing_entry_by_source(args.url)

    inferred_group = classify_group(combined_text)
    inferred_level = classify_level(combined_text)

    if args.group != "auto":
        group = args.group
    elif existing_entry:
        group = existing_entry[0]
    else:
        group = inferred_group

    if args.level != "auto":
        level = args.level
    elif existing_entry:
        level = existing_entry[4]
    else:
        level = inferred_level

    cfg = GROUPS[group]

    title = clean_text(args.title) or parser.title
    if title and is_noise(title):
        title = ""
    if not title and existing_entry:
        title = existing_entry[3]
    if not title:
        title = derive_title_from_url(parsed)

    if existing_entry and existing_entry[1] == cfg:
        note_path = existing_entry[2]
        note_dir = note_path.parent
    else:
        slug = slugify(title)
        note_dir = unique_note_dir(ROOT / cfg.knowledge_dir, slug)
        note_path = note_dir / "README.md"

    access_limited = has_x_js_block_page(parsed, parser)
    oembed_info = fetch_x_oembed(args.url) if access_limited else None

    note_content = build_note_content(
        cfg=cfg,
        title=title,
        url=args.url,
        level=level,
        description=parser.description,
        headings=parser.headings,
        paragraphs=parser.paragraphs,
        list_items=parser.list_items,
        access_limited=access_limited,
        oembed_info=oembed_info,
    )

    if args.dry_run:
        print(f"group={group}")
        print(f"level={level}")
        print(f"target={note_path.relative_to(ROOT)}")
        if existing_entry:
            print("mode=update-existing")
        else:
            print("mode=create-new")
        return 0

    note_dir.mkdir(parents=True, exist_ok=True)
    note_path.write_text(note_content, encoding="utf-8")

    ensure_knowledge_index(group, cfg)
    upsert_knowledge_index_entry(cfg, title, note_dir, level, args.url)

    action = "Updated" if existing_entry and existing_entry[1] == cfg else "Created"
    print(f"{action}: {note_path.relative_to(ROOT)}")
    print(f"Updated: {cfg.knowledge_index.as_posix()}")
    print(f"Group: {group} | Level: {level}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
