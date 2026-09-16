from config.api_config import BASE_URL
from data.api_constants import MY_TRAINER_ID


def get_pokemons(api_session, filter_query=""):
    response = api_session.get(BASE_URL + "pokemons" + filter_query)
    assert response.status_code == 200
    return response.json()


def create_pokemon(api_session, name="generate", photo_id=-1):
    response = api_session.post(BASE_URL + "pokemons", json={"name": name, "photo_id": photo_id})
    assert response.status_code == 201
    return response.json()


def knockout_pokemon(api_session, pokemon_id=None):
    if pokemon_id is None:
        active_pokemons = my_active_pokemon_list(api_session)
        if active_pokemons:
            for pok in active_pokemons:
                knockout_pokemon(api_session, pok)
    else:
        response = api_session.post(BASE_URL + "pokemons/knockout", json={"pokemon_id": pokemon_id})
        assert response.status_code == 200


def my_active_pokemon_list(api_session):
    active_pokemons = []
    body = get_pokemons(api_session, f"?trainer_id={MY_TRAINER_ID}")
    for i in range(0, len(body["data"])):
        if body["data"][i]["status"] == 1:
            active_pokemons.append(body["data"][i]["id"])
    return active_pokemons


def start_battle(api_session, my_pokemon_id, enemy_pokemon_id):
    response = api_session.post(BASE_URL + "battle", json={"attacking_pokemon": f"{my_pokemon_id}", "defending_pokemon": f"{enemy_pokemon_id}"})
    assert response.status_code == 200
    return response.json()