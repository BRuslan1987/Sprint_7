import allure
import pytest

from data.data import EXPECTED_RESPONSES
from data.helpers import OrderHelper

@allure.feature('Получение заказа по его номеру')
@allure.story('Негативные сценарии')
class TestGetOrderByTrackNegative:

    @pytest.mark.negative
    @allure.title("Попытка получить заказ без указания номера трека")
    def test_get_order_by_track_without_track(self):
        order_helper = OrderHelper()

        with allure.step('Отправка запроса без номера трека'):
            response = order_helper.get_order_by_track('')

        with allure.step('Проверка ответа сервера'):
            assert response.status_code == EXPECTED_RESPONSES["get_order_by_track_missing_data_code"], \
                f"Ожидался код {EXPECTED_RESPONSES['get_order_by_track_missing_data_code']}, получен {response.status_code}"
            assert response.json().get("message") == EXPECTED_RESPONSES["get_order_by_track_missing_data_message"], \
                f"Неверное сообщение об ошибке: {response.json().get('message', 'Нет сообщения в ответе')}"

    @pytest.mark.negative
    @allure.title("Попытка получить несуществующий заказ")
    def test_get_non_existent_order_by_track(self):
        order_helper = OrderHelper()
        non_existent_track = 999999999

        with allure.step('Отправка запроса с несуществующим треком'):
            response = order_helper.get_order_by_track(non_existent_track)

        with allure.step('Проверка ответа сервера'):
            assert response.status_code == EXPECTED_RESPONSES["get_order_by_track_not_found_code"], \
                f"Ожидался код {EXPECTED_RESPONSES['get_order_by_track_not_found_code']}, получен {response.status_code}"
            assert response.json().get("message") == EXPECTED_RESPONSES["get_order_by_track_not_found_message"], \
                f"Неверное сообщение: {response.json().get('message', 'Нет сообщения в ответе')}"
