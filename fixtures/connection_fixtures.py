import os

import allure
import pytest
import requests

from helpers.api_connection_helpers import ApiSession

@allure.title("Создание сессии")
@pytest.fixture(scope="session")
def api_session():
    with allure.step("Создаем сессию и добавляем в headers значение 'trainer_token'"):
        with requests.Session() as pokemon_session:
            pokemon_session.headers.update({"trainer_token": os.getenv("POKEMON_BATTLE_TOKEN")})
            yield ApiSession(pokemon_session)


@allure.title("Создание платежной сессии")
@pytest.fixture(scope="session")
def api_payment_session():
    with allure.step("Создаем платежную сессию и добавляем в headers значение 'trainer_token'"):
        with requests.Session() as payment_session:
            payment_session.headers.update({"trainer_token": os.getenv("POKEMON_BATTLE_TOKEN")})
            yield ApiSession(payment_session)