import allure
import pytest

from helpers.pokemons_api_methods import knockout_pokemon, create_pokemon
from helpers.trainers_api_methods import put_pokemon_into_pokeball


@pytest.fixture()
@allure.title("Готовлю тестовые данные для битвы")
def prepare_and_clear_battle_data(api_session):
    with allure.step("Перевожу в нокаут всех текущих покемонов"):
        knockout_pokemon(api_session)
    with allure.step("Создаю нового покемона"):
        new_pokemon = create_pokemon(api_session)
        new_pokemon_id = new_pokemon["id"]
    with allure.step("Ловлю покемона в покебол"):
        put_pokemon_into_pokeball(api_session, new_pokemon_id)
    yield int(new_pokemon_id)
    with allure.step("Перевожу в нокаут созданных покемонов"):
        knockout_pokemon(api_session)


