import allure
import pytest

from data import EXPECTED_RESPONSES, ORDER_COLORS
from data.helpers import OrderHelper
from data.test_data_generator import generate_order_data

@allure.feature('Создание заказа')
@allure.story('Позитивные сценарии')
class TestCreateOrderPositive:

    @pytest.mark.positive
    @pytest.mark.parametrize("color_combination", list(OrderHelper.powerset(ORDER_COLORS)))
    @allure.title("Создание заказа с комбинацией цветов: {color_combination}")
    def test_create_order_with_color_combinations(self, color_combination):
        order_helper = OrderHelper()
        with allure.step('Подготовка данных заказа'):
            order_data = generate_order_data()
            order_data['color'] = list(color_combination)

        with allure.step('Отправка запроса на создание'):
            response = order_helper.create_order(order_data)

        with allure.step('Проверка статус-кода'):
            assert response.status_code == EXPECTED_RESPONSES["create_order_success_code"], \
                f"Неверный код ответа. Ожидалось: {EXPECTED_RESPONSES['create_order_success_code']}"

        with allure.step('Проверка наличия трек-номера'):
            assert "track" in response.json(), "Отсутствует поле track в ответе"

    @pytest.mark.positive
    @allure.title("Создание заказа без указания цвета")
    def test_create_order_without_colors(self):
        order_helper = OrderHelper()
        with allure.step('Генерация данных без цвета'):
            order_data = generate_order_data()
            order_data.pop('color', None)

        with allure.step('Отправка запроса'):
            response = order_helper.create_order(order_data)

        with allure.step('Проверка успешного ответа'):
            assert response.status_code == EXPECTED_RESPONSES["create_order_success_code"], \
                f"Ожидался код {EXPECTED_RESPONSES['create_order_success_code']}, получен {response.status_code}"
            
        with allure.step('Проверка наличия трека'):
            assert "track" in response.json(), "Трек-номер отсутствует в ответе"
