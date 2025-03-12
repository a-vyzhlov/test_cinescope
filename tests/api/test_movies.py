from api.api_manager import ApiManager


class TestMoviesAPI:

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

    def test_create_movie(self, authenticate_super_admin, api_manager: ApiManager, movie_params):
        """
        Создание нового фильма с роли SUPER_ADMIN.
        """
        response = api_manager.movies_api.create_movie(movie_params)
        response_data = response.json()

        # Проверки
        assert response_data["name"] == movie_params["name"], "Название фильма не совпадает"
        assert "id" in response_data, "ID фильма отсутствует в ответе"
        assert "createdAt" in response_data, "Время создания отсутствует в ответе"

    def test_create_movie_without_authnticate(self, api_manager: ApiManager, movie_params, text_error_401):
        """
        Негативный тест создания фильма без авторизации.
        """
        api_manager.session.headers.pop("Authorization", None)
        response = api_manager.movies_api.create_movie(movie_params, expected_status=401)
        response_data = response.json()

        # Проверки
        assert response_data == text_error_401, "Неверное тело ошибки"

    def test_create_existing_movie(self, authenticate_super_admin, api_manager: ApiManager, movie_params, created_movie, text_error_409):
        """
        Негативный тест создания уже созданного фильма.
        """
        response = api_manager.movies_api.create_movie(movie_params, expected_status=409)
        response_data = response.json()

        # Проверки
        assert response_data == text_error_409, "Неверное тело ошибки"

    def test_create_and_get_movie(self, authenticate_super_admin, api_manager: ApiManager, created_movie):
        """
        Создание нового фильма с роли SUPER_ADMIN.
        """
        response = api_manager.movies_api.get_movies_id(created_movie)
        response_data = response.json()

        # Проверки
        assert response_data["name"] == created_movie["name"], "Название фильма не совпадает"
        assert response_data["genreId"] == created_movie["genreId"], "ID жанра фильма не совпадает"
        assert response_data["description"] == created_movie["description"], "Время создания не совпадает"

    def test_create_and_get_movie_with_nonexisting_id(self, authenticate_super_admin, api_manager: ApiManager, created_movie, rand_id, text_error_404):
        """
        Негативный тест получения фильма с несуществующим ID.
        """
        response = api_manager.movies_api.get_movies_id(rand_id, expected_status=404)
        response_data = response.json()

        # Проверки
        assert response_data == text_error_404, "Неверное тело ошибки"

    def test_create_and_delite_movie(self, authenticate_super_admin, api_manager: ApiManager, created_movie):
        """
        Создание нового фильма с роли SUPER_ADMIN.
        """
        response = api_manager.movies_api.delete_movies_id(created_movie)
        response_data = response.json()

        # Проверки
        assert response_data["name"] == created_movie["name"], "Название фильма не совпадает"
        assert response_data["genreId"] == created_movie["genreId"], "ID жанра фильма не совпадает"
        assert response_data["description"] == created_movie["description"], "Время создания не совпадает"

    def test_create_and_delite_movie(self, authenticate_super_admin, api_manager: ApiManager, created_movie, text_error_401):
        """
        Негативный тест создания нового фильма с роли SUPER_ADMIN, и удаление фильма уже просто юзером.
        """
        api_manager.session.headers.pop("Authorization", None)
        response = api_manager.movies_api.delete_movies_id(created_movie, expected_status=401)
        response_data = response.json()

        # Проверки
        assert response_data == text_error_401, "Неверное тело ошибки"

    def test_create_and_delite_movie_with_nonexisting_id(self, authenticate_super_admin, api_manager: ApiManager, created_movie, rand_id, text_error_404):
        """
        Негативный тест создания нового фильма с роли SUPER_ADMIN и удаления с этой же роли, но фильма с несуществующим ID.
        """
        response = api_manager.movies_api.delete_movies_id(rand_id, expected_status=404)
        response_data = response.json()

        # Проверки
        assert response_data == text_error_404, "Неверное тело ошибки"