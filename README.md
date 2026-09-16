# Навигация по проекту pokemonbattle_api_tests

- Тесты находятся тут: *tests/test_pokemonbattle_api.py*

- Тестовые данные тут: *data/api_constants.py*

- Фикстуры тут: *fixtures/api_fixtures.py*

- Базовые url тут: *config/api_config.py*

- Конфиг для запуска фикстур тут: *conftest.py*

- Кастомные метки markers и аргументы для запуска addopts тут: *pytest.ini*

- Схемы ответов тут: */schemas*

- В проекте есть папка helpers с вспомогательными функциями
В file_helpers есть функция *load_yaml* которая облегчает подключение файлов-схем для проверки ответов api
В api_helpers реализован класс ApiSession благодаря которого мы можем обойти rate limiter, проксировать все запросы и 
логировать их


# Команды Allure (установка pip install allure-pytest )

Не забываем для простоты прописать --alluredir=allure-results в pytest.ini
Не забываем пометить папки allure-report и allure-result как Mark Directory as Excluded, чтобы они не кешировались и
добавить в .gitignore

Для генерации отчета allure: *allure generate --clean allure-results/*
Для генерации 1 файлом: *allure generate --clean --single-file allure-results/*
Для запуска allure: *allure serve allure-results/*


# Для запуска прогона и генерации отчета allure использовать команду

pytest --html-report