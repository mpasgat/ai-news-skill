# AI News Skill for Claude Code / OpenCode

A production-ready skill that collects AI news from multiple RSS/Atom sources, filters by relevance, and returns a ranked digest directly into the agent context.

## For whom and why
This project is for developers, product teams, and analysts who need fresh AI updates without manual browsing.  
It is especially useful for backend engineers who want quick, link-backed signals about LLM tools, agent frameworks, and industry launches.  
The skill reduces research time by automatically filtering noise and keeping only relevant items.  
With `/news` command integration, it fits directly into daily workflows in Claude Code and OpenCode.

## Repository contents
- `SKILL.md` - skill definition and usage behavior.
- `scripts/news_skill.py` - parser, filtering, ranking, formatting, and resilience logic.
- `feeds.txt` - editable list of news sources (no code changes needed).
- `.claude/commands/news.md` - slash command for Claude Code.
- `.opencode/commands/news.md` - command equivalent for OpenCode.
- `INSTALLATION.md` - setup and run instructions.
- `DEMO_LOG.md` - sample run and output.
- `tests/` + `.github/workflows/tests.yml` - automated validation in CI.

## Quick start
```bash
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/news_skill.py --query "agents" --days 3 --limit 10 --format markdown
```

## Key behavior
- Auto-loads source list from `feeds.txt`.
- Uses retries for transient HTTP failures.
- Shows source health in output: `Sources: X ok, Y failed`.
- Supports strict automation mode with `--fail-on-empty`.

Example:
```bash
python scripts/news_skill.py --query "openai" --days 3 --limit 10 --format markdown --fail-on-empty
```

## Slash command usage
- Claude Code: `/news agents`
- OpenCode: `/news agents`

## Troubleshooting
- If you see warnings like `feed failed`, the script still continues with healthy sources.
- If all feeds fail, check local firewall/proxy/network rules first.
- If results are too broad, narrow with `--query`.
- If results are empty in automation, use wider `--days` or remove strict `--query`.

## What I would improve first
First, I would add embedding-based clustering and ranking so the digest prioritizes novelty and impact, not only keyword frequency. That would reduce near-duplicates and improve signal quality at scale.

