Collect and filter AI news, then return digest directly in chat context.

Use this command format:
- `/news`
- `/news <topic>`

Execution rules:
1. Interpret `$ARGUMENTS` as optional topic query. If empty, use broad mode.
2. Run:
```bash
python scripts/news_skill.py --query "$ARGUMENTS" --days 3 --limit 10 --format markdown
```
3. Return script output as-is in the final response.
4. If script prints warnings for failed feeds, include a short note about partial source availability.
