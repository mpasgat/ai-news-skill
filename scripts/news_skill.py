#!/usr/bin/env python3
"""AI News Skill: collect, filter and format AI news for agent context."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sys
from dataclasses import dataclass
from typing import Iterable, Sequence

import feedparser
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

DEFAULT_FEEDS: tuple[str, ...] = (
    "https://openai.com/news/rss.xml",
    "https://blog.google/technology/ai/rss/",
    "http://news.mit.edu/rss/topic/artificial-intelligence2",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "https://venturebeat.com/category/ai/feed/",
    "https://techcrunch.com/category/artificial-intelligence/feed/",
)

AI_KEYWORDS: tuple[str, ...] = (
    "ai",
    "artificial intelligence",
    "llm",
    "gpt",
    "claude",
    "gemini",
    "mistral",
    "deepseek",
    "openai",
    "anthropic",
    "agent",
    "rag",
    "inference",
    "token",
    "transformer",
    "multimodal",
)

NEGATIVE_KEYWORDS: tuple[str, ...] = (
    "game ai bot",
    "fifa ai",
    "call of duty ai",
)

USER_AGENT = "ai-news-skill/1.0 (+local skill)"


@dataclass(slots=True)
class NewsItem:
    title: str
    url: str
    source: str
    published: dt.datetime
    summary: str
    score: int


@dataclass(slots=True)
class FeedRunResult:
    items: list[NewsItem]
    successful_feeds: list[str]
    failed_feeds: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect and filter AI news.")
    parser.add_argument("--query", default="", help="Optional text filter.")
    parser.add_argument("--days", type=int, default=3, help="Lookback window in days.")
    parser.add_argument("--limit", type=int, default=10, help="Max items in output.")
    parser.add_argument(
        "--feeds",
        nargs="*",
        default=list(DEFAULT_FEEDS),
        help="Override feed list.",
    )
    parser.add_argument(
        "--feeds-file",
        default="",
        help="Path to text file with one feed URL per line.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=12,
        help="HTTP timeout in seconds per feed.",
    )
    parser.add_argument(
        "--fail-on-empty",
        action="store_true",
        help="Return non-zero code when no items are found.",
    )
    return parser.parse_args()


def to_datetime(entry: feedparser.FeedParserDict) -> dt.datetime:
    struct = entry.get("published_parsed") or entry.get("updated_parsed")
    if struct:
        return dt.datetime(*struct[:6], tzinfo=dt.timezone.utc)
    return dt.datetime.now(tz=dt.timezone.utc)


def clean_text(text: str) -> str:
    no_html = re.sub(r"<[^>]+>", " ", text or "")
    return re.sub(r"\s+", " ", no_html).strip()


def normalized_key(title: str, url: str) -> str:
    t = re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()
    u = re.sub(r"\?.*$", "", url.lower()).rstrip("/")
    return f"{t}|{u}"


def score_item(text: str) -> int:
    lowered = text.lower()
    if any(neg in lowered for neg in NEGATIVE_KEYWORDS):
        return -100
    score = 0
    for keyword in AI_KEYWORDS:
        if keyword in {"ai", "llm", "gpt", "rag"}:
            # Use word boundaries for short terms to avoid false positives
            pattern = rf"\b{re.escape(keyword)}\b"
            if re.search(pattern, lowered):
                score += 2
            continue
        if keyword in lowered:
            score += 2
    return score


def requests_session() -> requests.Session:
    retry = Retry(
        total=2,
        connect=2,
        read=2,
        backoff_factor=0.4,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def feed_variants(url: str) -> tuple[str, ...]:
    if url.startswith("file://"):
        return (url,)
    trimmed = url.rstrip("/")
    return (trimmed, f"{trimmed}/")


def parse_feed(url: str, timeout: int, session: requests.Session) -> feedparser.FeedParserDict:
    if url.startswith("file://"):
        local_path = pathlib.Path(url[7:])
        return feedparser.parse(local_path.read_bytes())
    last_error: Exception | None = None
    for variant in feed_variants(url):
        try:
            response = session.get(variant, timeout=timeout, headers={"User-Agent": USER_AGENT})
            response.raise_for_status()
            return feedparser.parse(response.content)
        except Exception as exc:  # noqa: BLE001
            last_error = exc
    if last_error is not None:
        raise last_error
    raise RuntimeError("No feed variant to parse.")


def resolve_feeds(args: argparse.Namespace) -> list[str]:
    feeds = list(args.feeds)
    file_candidate = pathlib.Path(args.feeds_file) if args.feeds_file else pathlib.Path("feeds.txt")
    if file_candidate.exists():
        file_feeds = [
            line.strip()
            for line in file_candidate.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        if file_feeds:
            feeds = file_feeds
    return feeds


def collect_items(feeds: Sequence[str], days: int, query: str, timeout: int) -> list[NewsItem]:
    return collect_with_health(feeds=feeds, days=days, query=query, timeout=timeout).items


def collect_with_health(feeds: Sequence[str], days: int, query: str, timeout: int) -> FeedRunResult:
    items: list[NewsItem] = []
    successful_feeds: list[str] = []
    failed_feeds: list[str] = []
    seen: set[str] = set()
    min_date = dt.datetime.now(tz=dt.timezone.utc) - dt.timedelta(days=days)
    query_lower = query.lower().strip()
    session = requests_session()

    for feed_url in feeds:
        try:
            parsed = parse_feed(feed_url, timeout=timeout, session=session)
            successful_feeds.append(feed_url)
        except Exception as exc:  # noqa: BLE001
            print(f"[warn] feed failed: {feed_url} ({exc})", file=sys.stderr)
            failed_feeds.append(feed_url)
            continue

        source_title = clean_text(parsed.feed.get("title", feed_url))
        for entry in parsed.entries:
            title = clean_text(entry.get("title", ""))
            link = entry.get("link", "")
            summary = clean_text(entry.get("summary", "") or entry.get("description", ""))
            published = to_datetime(entry)

            if not title or not link:
                continue
            if published < min_date:
                continue

            text_blob = f"{title}\n{summary}\n{source_title}"
            relevance = score_item(text_blob)
            if relevance <= 0:
                continue

            if query_lower and query_lower not in text_blob.lower():
                continue

            dedup_key = normalized_key(title, link)
            if dedup_key in seen:
                continue
            seen.add(dedup_key)

            items.append(
                NewsItem(
                    title=title,
                    url=link,
                    source=source_title,
                    published=published,
                    summary=summary,
                    score=relevance,
                )
            )

    items.sort(key=lambda x: (x.score, x.published), reverse=True)
    return FeedRunResult(items=items, successful_feeds=successful_feeds, failed_feeds=failed_feeds)


def as_markdown(
    items: Iterable[NewsItem],
    query: str,
    days: int,
    limit: int,
    successful_feeds: Sequence[str] | None = None,
    failed_feeds: Sequence[str] | None = None,
) -> str:
    now = dt.datetime.now(tz=dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    ok_count = len(successful_feeds or [])
    fail_count = len(failed_feeds or [])
    header = [
        "# AI News Digest",
        f"_Generated: {now}; window: last {days} days; query: `{query or 'any'}`_",
        f"_Sources: {ok_count} ok, {fail_count} failed_",
        "",
    ]

    selected = list(items)[:limit]
    if not selected:
        return "\n".join(header + ["No matching AI news found."])

    body: list[str] = []
    for idx, item in enumerate(selected, 1):
        pub = item.published.strftime("%Y-%m-%d")
        snippet = item.summary[:220] + ("..." if len(item.summary) > 220 else "")
        body.extend(
            [
                f"{idx}. [{item.title}]({item.url})",
                f"   - Source: {item.source}",
                f"   - Date: {pub}",
                f"   - Why relevant: matched AI keywords score `{item.score}`",
                f"   - Summary: {snippet or 'No summary provided.'}",
                "",
            ]
        )

    tail = [
        "## Quick Insight",
        "Most links above are ranked by AI-keyword density and recency. For deeper analysis, rerun with a focused `--query`.",
    ]
    return "\n".join(header + body + tail)


def main() -> int:
    args = parse_args()
    run_result = collect_with_health(
        feeds=resolve_feeds(args),
        days=max(1, args.days),
        query=args.query,
        timeout=max(3, args.timeout),
    )
    items = run_result.items

    if args.format == "json":
        payload = [
            {
                "title": i.title,
                "url": i.url,
                "source": i.source,
                "published": i.published.isoformat(),
                "summary": i.summary,
                "score": i.score,
            }
            for i in items[: args.limit]
        ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 2 if args.fail_on_empty and not payload else 0

    print(
        as_markdown(
            items=items,
            query=args.query,
            days=args.days,
            limit=args.limit,
            successful_feeds=run_result.successful_feeds,
            failed_feeds=run_result.failed_feeds,
        )
    )
    return 2 if args.fail_on_empty and not items else 0


if __name__ == "__main__":
    raise SystemExit(main())
