---
name: ai-news-skill
description: Collect and filter AI news from multiple RSS/Atom sources and return concise, ranked results directly into agent context. Use when a user asks for fresh AI/LLM industry updates, topic-focused AI digests, or summary briefs with links.
---

# AI News Skill

1. Запусти сборщик:
```bash
python scripts/news_skill.py --query "<topic>" --days 3 --limit 10 --format markdown
```

2. Вставь сгенерированный markdown в контекст ответа агента.

3. Если пользователю нужен сырой формат данных, запусти:
```bash
python scripts/news_skill.py --query "<topic>" --days 3 --limit 20 --format json
```

4. Для лучших результатов используй тематические запросы: `openai`, `agents`, `inference`, `multimodal`, `enterprise`.

5. Если часть фидов недоступна, продолжай с доступными источниками и явно укажи частичное покрытие.
