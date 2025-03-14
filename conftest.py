import pytest
from api.api_manager import ApiManager
import requests
from constants import BASE_URL_AUTH
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

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
    return [os.getenv('ADMIN_EMAIL'), os.getenv('ADMIN_PASSWORD')]

@pytest.fixture
def movie_filters_for_search():
    """
        Фикстура корректных фильтров по поиску фильмов.
    """
    return {
        "pageSize": 10,
        "page": 1,
        "minPrice": 1,
        "maxPrice": 1000,
        "locations": ["MSK", "SPB"],
        "published": True,
        "genreId": 1,
        "createdAt": "asc"
    }

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
        Фикстура для создания некорректных текста ошибки 400.
    """
    return {
        "message": "Некорректные данные",
        "error": "Bad Request",
        "statusCode": 400
    }


@pytest.fixture
def text_error_401():
    """
        Фикстура для создания некорректных текста ошибки 401.
    """
    return {
        "message": "Unauthorized",
        "statusCode": 401
    }
@pytest.fixture
def text_error_404():
    """
        Фикстура для создания некорректных текста ошибки 404.
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
def movie_params():
    """
        Фикстура для передачи рандомных параметров фильма.
    """
    return DataGenerator.generate_movie_params()

@pytest.fixture
def authenticate_super_admin(api_manager: ApiManager, user_creds):
    """
    Фикстура для аутентификации супер админа.
    """
    return api_manager.auth_api.authenticate(user_creds)

@pytest.fixture
def created_movie(api_manager: ApiManager, movie_params):
    """
    Фикстура для создания и получения данных нового фильма.
    """
    return api_manager.movies_api.create_movie(movie_params).json()

@pytest.fixture
def rand_id():
    """
        Фикстура для передачи рандомного ID фильма.
    """
    return DataGenerator.generate_movie_id()
