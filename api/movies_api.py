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