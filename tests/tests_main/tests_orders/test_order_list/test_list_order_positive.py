import allure
import pytest
import requests

from data import API_ENDPOINTS, EXPECTED_RESPONSES
from data.helpers import OrderParamsHelper

@allure.feature('Получение списка заказов')
@allure.story('Позитивные сценарии')
class TestListOrdersPositive:

    @pytest.mark.positive
    @allure.title("Получение заказов рядом с ближайшей станцией")
    def test_get_orders_with_nearest_station(self, setup_orders_for_list_tests):
        with allure.step('Отправка запроса на получение заказов рядом со станцией'):
            params = OrderParamsHelper.get_station_orders_params(setup_orders_for_list_tests)
            response = requests.get(API_ENDPOINTS["list_orders"], params=params)

        with allure.step('Проверка ответа'):
            assert response.status_code == EXPECTED_RESPONSES["get_orders_list_success_code"], \
                f"Неверный код ответа. Ожидалось: {EXPECTED_RESPONSES['get_orders_list_success_code']}"
            assert OrderParamsHelper.check_response(
                response,
                EXPECTED_RESPONSES["get_orders_list_success_code"],
                EXPECTED_RESPONSES["get_orders_list_success_response"]
            ), "Некорректное тело ответа"

    @pytest.mark.positive
    @allure.title("Получение заказов с ID курьера и станцией (успешный сценарий)")
    def test_get_orders_with_courier_id_and_station_success(self, setup_orders_for_list_tests):
        with allure.step('Отправка запроса на получение заказов с ID курьера и станцией'):
            params = OrderParamsHelper.get_courier_station_orders_params(setup_orders_for_list_tests)
            response = requests.get(API_ENDPOINTS["list_orders"], params=params)

        with allure.step('Проверка успешного ответа'):
            assert response.status_code == EXPECTED_RESPONSES["get_orders_list_success_code"], \
                f"Ожидался код {EXPECTED_RESPONSES['get_orders_list_success_code']}"
            assert OrderParamsHelper.check_response(
                response,
                EXPECTED_RESPONSES["get_orders_list_success_code"],
                EXPECTED_RESPONSES["get_orders_list_success_response"]
            ), "Некорректное тело ответа"

    @pytest.mark.positive
    @allure.title("Получение заказов с ID курьера и станцией (ошибка сервера)")
    def test_get_orders_with_courier_id_and_station_server_error(self, setup_orders_for_list_tests):
        with allure.step('Отправка запроса на получение заказов с ID курьера и станцией'):
            params = OrderParamsHelper.get_courier_station_orders_params(setup_orders_for_list_tests)
            response = requests.get(API_ENDPOINTS["list_orders"], params=params)

        with allure.step('Проверка ошибки сервера'):
            assert response.status_code == 500, f"Ожидалась ошибка 500, получен код {response.status_code}"
            allure.attach("Сервер вернул ошибку 500", "Предупреждение", allure.attachment_type.TEXT)

    @pytest.mark.positive
    @allure.title("Получение заказов с лимитом и номером страницы")
    def test_get_orders_with_limit_and_page(self, setup_orders_for_list_tests):
        with allure.step('Отправка запроса на получение заказов с лимитом и номером страницы'):
            params = OrderParamsHelper.get_limit_page_orders_params()
            response = requests.get(API_ENDPOINTS["list_orders"], params=params)

        with allure.step('Проверка ответа'):
            assert response.status_code == EXPECTED_RESPONSES["get_orders_list_success_code"], \
                f"Неверный код ответа. Ожидалось: {EXPECTED_RESPONSES['get_orders_list_success_code']}"
            assert OrderParamsHelper.check_response(
                response,
                EXPECTED_RESPONSES["get_orders_list_success_code"],
                EXPECTED_RESPONSES["get_orders_list_success_response"]
            ), "Некорректное тело ответа"
