import allure
import pytest

from config.api_config import BASE_URL
from helpers.achievements_api_methods import get_achievements
from helpers.file_helpers import load_yaml
from jsonschema import validate
from deepdiff import DeepDiff


@allure.suite("Тесты Achievements")
class TestAchievements:

    # DeepDiff - подключили через deepdiff. Проверяем конкретно на соответствие ключей и значений
    @pytest.mark.regress
    @allure.title("Тест json ответа на соответствие json макету. Исключаем is_reached из проверки")
    def test__get_achievements_diff(self, api_session):
        with allure.step("Получаем ответ от GET /achievements"):
            body = get_achievements(api_session)
        with allure.step("Сравниваем с файлом образцом, исключаем ключ 'is_reached'"):
            template = {
                'data': [{'slug': 'beginning'}, {'is_reached': False, 'slug': 'out_of_battles'},
                         {'is_reached': False, 'slug': 'self_knockout'}, {'slug': 'max_level'},
                         {'is_reached': False, 'slug': 'one_vs_seven'},
                         {'is_reached': False, 'slug': 'five_battles'},
                         {'is_reached': False, 'slug': 'three_defends'}]}
            # Какие то поля можем выбросить через exclude_regex_paths
            compare = DeepDiff(template, body, exclude_regex_paths=r"root\['data'\]\[\d+\]\['is_reached'\]")
            assert not compare, compare

    @pytest.mark.smoke
    @allure.title("Проверка json схемы ответа на GET /achievements")
    def test__get_achievements_scheme(self, api_session):
        with allure.step("Получаем json схему ответа на GET /achievements"):
            body = get_achievements(api_session)
        with allure.step("Сравниваем с json схемой шаблоном"):
            template = load_yaml("achievements_get.yml")
            validate(body, template)

    # check - Фикстура. Тут мягкое сравнение. Если 1 assert упадет, тест продолжится. Подключили pytest-check
    @pytest.mark.regress
    @allure.title("Проверка GET /achievements в случае отправки туда некорректного значения в поле 'is_reached'")
    def test__get_achievements_by_query_is_reached(self, api_session, check):
        with allure.step("Получаем ошибку 422 в ответе GET /achievements"):
            response = api_session.get(BASE_URL + "achievements" + f"?is_reached=string")
            assert response.status_code == 422
        with allure.step("Проверяем поля 'status' и 'message' тело ответа GET /achievements"):
            body = response.json()
            with check:
                assert body["status"] == "error"
            with check:
                assert body[
                           "message"] == "[{'type': 'bool_parsing', 'loc': ('query', 'is_reached'), 'msg': 'Input should be a valid boolean, unable to interpret input', 'input': 'string'}]"
