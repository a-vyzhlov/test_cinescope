from custom_requester.custom_requester import CustomRequester
from constants import BASE_URL_MOVIES, MOVIES_END_POINT

class MoviesAPI(CustomRequester):
    """
      Класс для взаимодействия с сервисом фильмов.
      """
    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL_MOVIES)
        self.session = session

    def get_movies(self, params, expected_status=200):
        return self.send_request(
            method="GET",
            params=params,
            endpoint=MOVIES_END_POINT,
            expected_status=expected_status
        )

    def create_movie(self, movie_params,  expected_status=201):
        return self.send_request(
            method="POST",
            data=movie_params,
            endpoint=MOVIES_END_POINT,
            expected_status=expected_status
        )

    def get_movies_id(self, created_movie,  expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES_END_POINT}/{created_movie['id']}",
            expected_status=expected_status
        )

    def delete_movies_id(self, created_movie,  expected_status=200):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_END_POINT}/{created_movie['id']}",
            expected_status=expected_status
        )