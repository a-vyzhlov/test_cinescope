import datetime
import random

import allure
import pytest
from pytz import timezone
from sqlalchemy.orm import Session
from db_requester.models import MovieDBModel, AccountTransactionTemplate, GenreDBModel
from models.movie_data_model import OptionalMovie
from utils.data_generator import DataGenerator


class TestOtherAPI:
    def test_create_delete_movie(self, api_manager, super_admin_token, db_session: Session):

        movie_name = f"Test Movie{DataGenerator.generate_random_str(10)}"
        movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == movie_name)

        # проверяем что до начала тестирования фильма с таким названием нет
        assert movies_from_db.count() == 0, "В базе уже присутствует фильм с таким названием"

        movie_data = OptionalMovie(
            name=movie_name,
            price=500,
            description="Описание тестового фильма",
            location="MSK",
            published=True,
            genreId=3
        )
        response = api_manager.movies_api.create_movie(
            movie_params=movie_data,
            headers={"authorization": f"Bearer {super_admin_token}"}
        )
        assert response.status_code == 201, "Фильм должен успешно создаться"
        response = response.json()

        # проверяем после вызова api_manager.movies_api.create_movie в базе появился наш фильм
        movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == movie_name)
        assert movies_from_db.count() == 1, "В базе уже присутствует фильм с таким названием"

        movie_from_db = movies_from_db.first()
        # Можете обратить внимание, что в базе данных есть поле created_at которое мы не задавали явно
        # Наш сервис сам его заполнил. Проверим что он заполнил его верно с погрешностью в 5 минут
        assert movie_from_db.created_at >= (
                    datetime.datetime.now(timezone('UTC')).replace(tzinfo=None) - datetime.timedelta(
                minutes=5)), "Сервис выставил время создания с большой погрешностью"

        # Берем айди фильма который мы только что создали и удаляем его из базы через апи
        # Удаляем фильм
        delete_response = api_manager.movies_api.delete_movies_id(
            created_movie_id=response["id"],
            headers={"authorization": f"Bearer {super_admin_token}"}
        )
        assert delete_response.status_code == 200, "Фильм должен успешно удалиться"

        # Проверяем что в конце тестирования фильма с таким названием действительно нет в базе
        movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == movie_name)
        assert movies_from_db.count() == 0, "Фильм небыл удален из базы!"

    def test_unprocessed_transaction(self, db_session: Session):
        # ====================================================================== Подготовка к тесту
        # Создаем новые записи в базе данных (чтоб точно быть уверенными что в базе присутствуют данные для тестирования)

        stan = AccountTransactionTemplate(user=f"Stan_{DataGenerator.generate_random_int(10)}", balance=100)
        bob = AccountTransactionTemplate(user=f"Bob_{DataGenerator.generate_random_int(10)}", balance=500)

        # Добавляем записи в сессию
        db_session.add_all([stan, bob])
        # Фиксируем изменения в базе данных
        db_session.commit()

        def transfer_money(session, from_account, to_account, amount):
            # пример функции выполняющей транзакцию
            # представим что она написана на стороне тестируемого сервиса
            # и вызывая метод transfer_money, мы какбудтобы делем запрос в api_manager.movies_api.transfer_money
            """
            Переводит деньги с одного счета на другой.
            :param session: Сессия SQLAlchemy.
            :param from_account_id: ID счета, с которого списываются деньги.
            :param to_account_id: ID счета, на который зачисляются деньги.
            :param amount: Сумма перевода.
            """
            # Получаем счета
            from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
            to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()

            # Проверяем, что на счете достаточно средств
            if from_account.balance < amount:
                raise ValueError("Недостаточно средств на счете")

            # Выполняем перевод
            from_account.balance -= amount
            to_account.balance += amount

            # Сохраняем изменения
            session.commit()

        # ====================================================================== Тест
        # Проверяем начальные балансы
        assert stan.balance == 100
        assert bob.balance == 500

        try:
            # Выполняем перевод 200 единиц от stan к bob
            transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=200)

            # Если перевод прошел успешно, это ошибка
            pytest.fail("Ожидалось исключение 'Недостаточно средств на счете', но перевод прошел успешно")

        except Exception as e:
            assert str(e) == "Недостаточно средств на счете"
            # Если произошла ошибка, откатываем транзакцию
            db_session.refresh(stan)  # Обновляем данные из базы
            db_session.refresh(bob)  # Обновляем данные из базы
            assert stan.balance == 100  # У Стена осталось 100 единиц
            assert bob.balance == 500  # У Боба осталось 500 единиц

        finally:
            # Удаляем данные для тестирования из базы
            db_session.delete(stan)
            db_session.delete(bob)
            # Фиксируем изменения в базе данных
            db_session.commit()

    def test_delete_movie(self, api_manager, super_admin_token, db_session: Session):
        '''
        Тест для удаления фильма
        '''

        # Задайте заранее известный ID существующего фильма
        movie_id = 54

        # Проверяем, существует ли таблица genres и есть ли в ней запись с ID 3
        genre_from_db = db_session.query(GenreDBModel).filter(GenreDBModel.id == "3").first()

        # Если жанра с ID 3 нет, создаем его
        if not genre_from_db:
            new_genre = GenreDBModel(
                id="3",
                name="Test Genre"
            )
            db_session.add(new_genre)
            db_session.commit()

        # Проверяем, существует ли фильм с таким ID в базе данных
        movie_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.id == movie_id).first()

        # Если фильма нет, создаем его
        if not movie_from_db:
            # Создаем новый фильм с указанным ID
            new_movie = MovieDBModel(
                id=movie_id,
                name=f"Movie {DataGenerator.generate_random_str(10)}",
                price=500,
                description="Описание тестового фильма",
                location="MSK",
                published=True,
                genre_id=3,
                rating=5,
                created_at=datetime.datetime.now(timezone('UTC')).replace(tzinfo=None)
            )
            db_session.add(new_movie)
            db_session.commit()

        # Удаляем фильм
        delete_response = api_manager.movies_api.delete_movies_id(
            created_movie_id=movie_id,
            headers={"authorization": f"Bearer {super_admin_token}"}
        )
        assert delete_response.status_code == 200, "Фильм должен успешно удалиться"

        # Проверяем, что фильм действительно удалён
        get_response = api_manager.movies_api.get_movies_id(
            created_movie_id=movie_id,
            expected_status=404
        )
        assert get_response.status_code == 404, "Фильм  не должен существовать"

        # Если фильм был создан в рамках теста, удаляем его из базы
        if not movie_from_db:
            db_session.query(MovieDBModel).filter(MovieDBModel.id == movie_id).delete()
            db_session.commit()

        # Если жанр был создан в рамках теста, удаляем его из базы
        if not genre_from_db:
            db_session.query(GenreDBModel).filter(GenreDBModel.id == "3").delete()
            db_session.commit()


@allure.epic("Тестирование транзакций")
@allure.feature("Тестирование транзакций между счетами")
class TestAccountTransactionTemplateAndOther:

    @allure.story("Корректность перевода денег между двумя счетами")
    @allure.description("""
    Этот тест проверяет корректность перевода денег между двумя счетами.
    Шаги:
    1. Создание двух счетов: Stan и Bob.
    2. Перевод 200 единиц от Stan к Bob.
    3. Проверка изменения балансов.
    4. Очистка тестовых данных.
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Ivan Petrovich")
    @allure.title("Тест перевода денег между счетами 200 рублей")
    def test_accounts_transaction_template(self, db_session: Session):
        # ====================================================================== Подготовка к тесту
        with allure.step("Создание тестовых данных в базе данных: счета Stan и Bob"):
            stan = AccountTransactionTemplate(user=f"Stan_{DataGenerator.generate_random_int(10)}", balance=1000)
            bob = AccountTransactionTemplate(user=f"Bob_{DataGenerator.generate_random_int(10)}", balance=500)
            db_session.add_all([stan, bob])
            db_session.commit()

        @allure.step("Функция перевода денег: transfer_money")
        @allure.description("""
            функция выполняющая транзакцию, имитация вызова функции на стороне тестируемого сервиса
            и вызывая метод transfer_money, мы какбудтобы делем запрос в api_manager.movies_api.transfer_money
            """)
        def transfer_money(session, from_account, to_account, amount):
            with allure.step(" Получаем счета"):
                from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
                to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()

            with allure.step("Проверяем, что на счете достаточно средств"):
                if from_account.balance < amount:
                    raise ValueError("Недостаточно средств на счете")

            with allure.step("Выполняем перевод"):
                from_account.balance -= amount
                to_account.balance += amount

            with allure.step("Сохраняем изменения"):
                session.commit()

        # ====================================================================== Тест
        with allure.step("Проверяем начальные балансы"):
            assert stan.balance == 1000
            assert bob.balance == 500

        try:
            with allure.step("Выполняем перевод 200 единиц от stan к bob"):
                transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=200)

            with allure.step("Проверяем, что балансы изменились"):
                assert stan.balance == 800
                assert bob.balance == 700

        except Exception as e:
            with allure.step("ОШИБКА откаты транзакции"):
                db_session.rollback()

            pytest.fail(f"Ошибка при переводе денег: {e}")

        finally:
            with allure.step("Удаляем данные для тестирования из базы"):
                db_session.delete(stan)
                db_session.delete(bob)
                db_session.commit()

    @allure.title("Тест с перезапусками")
    @pytest.mark.flaky(reruns=3)
    def test_with_retries(delay_between_retries):
        with allure.step("Шаг 1: Проверка случайного значения"):
            result = random.choice([True, False])
            assert result, "Тест упал, потому что результат False"