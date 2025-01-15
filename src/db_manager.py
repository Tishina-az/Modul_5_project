from texttable import Texttable

from src.db_create import DataBaseCreate


class DBManager(DataBaseCreate):
    """ Класс для подключения к БД PostgreSQL и получения выборок """

    def __init__(self, db_new_name='hh_ru'):
        """ Конструктор класса DBManager """
        super().__init__(self)
        self.dbname = db_new_name

    @staticmethod
    def tuple_in_table(select_tuple: list[tuple]):
        """ Преобразование списка кортежей в табличку, для вывода в консоль """
        t = Texttable()
        t.add_rows(select_tuple)
        print(t.draw())

    def get_companies_and_vacancies_count(self):
        """ Получаем список всех компаний и количество вакансий у каждой компании """
        query = """SELECT employer_id, name, open_vacancies FROM employers
                    ORDER BY name"""
        return self.tuple_in_table(self.create_execute(query))


if __name__ == "__main__":
    dbm = DBManager()
    dbm.get_companies_and_vacancies_count()
