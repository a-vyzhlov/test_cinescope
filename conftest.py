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
    response = api_manager.auth_api.register_user(test_user)
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

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

@pytest.fixture()
def corr_params():
    """
        Фикстура для создания корректных фильтров по поиску фильмов.
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

@pytest.fixture()
def incorr_params():
    """
        Фикстура для создания корректных фильтров по поиску фильмов.
    """
    return {
    "locations": "Будапешт", # Несуществующая локация
    "published": "Нет" # Неверные тип данных
}

@pytest.fixture()
def text_error_400():
    """
        Фикстура для создания корректных фильтров по поиску фильмов.
    """
    return {
    "message": "Некорректные данные",
    "error": "Bad Request",
    "statusCode": 400
}

