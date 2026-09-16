import allure
import pytest

from config.api_config import BASE_URL
from data.api_constants import MY_TRAINER_ID
from helpers.file_helpers import load_yaml
from jsonschema import validate
from helpers.pokemons_api_methods import get_pokemons, start_battle


@allure.suite("Тесты Battle")
class TestBattle:
    # Сравниваем ответ с файликом-структурой(схемой). Проверка ключей и типов значений. Подключили через pyyaml
    @pytest.mark.api
    @pytest.mark.smoke
    @allure.title("Проверка json схемы ответа на GET /battle")
    def test__get_battle(self, api_session, filter_query=""):
        response = api_session.get(BASE_URL + "battle" + filter_query)
        assert response.status_code == 200
        body = response.json()
        template = load_yaml("battle_get.yml")
        # Проверка происходит тут
        validate(body, template)

    @pytest.mark.api
    @allure.title("Проверка проведения битвы покемонов")
    def test__start_battle(self, api_session, prepare_and_clear_battle_data):
        with allure.step(
                "Получаю список покемонов готовых к битве(они в покеболах и для вариативности с низкой атакой"):
            body = get_pokemons(api_session, filter_query="?in_pokeball=1&sort=asc_attack")
        with allure.step("Отсортировываю из списка наших покемонов"):
            enemy_pokemons_in_pokeball = [pok for pok in body["data"] if pok["trainer_id"] != MY_TRAINER_ID]
        with allure.step("Получаю id покемона соперника"):
            enemy_pokemons_in_pokeball_id = enemy_pokemons_in_pokeball[0]["id"]
        with allure.step("Провожу битву"):
            result = start_battle(api_session, prepare_and_clear_battle_data, enemy_pokemons_in_pokeball_id)
            battle_id = result["id"]
            battle_result_message = result["result"]
        with allure.step("Получаю результаты битвы по id битвы"):
            response = api_session.get(BASE_URL + f"battle", params={"battle_id": battle_id})
            get_battle_result_body = response.json()
        with allure.step("Проверяю состояние покемонов in_pokeball по результатам битвы"):
            if get_battle_result_body["data"][0]["winner_pokemon"]["id"] == prepare_and_clear_battle_data:
                assert battle_result_message == "Твой покемон победил"
                assert get_battle_result_body["data"][0]["winner_pokemon"]["in_pokeball"] == True
                assert get_battle_result_body["data"][0]["winner_pokemon"]["status"] == True
            elif get_battle_result_body["data"][0]["loser_pokemon"]["id"] == prepare_and_clear_battle_data:
                assert battle_result_message == "Твой покемон проиграл"
                assert get_battle_result_body["data"][0]["loser_pokemon"]["in_pokeball"] == False
                assert get_battle_result_body["data"][0]["loser_pokemon"]["status"] == False
            else:
                pytest.fail(f"Наш покемон {prepare_and_clear_battle_data} не найден в результатах битвы")
