---
name: ai-news-skill
description: Collect and filter AI news from multiple RSS/Atom sources and return concise, ranked results directly into agent context. Use when a user asks for fresh AI/LLM industry updates, topic-focused AI digests, or summary briefs with links.
---

# AI News Skill

1. Run the collector:
```bash
python scripts/news_skill.py --query "<topic>" --days 3 --limit 10 --format markdown
```

2. Paste the generated markdown into the agent response context.

3. If user asks for raw data, run:
```bash
python scripts/news_skill.py --query "<topic>" --days 3 --limit 20 --format json
```

4. Prefer topic queries like `openai`, `agents`, `inference`, `multimodal`, `enterprise`.

5. If feeds fail, keep successful sources and continue; mention partial coverage.
