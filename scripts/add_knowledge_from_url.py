#!/usr/bin/env python3
"""Ingest a web URL into this Obsidian-compatible knowledge vault.

The script fetches a URL, extracts lightweight page metadata, classifies the page
into a group (agents/ai/supercomputing/projects), generates a README-style
knowledge note, and appends it to the right group Knowledge Index.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
TODAY = dt.date.today().isoformat()


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

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str | None]]) -> None:
        attrs_dict = {k.lower(): (v or "") for k, v in attrs}
        if tag == "meta":
            key = (attrs_dict.get("name") or attrs_dict.get("property") or "").lower()
            if key in {"description", "og:description", "twitter:description"} and not self.description:
                self.description = clean_text(attrs_dict.get("content", ""))
        if tag in {"title", "h1", "h2", "h3", "p"}:
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
        elif tag in {"h1", "h2", "h3"} and len(self.headings) < 8:
            self.headings.append(text)
        elif tag == "p" and len(self.paragraphs) < 6:
            self.paragraphs.append(text)

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


def append_to_knowledge_index(cfg: GroupConfig, title: str, note_dir: Path, level: str, source_url: str) -> None:
    index_path = ROOT / cfg.knowledge_index
    rel = note_dir.relative_to(index_path.parent)
    line = f"- [ ] [{title}]({rel.as_posix()}/README.md) - level: {level} - source: {source_url}\n"

    existing = index_path.read_text(encoding="utf-8")
    if source_url in existing:
        return

    if "## Entries" not in existing:
        existing = existing.rstrip() + "\n\n## Entries\n\n"

    updated = existing.rstrip() + "\n" + line
    index_path.write_text(updated + "\n", encoding="utf-8")


def build_note_content(
    cfg: GroupConfig,
    title: str,
    url: str,
    level: str,
    description: str,
    headings: List[str],
    paragraphs: List[str],
    access_limited: bool,
) -> str:
    if access_limited:
        summary = (
            "Content could not be fully fetched in this environment because the source requires "
            "JavaScript/authenticated rendering. Add the post text manually."
        )
    else:
        summary = description or (paragraphs[0] if paragraphs else "")
        summary = summary or "Add a short summary of the source."

    bullets = headings[:5] if headings else []
    if not bullets and paragraphs:
        bullets = [paragraphs[0][:140], paragraphs[1][:140] if len(paragraphs) > 1 else ""]
        bullets = [b for b in bullets if b]

    if access_limited:
        bullets = [
            "Page rendering is blocked in this environment (JavaScript/auth wall).",
            "Paste the primary content and key claims manually.",
        ]

    if not bullets:
        bullets = ["Extract key points from the source."]

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
        f"- URL: {url}",
        f"- Captured: {TODAY}",
        "",
        "## Summary",
        summary,
        "",
        "## Key Points",
    ]
    lines.extend([f"- {item}" for item in bullets])
    lines.extend(
        [
            "",
            "## Connections",
            f"- [[{cfg.group_index.with_suffix('').as_posix()}]]",
            f"- [[{cfg.moc.with_suffix('').as_posix()}]]",
            f"- [[{cfg.knowledge_index.with_suffix('').as_posix()}]]",
            "",
            "## Notes",
            "- Add your personal takeaways.",
            "- Add comparisons with existing notes.",
            "",
        ]
    )
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

    group = args.group if args.group != "auto" else classify_group(combined_text)
    level = args.level if args.level != "auto" else classify_level(combined_text)
    cfg = GROUPS[group]

    title = clean_text(args.title) or parser.title
    if not title:
        title = derive_title_from_url(parsed)

    slug = slugify(title)
    note_dir = unique_note_dir(ROOT / cfg.knowledge_dir, slug)
    note_path = note_dir / "README.md"
    access_limited = has_x_js_block_page(parsed, parser)

    note_content = build_note_content(
        cfg=cfg,
        title=title,
        url=args.url,
        level=level,
        description=parser.description,
        headings=parser.headings,
        paragraphs=parser.paragraphs,
        access_limited=access_limited,
    )

    if args.dry_run:
        print(f"group={group}")
        print(f"level={level}")
        print(f"target={note_path.relative_to(ROOT)}")
        return 0

    note_dir.mkdir(parents=True, exist_ok=True)
    note_path.write_text(note_content, encoding="utf-8")

    ensure_knowledge_index(group, cfg)
    append_to_knowledge_index(cfg, title, note_dir, level, args.url)

    print(f"Created: {note_path.relative_to(ROOT)}")
    print(f"Updated: {cfg.knowledge_index.as_posix()}")
    print(f"Group: {group} | Level: {level}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
