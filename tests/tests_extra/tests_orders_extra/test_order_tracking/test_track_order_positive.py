import allure
import pytest

from data.data import EXPECTED_RESPONSES
from data.helpers import OrderHelper

@allure.feature('Получение заказа по его номеру')
@allure.story('Позитивные сценарии')
class TestGetOrderByTrackPositive:

    @pytest.mark.positive
    @allure.title("Успешное получение заказа по номеру трека")
    def test_get_order_by_track_success(self, setup_and_teardown_order_with_track):
        order_helper = OrderHelper()
        order_track = setup_and_teardown_order_with_track

        with allure.step('Отправка запроса на получение заказа'):
            response = order_helper.get_order_by_track(order_track)

        with allure.step('Проверка ответа сервера'):
            # Проверка статус-кода
            assert response.status_code == EXPECTED_RESPONSES["get_order_by_track_success_code"], \
                f"Ожидался код {EXPECTED_RESPONSES['get_order_by_track_success_code']}, получен {response.status_code}"
            
            # Проверка структуры ответа
            response_json = response.json()
            assert "order" in response_json, "Отсутствует обязательное поле 'order' в ответе"
            assert all(key in response_json["order"] for key in ["id", "track"]), \
                "В ответе отсутствуют обязательные поля заказа: id или track"
