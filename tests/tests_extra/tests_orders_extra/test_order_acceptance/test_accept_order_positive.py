import allure
import pytest

from data.data import EXPECTED_RESPONSES
from data.helpers import OrderHelper

@allure.feature('Принятие заказа')
@allure.story('Позитивные сценарии')
class TestAcceptOrderPositive:

    @allure.title("Успешное принятие заказа")
    @pytest.mark.positive
    def test_accept_order_success(self, order_and_courier_setup):
        order_id, courier_id = order_and_courier_setup

        with allure.step('Отправка запроса на принятие заказа'):
            response = OrderHelper.accept_order(order_id, courier_id)

        with allure.step('Проверка ответа сервера'):
            assert response.status_code == EXPECTED_RESPONSES["accept_order_success_code"], \
                f"Ожидался код {EXPECTED_RESPONSES['accept_order_success_code']}, получен {response.status_code}"
            assert response.json() == EXPECTED_RESPONSES["accept_order_success_response"], \
                f"Неверное тело ответа: {response.json()}"
