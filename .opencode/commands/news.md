# /news

Purpose: build an AI-news digest and insert it directly into agent context.

Command:
```bash
python scripts/news_skill.py --query "{{args}}" --days 3 --limit 10 --format markdown
```

Behavior:
- If `{{args}}` is empty, use all AI topics.
- Return output directly in chat.
- If some feeds fail, continue and mention partial coverage.
