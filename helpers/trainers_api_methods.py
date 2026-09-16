from config.api_config import BASE_URL


def find_trainers(api_session, filter_query=None):
    response = api_session.get(BASE_URL + "trainers" + filter_query)
    assert response.status_code == 200
    return response.json()

def put_pokemon_into_pokeball(api_session, pokemon_id):
    response = api_session.post(BASE_URL + "trainers/add_pokeball", json={"pokemon_id": pokemon_id})
    assert response.status_code == 200
    assert response.json()["message"] == "Покемон пойман в покебол"
    assert response.json()["id"] == pokemon_id