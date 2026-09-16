import allure
import pytest

from data.api_constants import MY_TRAINER_ID
from data.payment_cards_data import fail_card
from helpers.trainers_api_methods import find_trainers


@allure.suite("Тесты Payments")
class TestPayments:
    @pytest.mark.api
    @allure.title("Проверка успешной покупки премиума")
    def test__buy_premium_success(self, api_payment_session, buy_and_cancel_premium_success):
        with allure.step("Получаю данные о покупке"):
            buy_body = buy_and_cancel_premium_success
        with allure.step("Проверяю данные(количество days и message) о покупке"):
            assert buy_body["message"] == "Транзакция успешна"
            assert buy_body["days"] == 10
        with allure.step("Получаю данные о тренере"):
            trainer_info_body = find_trainers(api_payment_session, f"?trainer_id={MY_TRAINER_ID}")
        with allure.step("Проверяю что у тренера 'is_premium' имеет значение True"):
            assert trainer_info_body["data"][0]["is_premium"] == True

    @pytest.mark.parametrize("change_cards, expected_error_message",
                             [(fail_card[0], "Недостаточно средств для оплаты"),
                              (fail_card[1], "Неправильно введен подтверждающий код 3D-secure"),
                              (fail_card[2], "Не верный CVV код для данной карты"),
                              (fail_card[3], "Неправильный номер карты. Ошибка проверки по Luhn")])
    @allure.title("Проверка ошибок при попытках покупки премиума")
    def test__buy_premium_fail(self, api_payment_session, buy_and_cancel_premium_fail, change_cards, expected_error_message):
        with allure.step("Получаю данные платежа"):
            buy_body = buy_and_cancel_premium_fail(change_cards)
            assert buy_body["status"] == "error"
            assert buy_body["message"] == expected_error_message
        with allure.step("Получаю данные о тренере"):
            trainer_info_body = find_trainers(api_payment_session, f"?trainer_id={MY_TRAINER_ID}")
        with allure.step("Проверяю что у тренера 'is_premium' имеет значение True"):
            assert trainer_info_body["data"][0]["is_premium"] == False
