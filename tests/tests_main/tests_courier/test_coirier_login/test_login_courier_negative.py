import allure
import pytest
import requests

from data import API_ENDPOINTS, EXPECTED_RESPONSES

@allure.feature('Логин курьера')
@allure.story('Негативные сценарии')
class TestLoginCourierNegative:

    @pytest.mark.negative
    @allure.title("Логин без поля login")
    def test_courier_login_missing_login_field(self, setup_and_teardown_courier):
        courier = setup_and_teardown_courier
        
        with allure.step('Отправка запроса без login'):
            response = requests.post(
                API_ENDPOINTS["login_courier"],
                json={"password": courier["password"]}
            )

        with allure.step('Проверка статус-кода 400'):
            assert response.status_code == EXPECTED_RESPONSES["login_courier_missing_data_code"], \
                f"Ожидался код {EXPECTED_RESPONSES['login_courier_missing_data_code']}, получен {response.status_code}"

        with allure.step('Проверка сообщения об ошибке'):
            assert response.json().get("message") == EXPECTED_RESPONSES["login_courier_missing_data_message"], \
                "Неверное сообщение об ошибке"

    @pytest.mark.negative
    @allure.title("Логин с пустым полем login")
    def test_courier_login_empty_login(self, setup_and_teardown_courier):
        courier = setup_and_teardown_courier
        
        with allure.step('Отправка запроса с пустым login'):
            response = requests.post(
                API_ENDPOINTS["login_courier"],
                json={"login": "", "password": courier["password"]}
            )

        with allure.step('Проверка статус-кода 400'):
            assert response.status_code == EXPECTED_RESPONSES["login_courier_missing_data_code"], \
                f"Ожидался код {EXPECTED_RESPONSES['login_courier_missing_data_code']}, получен {response.status_code}"

        with allure.step('Проверка сообщения об ошибке'):
            assert response.json().get("message") == EXPECTED_RESPONSES["login_courier_missing_data_message"], \
                "Неверное сообщение об ошибке"

    @pytest.mark.negative
    @allure.title("Логин без поля password")
    def test_courier_login_missing_password_field(self, setup_and_teardown_courier):
        courier = setup_and_teardown_courier
        
        with allure.step('Отправка запроса без password'):
            response = requests.post(
                API_ENDPOINTS["login_courier"],
                json={"login": courier["login"]}
            )

        with allure.step('Проверка статус-кода 400'):
            assert response.status_code == EXPECTED_RESPONSES["login_courier_missing_field_code"], \
                f"Ожидался код {EXPECTED_RESPONSES['login_courier_missing_field_code']}, получен {response.status_code}"

        with allure.step('Проверка текста ответа'):
            assert response.text == EXPECTED_RESPONSES["login_courier_missing_field_message"], \
                "Неверное сообщение об ошибке"

    @pytest.mark.negative
    @allure.title("Логин с пустым паролем")
    def test_courier_login_empty_password(self, setup_and_teardown_courier):
        courier = setup_and_teardown_courier
        
        with allure.step('Отправка запроса с пустым password'):
            response = requests.post(
                API_ENDPOINTS["login_courier"],
                json={"login": courier["login"], "password": ""}
            )

        with allure.step('Проверка статус-кода 400'):
            assert response.status_code == EXPECTED_RESPONSES["login_courier_missing_data_code"], \
                f"Ожидался код {EXPECTED_RESPONSES['login_courier_missing_data_code']}, получен {response.status_code}"

        with allure.step('Проверка сообщения об ошибке'):
            assert response.json().get("message") == EXPECTED_RESPONSES["login_courier_missing_data_message"], \
                "Неверное сообщение об ошибке"

    @pytest.mark.negative
    @allure.title("Логин с несуществующими учетными данными")
    def test_courier_login_nonexistent_credentials(self):
        with allure.step('Отправка запроса с неверными данными'):
            response = requests.post(
                API_ENDPOINTS["login_courier"],
                json={"login": "nonexistent_user", "password": "nonexistent_password"}
            )

        with allure.step('Проверка статус-кода 404'):
            assert response.status_code == EXPECTED_RESPONSES["login_courier_invalid_code"], \
                f"Ожидался код {EXPECTED_RESPONSES['login_courier_invalid_code']}, получен {response.status_code}"

        with allure.step('Проверка сообщения об ошибке'):
            assert response.json().get("message") == EXPECTED_RESPONSES["login_courier_invalid_message"], \
                "Неверное сообщение об ошибке"
