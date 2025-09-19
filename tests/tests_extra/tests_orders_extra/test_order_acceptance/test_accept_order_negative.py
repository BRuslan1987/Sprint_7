import allure
import pytest

from data.data import EXPECTED_RESPONSES
from data.helpers import OrderHelper

@allure.feature('Принятие заказа')
@allure.story('Негативные сценарии')
class TestAcceptOrderNegative:

    @pytest.mark.negative
    @allure.title("Попытка принять заказ с несуществующим id заказа")
    def test_accept_order_non_existent_order(self, order_and_courier_setup):
        (_, courier_id) = order_and_courier_setup
        non_existent_order_id = 999999999

        with allure.step('Отправка запроса на принятие несуществующего заказа'):
            response = OrderHelper.accept_order(non_existent_order_id, courier_id)

        with allure.step('Проверка кода ответа и сообщения'):
            assert response.status_code == EXPECTED_RESPONSES["accept_order_not_found_order_code"], \
                f"Ожидался код {EXPECTED_RESPONSES['accept_order_not_found_order_code']}, получен {response.status_code}"
            assert response.json()["message"] == EXPECTED_RESPONSES["accept_order_not_found_order_message"], \
                f"Неверное сообщение: {response.json()['message']}"

    @pytest.mark.negative
    @allure.title("Попытка принять заказ с несуществующим id курьера")
    def test_accept_order_non_existent_courier(self, order_and_courier_setup):
        (order_id, _) = order_and_courier_setup
        non_existent_courier_id = 999999999

        with allure.step('Отправка запроса на принятие заказа несуществующим курьером'):
            response = OrderHelper.accept_order(order_id, non_existent_courier_id)

        with allure.step('Проверка кода ответа и сообщения'):
            assert response.status_code == EXPECTED_RESPONSES["accept_order_not_found_courier_code"], \
                f"Ожидался код {EXPECTED_RESPONSES['accept_order_not_found_courier_code']}, получен {response.status_code}"
            assert response.json()["message"] == EXPECTED_RESPONSES["accept_order_not_found_courier_message"], \
                f"Неверное сообщение: {response.json()['message']}"

    @pytest.mark.negative
    @allure.title("Попытка принять уже принятый заказ")
    def test_accept_already_accepted_order(self, order_and_courier_setup):
        order_id, courier_id = order_and_courier_setup

        with allure.step('Первоначальное принятие заказа'):
            first_response = OrderHelper.accept_order(order_id, courier_id)
            assert first_response.status_code == 200, "Не удалось принять заказ изначально"

        with allure.step('Повторная попытка принятия заказа'):
            response = OrderHelper.accept_order(order_id, courier_id)

        with allure.step('Проверка кода ответа и сообщения'):
            assert response.status_code == EXPECTED_RESPONSES["accept_order_conflict_code"], \
                f"Ожидался код {EXPECTED_RESPONSES['accept_order_conflict_code']}, получен {response.status_code}"
            assert response.json()["message"] == EXPECTED_RESPONSES["accept_order_conflict_message"], \
                f"Неверное сообщение: {response.json()['message']}"
