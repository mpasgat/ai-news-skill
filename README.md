# AI News Skill for Claude Code / OpenCode

Рабочий skill, который собирает AI-новости из нескольких источников, фильтрует по релевантности и отдает компактный digest прямо в контекст агента.

## Для кого и зачем
Этот проект для команд и individual-разработчиков, которым нужно быстро получать свежие AI-обновления без ручного обхода десятков сайтов.  
Skill полезен backend-инженеру, продукту и аналитике: он сразу выдает ссылки, краткий контекст и приоритетные новости по теме.  
Подход снижает время на ресерч и помогает принимать решения на основе актуальной повестки AI-рынка.  
В формате slash-команды (`/news`) это удобно встроить в ежедневный workflow в Claude Code или OpenCode.

## Что внутри репозитория
- `SKILL.md` — описание skill и как его использовать агенту.
- `scripts/news_skill.py` — Python-парсер + фильтрация + ранжирование + форматирование результата.
- `.claude/commands/news.md` — slash-команда `/news` для Claude Code.
- `.opencode/commands/news.md` — аналогичная команда для OpenCode.
- `INSTALLATION.md` — пошаговый запуск.
- `DEMO_LOG.md` — пример работы skill внутри агентного сценария.
- `tests/` + `.github/workflows/tests.yml` — автопроверка.

## Быстрый старт
```bash
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
python scripts/news_skill.py --query "agents" --days 3 --limit 10 --format markdown
```

По умолчанию скрипт читает источники из `feeds.txt`. Это позволяет быстро заменить проблемные RSS-ссылки без изменения кода.

## Пример вызова slash-команды
- Claude Code: `/news agents`
- OpenCode: `/news agents` (или через аналогичный command file)

## Что бы улучшил первым
Первым шагом добавил бы ML-ранжирование и кластеризацию дублей через embeddings, чтобы дайджест показывал не просто keyword-match, а реальные “сигналы” по важности и новизне. Это даст меньше шума и больше value при большом объеме источников.
