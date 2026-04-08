# Installation & Run Guide

## 1. Create virtual environment
```bash
python -m venv .venv
```

## 2. Activate environment
Windows PowerShell:
```bash
. .venv/Scripts/Activate.ps1
```

macOS/Linux:
```bash
source .venv/bin/activate
```

## 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 4. Run skill script
```bash
python scripts/news_skill.py --query "openai" --days 3 --limit 10 --format markdown
```

`feeds.txt` используется автоматически, если файл существует в корне проекта.

Для CI/cron сценариев (считать пустой результат ошибкой):
```bash
python scripts/news_skill.py --query "openai" --days 3 --limit 10 --format markdown --fail-on-empty
```

## 5. Optional: run tests
```bash
pip install -r requirements-dev.txt
pytest -q tests -p no:cacheprovider
```

## 6. Optional: deterministic local demo (offline)
```bash
python scripts/news_skill.py --feeds-file tests/fixtures/demo-feeds.txt --query "agent" --days 10 --limit 5 --format markdown
```
