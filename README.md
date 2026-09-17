# 🔴 pokemonbattle_api_tests

Учебный проект автотестов REST API игры **Pokemon Battle** на `pytest` + `requests` с Allure-отчётами
и прогоном в GitLab CI.

⚠️ВНИМАНИЕ: Проверки написаны по заданиям в ходе учебного процесса. Некоторые тесты реализованы для отработки 
специальных навыков. Это не выбранные мною обязательные Smoke тесты. Каких то проверок может не хватать, но 
периодически я буду дополнять проект. Цель проекта показать навыки AQA которыми я владею

Тестируются два сервиса:

| Сервис | Base URL | Что проверяем |
|---|---|---|
| Основное API игры | `https://api.pokemonbattle.ru/v2/` | тренеры, покемоны, битвы, достижения |
| Платёжный сервис «Лавка» | `https://lavka.pokemonbattle.ru/` | покупка и отмена premium-подписки |

---

## ✨ Что интересного внутри

- **Обход rate limiter.** Класс `ApiSession` (`helpers/api_connection_helpers.py`) — обёртка над
  `requests.Session`. Если API отвечает `400 / "Лимит запросов превышен"`, запрос повторяется
  в течение 5 секунд с паузой в 1 секунду. Все запросы проходят через один класс — там же
  централизованное логирование и прикрепление request/response в Allure.
- **Три способа проверки ответа:**
  - `jsonschema` + YAML-схемы из `schemas/` — проверка структуры и типов;
  - `DeepDiff` — точное сравнение ключей и значений с эталоном, с возможностью выкинуть
    нестабильные поля через `exclude_regex_paths`;
  - `pytest-check` — мягкие assert'ы: тест не падает на первой же проверке.
- **Фикстуры с очисткой за собой.** Битва готовит покемона и после теста нокаутирует всех
  созданных; платёжные фикстуры отменяют premium и проверяют, что `is_premium` вернулся в `False`.
- **Фикстура-фабрика** `buy_and_cancel_premium_fail` — возвращает функцию, поэтому один и тот же
  сетап переиспользуется для 4 параметризованных негативных кейсов (нет денег, неверный 3D-secure,
  неверный CVV, номер карты не проходит проверку по Луну).
- **Свой хук `--html-report`** в `conftest.py` — после прогона сам собирает Allure-отчёт одним файлом.

---

## 🗂 Структура проекта

```
pokemonbattle_api_tests/
│
├── tests/                          # 🧪 сами тесты, по одному файлу на раздел API
│   ├── test_trainers_api.py
│   ├── test_pokemons_api.py
│   ├── test_battle_api.py
│   ├── test_achievements_api.py
│   └── test_payments_api.py
│
├── helpers/                        # 🧩 обёртка над requests и методы работы с API
│   ├── api_connection_helpers.py   #    класс ApiSession: обход rate limiter, логи, Allure
│   ├── file_helpers.py             #    load_yaml — подтягивает схему из schemas/
│   ├── pokemons_api_methods.py
│   ├── trainers_api_methods.py
│   └── achievements_api_methods.py
│
├── fixtures/                       # 🔧 фикстуры, подключаются через pytest_plugins в conftest.py
│   ├── connection_fixtures.py      #    сессии с trainer_token в headers
│   ├── battle_fixtures.py          #    подготовка и очистка данных для битвы
│   └── payment_fixtures.py         #    покупка и отмена premium
│
├── data/                           # 📦 тестовые данные
│   ├── api_constants.py            #    id моего тренера
│   └── payment_cards_data.py       #    карты для успешного и неуспешных платежей
│
├── schemas/                        # 📐 json-схемы ответов в формате yml
│   ├── achievements_get.yml
│   └── battle_get.yml
│
├── config/api_config.py            # 🌐 базовые url
├── conftest.py                     # ⚙️ подключение фикстур + хуки pytest
├── pytest.ini                      # ⚙️ markers и addopts
└── .gitlab-ci.yml                  # 🔄 пайплайн: линтеры → тесты → e2e
```

---

## 🧪 Тестовые наборы

| Файл | Suite | Что покрыто |
|---|---|---|
| `tests/test_trainers_api.py` | Trainers | поиск тренеров по городу, по id, сортировка по level на убывание |
| `tests/test_pokemons_api.py` | Pokemons | поиск по id тренера, нокаут всех покемонов, создание, переименование |
| `tests/test_battle_api.py` | Battle | json-схема ответа `GET /battle`, полный сценарий битвы |
| `tests/test_achievements_api.py` | Achievements | сравнение с эталоном через DeepDiff, json-схема, негативный кейс `is_reached=string` → 422 |
| `tests/test_payments_api.py` | Payments | успешная покупка premium + 4 негативных кейса оплаты |

### Маркеры

| Маркер | Назначение |
|---|---|
| `smoke` | быстрые проверки основных ручек |
| `regress` | более глубокие проверки и негативные кейсы |
| `api` | требуется по учебному заданию, используется в GitLab CI (`pytest -m api`) |

---

## 🚀 Установка и запуск

```bash
git clone <repo-url>
cd pokemonbattle_api_tests

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Токен авторизации берётся из `.env` (подхватывается через `pytest-dotenv`):

```dotenv
POKEMON_BATTLE_TOKEN=<твой trainer_token>
```

> `.env` умышленно не добавлен в `.gitignore` — это сделано по заданию в рамках учебного процесса,
> чтобы прогнать тесты в GitLab CI. В реальном проекте так делать нельзя.

Запуск:

```bash
pytest                 # все тесты
pytest -m smoke        # только smoke
pytest -m regress      # только regress
pytest -m api          # то, что гоняется в CI
pytest tests/test_battle_api.py::TestBattle::test__start_battle   # один тест
```

---

## 📊 Команды Allure (установка `pip install allure-pytest`)

Не забываем для простоты прописать `--alluredir=allure-results` в *pytest.ini*.

Не забываем пометить папки `allure-report` и `allure-results` как **Mark Directory as Excluded**,
чтобы они не кешировались, и добавить в *.gitignore*.

- Для генерации отчета allure: `allure generate --clean allure-results/`
- Для генерации 1 файлом: `allure generate --clean --single-file allure-results/`
- Для запуска allure: `allure serve allure-results/`

### Для запуска прогона и генерации отчета allure использовать команду

```bash
pytest --html-report
```

---

## 🔄 GitLab CI

Пайплайн `.gitlab-ci.yml` состоит из трёх стадий:

1. **linters** — `ruff`, `flake8`, `pylint`. Запускаются только на merge request, все с
   `allow_failure: true`. Результат flake8 сохраняется артефактом на 7 дней.
2. **tests** — прогон `pytest -m api` на образе `python:3.12` с последующей генерацией
   single-file Allure-отчёта. Exit code pytest пробрасывается наружу, поэтому падение тестов
   роняет джобу, но отчёт всё равно попадает в артефакты. Параллельно триггерится downstream-пайплайн
   e2e-тестов на Playwright.
3. **final** — ручная финальная джоба.

---

## 🧰 Стек

`pytest` · `requests` · `allure-pytest` · `jsonschema` + `PyYAML` · `deepdiff` · `pytest-check` ·
`pytest-dotenv` · GitLab CI
