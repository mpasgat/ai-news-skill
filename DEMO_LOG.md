# Demo: skill в действии внутри Claude Code

Ниже пример реального запуска команды (локальный офлайн-источник для воспроизводимости демо).

## 1) Запуск Python-скрипта, который использует skill-логику
```bash
venv\Scripts\python scripts/news_skill.py --feeds-file tests/fixtures/demo-feeds.txt --query "agent" --days 30 --limit 5 --format markdown
```

## 2) Вывод (возвращается в контекст агента)
```markdown
# AI News Digest
_Generated: 2026-04-08 14:44 UTC; window: last 30 days; query: `agent`_

1. [OpenAI launches new agent tooling for enterprises](https://example.com/openai-agent-enterprise)
   - Source: Demo AI Feed
   - Date: 2026-04-07
   - Why relevant: matched AI keywords score `10`
   - Summary: New enterprise APIs for agent orchestration, RAG, and token optimization.

## Quick Insight
Most links above are ranked by AI-keyword density and recency. For deeper analysis, rerun with a focused `--query`.
```

## 3) Как это выглядит как slash command
`/news agent` -> агент выполняет `python scripts/news_skill.py ...` -> digest появляется прямо в ответе.

