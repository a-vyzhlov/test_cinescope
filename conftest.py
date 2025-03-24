import datetime
import time

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.api_manager import ApiManager
import requests
from constants.roles import Roles
from db_requester.models import UserDBModel
from entities.user import User
from constants.constants import BASE_URL_AUTH
from custom_requester.custom_requester import CustomRequester
from models.movie_data_model import OptionalMovie, Movie
from utils.data_generator import DataGenerator
from models.user_data_model import TestUser
from dotenv import load_dotenv
import os


load_dotenv()
class SuperAdminCreds:
    USERNAME = os.getenv('SUPER_ADMIN_USERNAME')
    PASSWORD = os.getenv('SUPER_ADMIN_PASSWORD')

HOST = os.getenv('DB_HOST')
PORT = int(os.getenv('DB_PORT'))
DATABASE_NAME = os.getenv('DB_NAME')
USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')

engine = create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db_session():
    """
    Фикстура с областью видимости module.
    Тестовые данные создаются один раз для всех тестов в модуле.
    """
    session = SessionLocal()

    # Уникальный ID для тестового пользователя
    test_user_id = f"test_id_{DataGenerator.generate_random_str(5)}"

    test_user = session.query(UserDBModel).filter(UserDBModel.id == test_user_id).first()

    # Если пользователя нет, создаем его
    if not test_user:
        test_user = UserDBModel(
            id=test_user_id,
            email=DataGenerator.generate_random_email(),
            full_name=DataGenerator.generate_random_name(),
            password=DataGenerator.generate_random_password(),
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            verified=False,
            banned=False,
            roles="{USER}"
        )
        session.add(test_user)
        session.commit()

    yield session # можете запустить тесты в дебаг режиме и поставить тут брекпойнт
                  # зайдите в базу и убедитесь что новый объект был создан

		# код ниже выполнится после всех запущенных тестов
    session.delete(test_user) # Удаляем тестовые данные
    session.commit() # сохраняем изменения для всех остальных подключений
    session.close() # завершаем сессию (отключаемся от базы данных)


@pytest.fixture
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )

@pytest.fixture
def registered_user(api_manager: ApiManager, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    return api_manager.auth_api.register_user(test_user).json()

@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL_AUTH)

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)


@pytest.fixture(scope="session")
def user_creds():
    """
        Фикстура для передачи учетных данных ADMIN из .env.
    """
    return [os.getenv('SUPER_ADMIN_USERNAME'), os.getenv('SUPER_ADMIN_PASSWORD')]

@pytest.fixture
def incorrect_movie_filters_for_search():
    """
        Фикстура для создания корректных фильтров по поиску фильмов.
    """
    return {
        "locations": "Будапешт", # Несуществующая локация
        "published": "Нет" # Неверные тип данных
}

@pytest.fixture
def text_error_400():
    """
        Фикстура для создания некорректного текста ошибки 400.
    """
    return {
        "message": "Некорректные данные",
        "error": "Bad Request",
        "statusCode": 400
    }


@pytest.fixture
def text_error_401():
    """
        Фикстура для создания некорректного текста ошибки 401.
    """
    return {
        "message": "Unauthorized",
        "statusCode": 401
    }


@pytest.fixture
def text_error_403():
    """
        Фикстура для создания некорректного текста ошибки 403.
    """
    return  {
        "message": "Forbidden resource",
        "error": "Forbidden",
        "statusCode": 403
    }
@pytest.fixture
def text_error_404():
    """
        Фикстура для создания некорректного текста ошибки 404.
    """
    return {
        "message": "Фильм не найден",
        "error": "Not Found",
        "statusCode": 404
    }

@pytest.fixture
def text_error_409():
    """
        Фикстура для создания некорректных текста ошибки 409.
    """
    return {
        'error': 'Conflict',
        'message': 'Фильм с таким названием уже существует',
        'statusCode': 409
    }

@pytest.fixture
def movie_params() -> OptionalMovie:
    """
        Фикстура для передачи рандомных параметров фильма.
    """
    dict_filters = DataGenerator.generate_movie_params()
    return OptionalMovie(
          name=dict_filters.get('name'),
          imageUrl=dict_filters.get('imageUrl'),
          price=dict_filters.get('price'),
          description=dict_filters.get('description'),
          location=dict_filters.get('location'),
          published=dict_filters.get('published'),
          genreId=dict_filters.get('genreId')
        )

@pytest.fixture
def authenticate_super_admin(api_manager: ApiManager, user_creds):
    """
    Фикстура для аутентификации супер админа.
    """
    return api_manager.auth_api.authenticate(user_creds)

@pytest.fixture
def created_movie(super_admin, movie_params) -> Movie:
    """
    Фикстура для создания и получения данных нового фильма.
    """
    return Movie(**super_admin.api.movies_api.create_movie(movie_params).json())

@pytest.fixture
def rand_id():
    """
        Фикстура для передачи рандомного ID фильма.
    """
    return DataGenerator.generate_movie_id()

@pytest.fixture
def user_session():
    """
        Фикстура для создания сессии юзера
    """
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    """
        Фикстура для создания user с правами SUPER_ADMIN
    """
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture
def common_user(user_session, super_admin, registration_user_data: TestUser):
    new_session = user_session()

    common_user = User(
        registration_user_data.email,
        registration_user_data.password,
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(registration_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def admin_user(user_session, super_admin, registration_user_data):
    new_session = user_session()

    admin_user = User(
        registration_user_data.email,
        registration_user_data.password,
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(registration_user_data)
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user

@pytest.fixture(scope="function")
def registration_user_data()-> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value],
        verified= True,
        banned= False
    )

@pytest.fixture()
def super_admin_token(api_manager: ApiManager, user_creds) -> str:
    return api_manager.auth_api.authenticate(user_creds, for_token = True)

@pytest.fixture()
def delay_between_retries():
    time.sleep(2)  # Задержка в 2 секунды
    yield