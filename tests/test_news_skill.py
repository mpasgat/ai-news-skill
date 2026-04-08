import argparse
from pathlib import Path

from scripts.news_skill import as_markdown, collect_items, resolve_feeds, score_item


def test_score_item_positive():
    value = score_item("OpenAI releases new multimodal agent platform")
    assert value > 0


def test_score_item_negative_keyword():
    value = score_item("Sports game ai bot launches")
    assert value < 0


def test_score_item_no_false_positive_for_paid():
    value = score_item("Paid subscription model updates this quarter")
    assert value <= 0


def test_collect_items_from_local_feed():
    feed_path = Path("tests/fixtures/demo-feed.xml").resolve()
    feeds = [f"file://{feed_path.as_posix()}"]
    items = collect_items(feeds=feeds, days=30, query="", timeout=3)
    assert len(items) >= 2
    titles = [i.title.lower() for i in items]
    assert any("openai" in t for t in titles)


def test_resolve_feeds_from_file():
    args = argparse.Namespace(
        feeds=["https://example.org/default.xml"],
        feeds_file="tests/fixtures/demo-feeds.txt",
    )
    result = resolve_feeds(args)
    assert result == ["file://tests/fixtures/demo-feed.xml"]


def test_markdown_output_has_header():
    feed_path = Path("tests/fixtures/demo-feed.xml").resolve()
    feeds = [f"file://{feed_path.as_posix()}"]
    items = collect_items(feeds=feeds, days=30, query="", timeout=3)
    output = as_markdown(items, query="openai", days=7, limit=3)
    assert "# AI News Digest" in output
    assert "Quick Insight" in output
