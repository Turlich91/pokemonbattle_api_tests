from config.api_config import BASE_URL


def get_achievements(api_session):
    response = api_session.get(BASE_URL + "achievements")
    assert response.status_code == 200
    return response.json()