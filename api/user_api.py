from custom_requester.custom_requester import CustomRequester
from constants.constants import BASE_URL_AUTH, USER_ENDPOINT
import json

class UserAPI(CustomRequester):
    """
    Класс для работы с API пользователей.
    """

    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL_AUTH)
        self.session = session

    def get_user(self, user_id, expected_status=200):
        """
        Получение информации о пользователе.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request("GET",f"{USER_ENDPOINT}/{user_id}",expected_status=expected_status)

    def create_user(self, user_data, expected_status=201):
        """
        Получение информации о пользователе.
        :param user_data: Данные пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=USER_ENDPOINT,
            data=json.loads(user_data.model_dump_json(exclude_unset=True)),
            expected_status=expected_status,
            use_json = True
        )

    def delete_user(self, user_id, expected_status=204):
        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"/users/{user_id}",
            expected_status=expected_status
        )
