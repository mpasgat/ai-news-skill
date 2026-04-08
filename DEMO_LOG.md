# Демо: как skill работает в Claude Code

Ниже воспроизводимый локальный пример через fixture-источник.

## 1) Команда
```bash
venv\Scripts\python scripts/news_skill.py --feeds-file tests/fixtures/demo-feeds.txt --query "agent" --days 30 --limit 5 --format markdown
```

## 2) Вывод, который возвращается в контекст агента
```markdown
# AI News Digest
_Generated: 2026-04-08 17:39 UTC; window: last 30 days; query: `agent`_
_Sources: 1 ok, 0 failed_

1. [OpenAI launches new agent tooling for enterprises](https://example.com/openai-agent-enterprise)
   - Source: Demo AI Feed
   - Date: 2026-04-07
   - Why relevant: matched AI keywords score `10`
   - Summary: New enterprise APIs for agent orchestration, RAG, and token optimization.

## Quick Insight
Most links above are ranked by AI-keyword density and recency. For deeper analysis, rerun with a focused `--query`.
```

## 3) Как это выглядит как slash-команда
`/news agent` -> агент запускает `python scripts/news_skill.py ...` -> digest появляется прямо в ответе.

