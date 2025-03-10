from faker import Faker
from api.api_manager import ApiManager
import requests
from constants import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
@pytest.fixture(scope="session")
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

# '''До кастомвраппера'''
# @pytest.fixture(scope="session")
# def auth_session(test_user):
#     # Регистрируем нового пользователя
#     register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
#     response = requests.post(register_url, json=test_user, headers=HEADERS)
#     assert response.status_code == 201, "Ошибка регистрации пользователя"
#
#     # Логинимся для получения токена
#     login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
#     login_data = {
#         "email": test_user["email"],
#         "password": test_user["password"]
#     }
#     response = requests.post(login_url, json=login_data, headers=HEADERS)
#     assert response.status_code == 200, "Ошибка авторизации"
#
#     # Получаем токен и создаём сессию
#     token = response.json().get("accessToken")
#     assert token is not None, "Токен доступа отсутствует в ответе"
#
#     session = requests.Session()
#     session.headers.update(HEADERS)
#     session.headers.update({"Authorization": f"Bearer {token}"})
#     return session

@pytest.fixture(scope="session")
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
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
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope='session')
def login_data(test_user):
    return {
        "email": test_user["email"],
        "password": test_user["password"]
    }

@pytest.fixture()
def invalid_login_data(test_user):
    return {
        "email": test_user["email"],
        "password": test_user["password"] + "1"
    }

@pytest.fixture()
def error_401():
    return {"message":"Неверный логин или пароль","error":"Unauthorized","statusCode":401}

@pytest.fixture()
def error_404():
    return {"message":"Пользователь не найден","error":"Not Found","statusCode":404}


@pytest.fixture()
def nonexistent_login_data(test_user):
    return {
        "email": "llllll" + test_user["email"] + "LLLL",
        "password": test_user["password"]
    }

@pytest.fixture()
def error_400():
    return {"message":"Bad Request","error":"Not Found","statusCode":404}

@pytest.fixture()
def empty_login_data(test_user):
    return {}

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