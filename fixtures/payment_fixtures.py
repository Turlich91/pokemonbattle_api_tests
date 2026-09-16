import allure
import pytest

from config.api_config import LAVKA_URL
from data.api_constants import MY_TRAINER_ID
from data.payment_cards_data import success_card, fail_card
from helpers.trainers_api_methods import find_trainers


@pytest.fixture
@allure.title("Подготовка данных к успешному проведению платежа")
def buy_and_cancel_premium_success(api_payment_session):
    with allure.step("Отправляю запрос на покупку premium"):
        response_buy = api_payment_session.post(LAVKA_URL + "/payments",
                                                json=success_card)
    assert response_buy.status_code == 200
    yield response_buy.json()
    with allure.step("Отправляю запрос на отмену premium"):
        response_cancel = api_payment_session.post(LAVKA_URL + "/cancel_premium")
    assert response_cancel.status_code == 200
    body = response_cancel.json()
    assert body["message"] == "Пользователь потерял премиум"
    assert body["id"] == MY_TRAINER_ID
    trainer_info_body = find_trainers(api_payment_session, f"?trainer_id={MY_TRAINER_ID}")
    assert trainer_info_body["data"][0]["is_premium"] == False


@pytest.fixture
@allure.title("Подготовка данных к неуспешному проведению платежа")
def buy_and_cancel_premium_fail(api_payment_session):
    def _fail_payment(change_cards):
        with allure.step("Отправляю запрос с негативными параметрами на покупку premium"):
            response_buy = api_payment_session.post(LAVKA_URL + "/payments",
                                                    json=change_cards)
        assert response_buy.status_code == 400
        return response_buy.json()
    yield _fail_payment

    with allure.step("Отправляю запрос на отмену premium"):
        response_cancel = api_payment_session.post(LAVKA_URL + "/cancel_premium")
    assert response_cancel.status_code == 400
    with allure.step("Подписка отменена"):
        assert response_cancel.json()["status"] == "error"
        assert response_cancel.json()["message"] == "Подписка уже отменена"
        trainer_info_body = find_trainers(api_payment_session, f"?trainer_id={MY_TRAINER_ID}")
        assert trainer_info_body["data"][0]["is_premium"] == False