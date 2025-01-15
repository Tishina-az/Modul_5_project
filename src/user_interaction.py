from typing import Any

from src.db_manager import DBManager


def user_interaction() -> Any:
    """Функция взаимодействия с пользователем"""

    dbm = DBManager()

    print(
        """Выберите интересующую Вас информацию:
    1 - Список компаний, с числом вакансий;
    2 - Список вакансий компаний;
    3 - Средняя зарплата по всем вакансиям;
    4 - Список вакансий, с зарплатой выше среднего;
    5 - Список вакансий, содержащих поисковые слова."""
    )

    while True:
        user_choice = input("Введите число от 1 до 5: ")
        if user_choice.isdigit():
            number = int(user_choice)
            if number == 1:
                return dbm.get_companies_and_vacancies_count()
            elif number == 2:
                return dbm.get_all_vacancies()
            elif number == 3:
                return dbm.get_avg_salary()
            elif number == 4:
                return dbm.get_vacancies_with_higher_salary()
            elif number == 5:
                word = input("Введите слово для поиска: ")
                return dbm.get_vacancies_with_keyword(word)
            else:
                print("Некорректный ввод!")
        else:
            print("Некорректный ввод!")
