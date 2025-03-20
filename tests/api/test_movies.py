from api.api_manager import ApiManager
from conftest import common_user


class TestMoviesAPI:

    def test_get_movies_with_filters(self, common_user,
                                             movie_filters_for_search):
        """
        Позитивный тест на получения списка фильмов.
        """
        response = common_user.api.movies_api.get_movies(movie_filters_for_search)
        response_data = response.json()

        assert response_data["pageSize"] == movie_filters_for_search["pageSize"], "pageSize не совпадает"

    def test_get_movies_with_incorrect_filters(self, super_admin,
                                               incorrect_movie_filters_for_search,
                                               text_error_400):
        """
        Негативный тест на получения списка фильмов.
        """
        response = super_admin.api.movies_api.get_movies(incorrect_movie_filters_for_search, expected_status=400)
        response_data = response.json()

        assert response_data == text_error_400, "Неверное тело ошибки"

    def test_create_movie(self, super_admin,
                          movie_params):
        """
        Создание нового фильма с роли SUPER_ADMIN.
        """
        response = super_admin.api.movies_api.create_movie(movie_params)
        response_data = response.json()

        assert response_data["name"] == movie_params["name"], "Название фильма не совпадает"
        assert "id" in response_data, "ID фильма отсутствует в ответе"
        assert "createdAt" in response_data, "Время создания отсутствует в ответе"

    def test_create_movie_without_authenticate(self, api_manager: ApiManager,
                                               movie_params,
                                               text_error_401):
        """
        Негативный тест создания фильма без авторизации.
        """
        response = api_manager.movies_api.create_movie(movie_params, expected_status=401)
        response_data = response.json()

        assert response_data == text_error_401, "Неверное тело ошибки"

    def test_create_existing_movie(self, super_admin,
                                   created_movie,
                                   movie_params,
                                   text_error_409):
        """
        Негативный тест создания уже созданного фильма.
        """
        response = super_admin.api.movies_api.create_movie(movie_params, expected_status=409)
        response_data = response.json()

        assert response_data == text_error_409, "Неверное тело ошибки"

    def test_create_and_get_movie(self, super_admin,
                                  created_movie,
                                  movie_params):
        """
        Создание нового фильма с роли SUPER_ADMIN и получения фильма.
        """
        response = super_admin.api.movies_api.get_movies_id(created_movie["id"])
        response_data = response.json()

        assert response_data["name"] == movie_params["name"], "Название фильма не совпадает"
        assert response_data["genreId"] == movie_params["genreId"], "ID жанра фильма не совпадает"
        assert response_data["description"] == movie_params["description"], "Время создания не совпадает"

    def test_create_and_get_movie_with_nonexisting_id(self, super_admin,
                                                      created_movie,
                                                      rand_id,
                                                      text_error_404):
        """
        Негативный тест получения фильма с несуществующим ID.
        """
        response = super_admin.api.movies_api.get_movies_id(rand_id, expected_status=404)
        response_data = response.json()

        assert response_data == text_error_404, "Неверное тело ошибки"

    def test_create_and_delite_movie(self, super_admin,
                                     created_movie,
                                     movie_params):
        """
        Создание нового фильма с роли SUPER_ADMIN.
        """
        response = super_admin.api.movies_api.delete_movies_id(created_movie["id"])
        response_data = response.json()

        assert response_data["name"] == movie_params["name"], "Название фильма не совпадает"
        assert response_data["genreId"] == movie_params["genreId"], "ID жанра фильма не совпадает"
        assert response_data["description"] == movie_params["description"], "Время создания не совпадает"

    def test_create_and_delite_movie(self, common_user,
                                     created_movie,
                                     movie_params,
                                     text_error_403):
        """
        Негативный тест создания нового фильма с роли SUPER_ADMIN, и удаление фильма уже просто юзером.
        """
        response = common_user.api.movies_api.delete_movies_id(created_movie["id"], expected_status=403)
        response_data = response.json()

        assert response_data == text_error_403, "Неверное тело ошибки"

    def test_create_and_delite_movie_with_nonexisting_id(self, super_admin,
                                                         created_movie,
                                                         rand_id,
                                                         text_error_404):
        """
        Негативный тест создания нового фильма с роли SUPER_ADMIN и удаления с этой же роли, но фильма с несуществующим ID.
        """
        response = super_admin.api.movies_api.delete_movies_id(rand_id, expected_status=404)
        response_data = response.json()

        assert response_data == text_error_404, "Неверное тело ошибки"