from api.api_manager import ApiManager


class TestAuthAPI:

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

    def test_get_movies_with_correct_filters(self, api_manager: ApiManager, corr_params):
        """
        Позитивный тест на получения списка фильмов.
        """
        response = api_manager.movies_api.get_movies(corr_params)
        response_data = response.json()

        # Проверки
        assert response_data["pageSize"] == corr_params["pageSize"], "pageSize не совпадает"

    def test_get_movies_with_incorrect_filters(self, api_manager: ApiManager, incorr_params, text_error_400):
        """
        Негативный тест на получения списка фильмов.
        """
        response = api_manager.movies_api.get_movies(incorr_params, expected_status=400)
        response_data = response.json()

        # Проверки
        assert response_data == text_error_400, "Неверное тело ошибки"