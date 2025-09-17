import allure
import pytest
import requests

from data.data import API_ENDPOINTS, EXPECTED_RESPONSES

@allure.feature('Удаление курьера')
@allure.story('Негативные сценарии')
class TestDeleteCourierNegative:

    @pytest.mark.negative
    @allure.title("Попытка удаления курьера без указания id - проверка кода ответа")
    def test_delete_courier_without_id_status_code(self):
        with allure.step('Отправка запроса на удаление курьера без id'):
            response = requests.delete(API_ENDPOINTS["delete_created_courier"].format(id=""))
        
        with allure.step('Проверка кода ответа 400'):
            assert response.status_code == EXPECTED_RESPONSES["delete_courier_missing_data_code"], \
                f"Ожидался код 400, получен {response.status_code}"

    @pytest.mark.negative
    @allure.title("Попытка удаления курьера без указания id - проверка сообщения")
    def test_delete_courier_without_id_message(self):
        with allure.step('Отправка запроса на удаление курьера без id'):
            response = requests.delete(API_ENDPOINTS["delete_created_courier"].format(id=""))
        
        with allure.step('Проверка сообщения об ошибке'):
            assert response.json()["message"] == EXPECTED_RESPONSES["delete_courier_missing_data_message"], \
                f"Неверное сообщение об ошибке: {response.json()['message']}"

    @pytest.mark.negative
    @allure.title("Попытка удаления несуществующего курьера - проверка кода ответа")
    def test_delete_nonexistent_courier_status_code(self):
        nonexistent_id = 999999
        
        with allure.step(f'Отправка запроса на удаление курьера с id {nonexistent_id}'):
            response = requests.delete(API_ENDPOINTS["delete_created_courier"].format(id=nonexistent_id))
        
        with allure.step('Проверка кода ответа 404'):
            assert response.status_code == EXPECTED_RESPONSES["delete_courier_not_found_code"], \
                f"Ожидался код 404, получен {response.status_code}"

    @pytest.mark.negative
    @allure.title("Попытка удаления несуществующего курьера - проверка сообщения")
    def test_delete_nonexistent_courier_message(self):
        nonexistent_id = 999999
        
        with allure.step(f'Отправка запроса на удаление курьера с id {nonexistent_id}'):
            response = requests.delete(API_ENDPOINTS["delete_created_courier"].format(id=nonexistent_id))
        
        with allure.step('Проверка сообщения об ошибке'):
            assert response.json()["message"] == EXPECTED_RESPONSES["delete_courier_not_found_message"], \
                f"Неверное сообщение об ошибке: {response.json()['message']}"
