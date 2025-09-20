import allure
import pytest
import requests

from data import API_ENDPOINTS, EXPECTED_RESPONSES
from data.helpers import OrderHelper

@allure.feature('Создание заказа')
@allure.story('Негативные сценарии')
class TestCreateOrderNegative:

    @pytest.mark.negative
    @pytest.mark.parametrize("missing_field", ["firstName", "lastName", "address", "metroStation", "phone", "rentTime", "deliveryDate"])
    @allure.title("Создание заказа без обязательного поля {missing_field}")
    def test_create_order_missing_field(self, missing_field):
        with allure.step(f'Подготовка данных без поля {missing_field}'):
            order_data = OrderHelper.generate_order_without_field(missing_field)

        with allure.step('Отправка запроса на создание заказа'):
            response = requests.post(API_ENDPOINTS["create_order"], json=order_data)

        with allure.step('Проверка ответа сервера'):
            assert response.status_code == EXPECTED_RESPONSES["create_order_missing_field_code"], \
                f"Ожидался код {EXPECTED_RESPONSES['create_order_missing_field_code']}, получен {response.status_code}"
            assert response.json().get("message") == EXPECTED_RESPONSES["create_order_missing_field_message"].format(field=missing_field), \
                "Неверное сообщение об ошибке"

    @pytest.mark.negative
    @pytest.mark.parametrize("empty_field", ["firstName", "lastName", "address", "metroStation", "phone", "rentTime", "deliveryDate"])
    @allure.title("Создание заказа с пустым полем {empty_field}")
    def test_create_order_empty_field(self, empty_field):
        with allure.step(f'Подготовка данных с пустым полем {empty_field}'):
            order_data = OrderHelper.generate_order_with_empty_field(empty_field)

        with allure.step('Отправка запроса на создание заказа'):
            response = requests.post(API_ENDPOINTS["create_order"], json=order_data)

        with allure.step('Проверка ответа сервера'):
            assert response.status_code == EXPECTED_RESPONSES["create_order_empty_field_code"], \
                f"Ожидался код {EXPECTED_RESPONSES['create_order_empty_field_code']}, получен {response.status_code}"
            assert response.json().get("message") == EXPECTED_RESPONSES["create_order_empty_field_message"].format(field=empty_field), \
                "Неверное сообщение об ошибке"
