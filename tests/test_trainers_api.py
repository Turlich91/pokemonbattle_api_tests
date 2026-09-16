import allure
import pytest

from helpers.trainers_api_methods import find_trainers


@allure.suite("Тесты Trainers")
class TestTrainers:
    city_filter = "Moscow"
    trainer_id = 64577

    @allure.title("Поиск тренеров по городу")
    @pytest.mark.smoke
    def test__find_trainers_by_city_filter(self, api_session):
        with allure.step("Получаем список тренеров из API по фильтру city"):
            body = find_trainers(api_session, f"?city={self.city_filter}")
        with allure.step("Проверяем что в результате у всех тренеров есть искомый город"):
            for i in range(0, len(body["data"])):
                assert body["data"][i]["city"] in (self.city_filter.lower(), self.city_filter.capitalize())

    @allure.title("Тест на поиск тренеров по id")
    @pytest.mark.smoke
    def test__find_trainers_by_id(self, api_session):
        with allure.step("Получаем тренера из API по id"):
            body = find_trainers(api_session, f"/{self.trainer_id}")
        with allure.step("Проверяем что в ответе искомый id тренера"):
            assert body["id"] == str(self.trainer_id)

    @allure.title("Тест на поиск тренеров по городу и сортировка по уровню на убывание")
    @pytest.mark.regress
    def test__find_and_sort_trainers_from_city_by_level_desk(self, api_session):
        with allure.step(
                "Получаем из API отсортированный на убывание по level список тренеров по фильтру city и записываем в переменную"):
            list_of_trainers = find_trainers(api_session, f"?city={self.city_filter}&sort=desc_level")
        with allure.step(
                "В переменной сортируем полученный список по level на убывание"):
            sorted_trainers_list_by_level = sorted(list_of_trainers["data"], key=lambda t: int(t["level"]),
                                                   reverse=True)
        with allure.step("Cравниваем с сортированным ответом от API"):
            assert list_of_trainers["data"] == sorted_trainers_list_by_level
