import allure
import pytest
import requests

from data.data import API_ENDPOINTS, EXPECTED_RESPONSES

@allure.feature('Удаление курьера')
@allure.story('Позитивные сценарии')
class TestDeleteCourierPositive:

    @pytest.mark.positive
    @allure.title("Успешное удаление курьера")
    def test_delete_courier_success(self, courier_for_deletion):
        courier_id = courier_for_deletion

        with allure.step('Отправка запроса на удаление курьера'):
            response = requests.delete(API_ENDPOINTS["delete_created_courier"].format(id=courier_id))

        with allure.step('Проверка ответа сервера'):
            assert response.status_code == EXPECTED_RESPONSES["delete_courier_success_code"], \
                f"Ожидался код {EXPECTED_RESPONSES['delete_courier_success_code']}, получен {response.status_code}"
            assert response.json() == EXPECTED_RESPONSES["delete_courier_success_response"], \
                f"Неверное тело ответа: {response.json()}"
