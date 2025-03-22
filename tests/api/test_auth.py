from api.api_manager import ApiManager
from models.user_data_model import RegisterUserResponse, LoginUserResponse, LoginData
import json

class TestAuthAPI:

    def test_register_user(self, api_manager: ApiManager,
                           test_user):
        """
        Тест на регистрацию пользователя.
        """
        response = api_manager.auth_api.register_user(user_data=test_user)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == test_user.email, "Email не совпадает"

    def test_register_and_login_user(self, api_manager: ApiManager,
                                     registered_user,
                                     test_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        login_data = {
        "email": test_user.email,
        "password": test_user.password
    }
        response = api_manager.auth_api.login_user(login_data)
        register_user_response = LoginUserResponse(**response.json())

        assert register_user_response.user.email == test_user.email, "Email не совпадает"