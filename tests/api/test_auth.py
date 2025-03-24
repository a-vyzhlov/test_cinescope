import datetime

from sqlalchemy.orm import Session
from pytest_mock import mocker
from api.api_manager import ApiManager
from constants.roles import Roles
from db_requester.models import UserDBModel
from models.user_data_model import RegisterUserResponse, LoginUserResponse, LoginData, TestUser
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

    def test_register_user_db_session(self, api_manager: ApiManager, test_user: TestUser, db_session: Session):
        """
        Тест на регистрацию пользователя с проверкой в базе данных.
        """
        # выполняем запрос на регистрацию нового пользователя
        response = api_manager.auth_api.register_user(test_user)
        register_user_response = RegisterUserResponse(**response.json())

        # Проверяем добавил ли сервис Auth нового пользователя в базу данных
        users_from_db = db_session.query(UserDBModel).filter(UserDBModel.id == register_user_response.id)

        # получили объект из бзы данных и проверили что он действительно существует в единственном экземпляре
        assert users_from_db.count() == 1, "объект не попал в базу данных"
        # Достаем первый и единственный объект из списка полученных
        user_from_db = users_from_db.first()
        # Можем осуществить проверку всех полей в базе данных например Email
        assert user_from_db.email == test_user.email, "Email не совпадает"

    def test_register_user_mock(self, api_manager: ApiManager, test_user: TestUser, mocker):
        # Ответ полученный из мок сервиса
        mock_response = RegisterUserResponse(  # Фиктивный ответ
            id="id",
            email="email@email.com",
            fullName="fullName",
            verified=True,
            banned=False,
            roles=[Roles.SUPER_ADMIN],
            createdAt=str(datetime.datetime.now())
        )

        # Мокаем метод register_user в auth_api
        mocker.patch.object(
            api_manager.auth_api,  # Объект, который нужно замокать
            'register_user',  # Метод, который нужно замокать
            return_value=mock_response  # Фиктивный ответ
        )
        # Вызываем метод, который должен быть замокан
        register_user_response = api_manager.auth_api.register_user(test_user)
        # Проверяем, что ответ соответствует ожидаемому
        assert register_user_response.email == mock_response.email, "Email не совпадает"