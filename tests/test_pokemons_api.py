import random
import string

import allure
import pytest

from config.api_config import BASE_URL
from data.api_constants import MY_TRAINER_ID
from helpers.pokemons_api_methods import get_pokemons, knockout_pokemon, create_pokemon


@allure.suite("Тесты Pokemons")
class TestPokemons:

    @allure.title("Тест на поиск покемонов по id тренера")
    @pytest.mark.smoke
    def test__get_pokemon_by_trainer_id(self, api_session):
        with allure.step("Получение списка покемонов по id тренера"):
            body = get_pokemons(api_session, f"?trainer_id={MY_TRAINER_ID}")
        with allure.step("Проверяю что id тренера соответствует искомому"):
            assert body["data"][0]["trainer_id"] == MY_TRAINER_ID

    @allure.title("Тест на нокаутирование всех покемонов по id тренера")
    @pytest.mark.smoke
    def test__knockout_pokemon_list(self, api_session):
        with allure.step("Нокаутируем всех покемонов по id тренера"):
            knockout_pokemon(api_session)
        with allure.step("Проверяем что нет активных покемонов у тренера"):
            body = get_pokemons(api_session, f"?trainer_id={MY_TRAINER_ID}")
            for i in range(0, len(body["data"])):
                assert body["data"][i]["status"] == 0

    @allure.title("Тест на создание покемона")
    @pytest.mark.smoke
    def test__create_pokemon(self, api_session):
        with allure.step("Создаем покемона"):
            id_list: list[str] = []
            body = create_pokemon(api_session)
        with allure.step("Проверяем что в списке всех покемонов тренера есть покемон с id созданного"):
            list_of_pokemons = get_pokemons(api_session, f"?trainer_id={MY_TRAINER_ID}")
            for i in range(0, len(list_of_pokemons["data"])):
                id_list.append(list_of_pokemons["data"][i]["id"])
            assert body["id"] in id_list

    @allure.title("Тест на переименование покемона")
    @pytest.mark.regress
    def test__rename_pokemon(self, api_session):
        gen_new_name: str = ""
        pokemon_new_name: None = None
        pokemon_old_name: None = None
        with allure.step("Переводим всех покемонов тренера в нокаут"):
            knockout_pokemon(api_session)
        with allure.step("Создаем нового покемона и достаем его id"):
            pokemon_before = create_pokemon(api_session)
            pokemon_before_id = pokemon_before["id"]
        with allure.step("Получаем список всех покемонов тренера"):
            pokemons = get_pokemons(api_session, f"?trainer_id={MY_TRAINER_ID}")
        with allure.step("Поиск в списке созданного покемона по id и проверка что его имя не None"):
            for i in range(0, len(pokemons["data"])):
                if pokemons["data"][i]["id"] == pokemon_before_id:
                    pokemon_old_name = pokemons["data"][i]["name"]
            assert pokemon_old_name != None
        with allure.step("Генерируем новое имя покемону"):
            for _ in range(0, 5):
                gen_new_name += random.choice(string.ascii_lowercase)
        with allure.step("Переименовываем созданного покемона"):
            response = api_session.patch(BASE_URL + f"pokemons/{pokemon_before_id}", json={"name": f"{gen_new_name}"})
            assert response.status_code == 200
            body = response.json()
        with allure.step("Проверяю что в ответе у переименованного покемона исходный id"):
            assert body["id"] == pokemon_before_id
            pokemon_after = get_pokemons(api_session, f"?trainer_id={MY_TRAINER_ID}")
        with allure.step("Проверяю что новое имя покемона соответствует сгенерированному имени"):
            for i in range(0, len(pokemon_after["data"])):
                if pokemon_after["data"][i]["id"] == pokemon_before_id:
                    pokemon_new_name = pokemon_after["data"][i]["name"]
            assert pokemon_new_name == gen_new_name
