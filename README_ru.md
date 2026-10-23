# Бенчмарк README

Бенчмарк сравнивает пять способов генерации README на 48 репозиториях с закреплёнными коммитами. Генераторы работают через OpenRouter: `openai/gpt-6-luna`, `anthropic/claude-haiku-5.5`, `z-ai/glm-5.3-flash`. Оценку GEval выполняет `openai/gpt-6-sol`.

## Установка в Linux

Нужны Python 3.12 и Git. Из корня проекта:

```bash
bash scripts/install_tools.sh
python3 scripts/verify_install.py
```

Скрипт устанавливает актуальные закреплённые версии OSA, LArch и ReadMeReady в отдельных окружениях `.tools/venvs/`, а OpenCode 2 — в `.tools/opencode/`. Коммиты и версии записаны в [tool_versions.json](benchmark_README/tool_versions.json). Старые копии инструментов в корне сохранены как исторические; при запуске используются `.tools/src/`.

При установке к закреплённой версии ReadMeReady применяется [локальный патч](scripts/patches/readmeready-output-paths.patch): он сохраняет промежуточные файлы отдельно от исходников, читает текст UTF-16 и параллельно обрабатывает независимые сводки файлов и папок в пределах заданного лимита. OpenCode запускается в отдельной временной копии репозитория.

Создайте `.env` в корне репозитория с `OPENROUTER_API_KEY=...`. Проверка выводит только факт наличия ключа.

## Этапы

Откройте [ноутбук](benchmark_README/README_benchmark.ipynb) в окружении `benchmark_README/.venv`. Начальная фаза `prepare` загружает закреплённые коммиты, сохраняет исходные README отдельно для оценки и создаёт локальные входы без исходного README. Каждому методу передаётся новая изолированная копия. В [датасете](benchmark_README/data/repo_list.csv) 30 репозиториев Common и 18 Scientific.

Позже запустите фазы `generate`, `score` и `report` по порядку. Последняя создаёт Markdown-таблицу, покрытие и сводку только по репозиториям с полным набором 15 оценок и без подтверждённого доступа генератора к исходному README через сеть. В опубликованной таблице 34 репозитория: 22 Common и 12 Scientific. Три случая такого доступа в OpenCode зафиксированы в [журнале аудита](benchmark_README/results/readme_2026_three_models/evaluation/reference_access.csv); два из них исключены дополнительно, третий уже не имел полного набора результатов. Базовый метод передаёт модели текст репозитория с детерминированным лимитом 64 000 токенов. [Результаты и журналы](benchmark_README/results/README.md) включены в репозиторий.

После подготовки можно выполнить `benchmark_README/.venv/bin/python scripts/run_full_benchmark.py`: скрипт продолжает прерванный запуск, параллельно обрабатывает три модели, оценивает готовые README и формирует таблицу.

Для отдельной оценки сохранённых README моделью `z-ai/glm-5.3-flash` используется `benchmark_README/.venv/bin/python scripts/run_glm_judge.py --run`. Новая оценка сохраняется в `benchmark_README/results/readme_2026_three_models_glm_judge/` и не запускает генераторы. Команда с `--status` показывает число готовых оценок и зарегистрированную стоимость без обращения к API.
