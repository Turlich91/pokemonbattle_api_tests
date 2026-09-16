# модуль subprocess отвечает за запуск команд операционной системы
import subprocess
pytest_plugins = ["fixtures.connection_fixtures", "fixtures.battle_fixtures", "fixtures.payment_fixtures"]


# Эта функция хук. Она применяется в начале сессии. Parser - это фикстура, которая парсит аргументы в
# коммандной строке и можно добавить свои опции. Это делает метод addoption у parser.addoption
def pytest_addoption(parser):
    parser.addoption(
        "--html-report",
        # Это значит что параметр будет bool. По умолчанию False. Если передаем значение, тогда True
        action="store_true",
        default=False,
        help="Сгенерировать отчет в формате HTML в директорию allure-report"
    )

# В данной функции session это фикстура pytest. У нее есть объект config в котором метод getoption. Он возвращает
# значение опциикомандной строки, которое мы передали при запуске pytest
# Эта функция хук. Она применяется в конце сессии
def pytest_sessionfinish(session):
    # сами сгенерировали команду
    if session.config.getoption("--html-report"):
        # Исходная команда, которую заменяем на --html-report. Между элементами списка будет пробел
        subprocess.call(["allure", "generate", "--clean", "--single-file", "allure-results"])