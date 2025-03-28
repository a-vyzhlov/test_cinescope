import random
import string
from faker import Faker

faker = Faker()

class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"


    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"


    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        # Гарантируем наличие хотя бы одной буквы и одной цифры
        letters = random.choice(string.ascii_letters)  # Одна буква
        digits = random.choice(string.digits)  # Одна цифра

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)  # Остальная длина пароля
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_movie_params():
        """
        Генерация обязательных параметров фильмов:
        """
        return {
          "name": faker.catch_phrase(),
          "imageUrl": faker.image_url(),
          "price": random.randint(1, 1000),
          "description": faker.text(max_nb_chars=200),
          "location": random.choice(["MSK", "SPB"]),
          "published": bool(random.randint(0, 1)),
          "genreId": random.randint(1, 10)
        }

    @staticmethod
    def generate_movie_id():
        """
        Генерация рандомного ID фильма:
        """
        return random.randint(100000, 1000000)

    @staticmethod
    def generate_random_str(length: int) -> str:
        """
        Генерирует случайную строку заданной длины.
        """
        # Используем модуль string для получения всех букв (строчных и заглавных) и цифр
        characters = string.ascii_letters + string.digits
        # Генерируем случайную строку, выбирая `length` символов из `characters`
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string

    @staticmethod
    def generate_random_int(length: int) -> int:
        return random.randint(10 ** (length - 1), 10 ** length - 1)