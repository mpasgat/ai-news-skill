# Инструкция по установке и запуску

## 1. Создать виртуальное окружение
```bash
python -m venv .venv
```

## 2. Активировать окружение
Windows PowerShell:
```bash
. .venv/Scripts/Activate.ps1
```

macOS/Linux:
```bash
source .venv/bin/activate
```

## 3. Установить зависимости
```bash
pip install -r requirements.txt
```

## 4. Запустить скрипт skill
```bash
python scripts/news_skill.py --query "openai" --days 3 --limit 10 --format markdown
```

`feeds.txt` используется автоматически, если файл существует в корне проекта.

Для CI/cron-сценариев (считать пустой результат ошибкой):
```bash
python scripts/news_skill.py --query "openai" --days 3 --limit 10 --format markdown --fail-on-empty
```

## 5. Опционально: запустить тесты
```bash
pip install -r requirements-dev.txt
pytest -q tests -p no:cacheprovider
```

## 6. Опционально: детерминированный локальный демо-режим (offline)
```bash
python scripts/news_skill.py --feeds-file tests/fixtures/demo-feeds.txt --query "agent" --days 10 --limit 5 --format markdown
```

