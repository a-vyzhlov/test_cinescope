import pytest
import requests
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT,  LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from api.api_manager import ApiManager


class TestAuthAPI:
    # '''До кастомвраппера'''
    # def test_register_user(self, test_user):
    #     # URL для регистрации
    #     register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
    #
    #     # Отправка запроса на регистрацию
    #     response = requests.post(register_url, json=test_user, headers=HEADERS)
    #
    #     # Проверки
    #     assert response.status_code == 201, "Ошибка регистрации пользователя"
    #     response_data = response.json()
    #     assert response_data["email"] == test_user["email"], "Email не совпадает"
    #     assert "id" in response_data, "ID пользователя отсутствует в ответе"
    #     assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
    #
    #     # Проверяем, что роль USER назначена по умолчанию
    #     assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"
    #
    # def test_auth_user(self, auth_session, login_data):
    #     # URL для авторизации
    #     login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    #
    #     response = auth_session.post(login_url, json=login_data)
    #     assert response.status_code == 200, "Ошибка логирования пользователя"
    #     assert response.json().get("accessToken") is not None, "Нет поля accessToken"
    #     assert response.json().get("user") is not None, "Нет поля user"
    #     assert response.json()["user"].get("email") == login_data["email"], "Поле email некорректно"
    #
    # def test_auth_user_with_invalid_password(self, auth_session, invalid_login_data, error_401):
    #     # URL для авторизации
    #     login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    #
    #     response = auth_session.post(login_url, json=invalid_login_data)
    #     assert response.status_code == 401, "Ошибка логирования пользователя"
    #     assert response.json() == error_401, "тело не содержит сообщения об ошибке"
    #
    # def test_auth_user_with_nonexistent_email(self, auth_session, nonexistent_login_data, error_404):
    #     # URL для авторизации
    #     login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    #
    #     response = auth_session.post(login_url, json=nonexistent_login_data)
    #     assert response.status_code == 404, "Ошибка при определении email"
    #     assert response.json() == error_404, "Тело не содержит сообщения об ошибке"
    #
    # def test_auth_user_with_empty_email(self, auth_session, empty_login_data, error_400):
    #     # URL для авторизации
    #     login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    #
    #     response = auth_session.post(login_url, json=empty_login_data)
    #     assert response.status_code == 400, "Статус код не 400"
    #     assert response.json() == error_400, "Тело не содержит сообщения об ошибке"

    def test_register_user(self, api_manager: ApiManager, test_user):
        """
        Тест на регистрацию пользователя.
        """
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        # Проверки
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    def test_register_and_login_user(self, api_manager: ApiManager, registered_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        # Проверки
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"