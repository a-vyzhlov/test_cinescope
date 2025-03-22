# '''Напишите функцию greet, которая принимает именованные аргументы и выводит приветствие.'''
# def greet(**kwargs):
#     name = kwargs.get("name", "Guest")  # Если name не передан, используем "Guest"
#     age = kwargs.get("age", "unknown")  # Если age не передан, используем "unknown"
#     greeting = f"Hello, {name}! You are {age} years old."
#     print(greeting)
#
#
# greet(name="Alice", age=25)

# '''Создайте функцию create_dict, которая принимает произвольное количество именованных аргументов и возвращает их в виде словаря.'''
# def create_dict(**kwargs):
#     return kwargs
#
# print(create_dict(a=1, b=2, c=3))

# '''Напишите функцию update_settings, которая принимает базовые настройки в виде словаря и обновляет их с помощью дополнительных аргументов.'''
# def update_settings(settings, **kwargs):
#     new_settings = settings.copy()  # Создаем копию исходного словаря
#     new_settings.update(kwargs)
#     return new_settings
#
# default_settings = {"theme": "light", "notifications": True}
# print(update_settings(default_settings, theme="dark", volume=80))

# '''Создайте функцию filter_kwargs, которая принимает именованные аргументы и возвращает только те, где значения больше 10.'''
# def filter_kwargs(**kwargs):
#     filtered = {key: value for key, value in kwargs.items() if value > 10}
#     return filtered
#
# print(filter_kwargs(a=5, b=20, c=15, d=3))


# '''Создайте декоратор log_kwargs, который выводит все именованные аргументы, переданные в декорируемую функцию.'''
# def log_kwargs(func):
#     def wrapper(*args, **kwargs):
#         # Выводим все именованные аргументы
#         print("Именованные аргументы:", kwargs)
#         # Вызываем декорируемую функцию
#         return func(*args, **kwargs)
#     return wrapper
#
# # Пример использования декоратора
# @log_kwargs
# def my_function(a, b, **kwargs):
#     return a + b
#
# result = my_function(5, 10, debug=True, verbose=False)
# print("Результат функции:", result)

# '''Напишите функцию add_numbers, которая принимает произвольное количество чисел и возвращает их сумму.'''
# def add_numbers(*args):
#     return sum(args)
#
# print(add_numbers(1, 2, 3))

# '''Создайте функцию create_list, которая принимает произвольное количество элементов и возвращает их в виде списка.'''
# def create_list(*args):
#     return list(args)
#
# print(create_list(1, "apple", True, 3.14))

# '''Создайте функцию pass_arguments, которая принимает любые аргументы и передает их другой функции, например, print_args.'''
# def print_args(*args):
#     for arg in args:
#         print(arg)
#
# def pass_arguments(*args):
#     print_args(*args)
#
# pass_arguments("Hello", 42, False)


# '''Напишите функцию find_max, которая принимает произвольное количество чисел и возвращает максимальное значение.'''
# def find_max(*args):
#     return max(args)
#
# print(find_max(10, 20, 5, 100, 50))

# '''Напишите функцию join_strings, которая принимает произвольное количество строк и объединяет их через пробел.'''
# def join_strings(*args):
#     return " ".join(args)
#
# print(join_strings("Hello", "world", "!"))

# '''Напишите функцию process_data, которая принимает произвольное количество позиционных и именованных аргументов, выводя их отдельно.'''
# def process_data(*args, **kwargs):
#     print("Positional arguments:", args)
#     print("Keyword arguments:", kwargs)
#
# process_data(1, 2, 3, name="Alice", age=25)

# '''Создайте функцию configure_function, которая принимает настройки через *args (ключи) и **kwargs (значения), возвращая словарь настроек.'''
# def configure_function(*args, **kwargs):
#     settings = {}
#     for key in args:
#         if key in kwargs:
#             settings[key] = kwargs[key]
#     return settings
#
#
# print(configure_function("theme", "volume", theme="dark", volume=50))

# def squares(n):
#     for i in range(n):
#         yield i ** 2
#
# square = list(squares(5))
# print(square)
#
#
# from typing import Optional, Union
#
# def multiply(a: int, b: int) -> int:
#     return a * b
#
# def sum_numbers(numbers: list[int]) -> int:
#     return sum(numbers)
#
# def find_user(user_id: int) -> Optional[str]:
#     if user_id == 1:
#         return "Пользователь найден"
#     return None
#
# def process_input(value: Union[int, str]) -> str:
#     return f"Ты передал: {value}"
#
#
# class User:
#     def __init__(self, name: str, age: int):
#         self.name = name
#         self.age = age
#
#     def greet(self) -> str:
#         return f"Привет, меня зовут {self.name}!"
#
# def get_even_numbers(numbers: list[int]) -> list:
#     return [num for num in numbers if num % 2 == 0]
#
# if __name__ == '__main__':
#     print(get_even_numbers(['1','2','3','4','5','6']))