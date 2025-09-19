import allure
import pytest
import requests

from data.data import API_ENDPOINTS, EXPECTED_RESPONSES

@allure.feature('Удаление курьера')
@allure.story('Негативные сценарии')
class TestDeleteCourierNegative:

    @pytest.mark.negative
    @allure.title("Попытка удаления курьера без указания id")
    def test_delete_courier_without_id(self):
        with allure.step('Отправка запроса на удаление курьера без id'):
            response = requests.delete(API_ENDPOINTS["delete_created_courier"].format(id=""))
        
        with allure.step('Проверка кода ответа и сообщения'):
            assert response.status_code == EXPECTED_RESPONSES["delete_courier_missing_data_code"], \
                f"Ожидался код {EXPECTED_RESPONSES['delete_courier_missing_data_code']}, получен {response.status_code}"
            assert response.json()["message"] == EXPECTED_RESPONSES["delete_courier_missing_data_message"], \
                f"Неверное сообщение об ошибке: {response.json()['message']}"

    @pytest.mark.negative
    @allure.title("Попытка удаления несуществующего курьера")
    def test_delete_nonexistent_courier(self):
        nonexistent_id = 999999
        
        with allure.step(f'Отправка запроса на удаление курьера с id {nonexistent_id}'):
            response = requests.delete(API_ENDPOINTS["delete_created_courier"].format(id=nonexistent_id))
        
        with allure.step('Проверка кода ответа и сообщения'):
            assert response.status_code == EXPECTED_RESPONSES["delete_courier_not_found_code"], \
                f"Ожидался код {EXPECTED_RESPONSES['delete_courier_not_found_code']}, получен {response.status_code}"
            assert response.json()["message"] == EXPECTED_RESPONSES["delete_courier_not_found_message"], \
                f"Неверное сообщение об ошибке: {response.json()['message']}"
