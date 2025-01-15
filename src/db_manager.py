from texttable import Texttable

from src.db_create import DataBaseCreate


class DBManager(DataBaseCreate):
    """Класс для подключения к БД PostgreSQL и получения выборок"""

    def __init__(self, db_new_name="hh_ru"):
        """Конструктор класса DBManager"""
        super().__init__(self)
        self.dbname = db_new_name

    @staticmethod
    def tuple_in_table(select_tuple: list[tuple]):
        """Преобразование списка кортежей в табличку, для вывода в консоль"""
        t = Texttable()
        t.add_rows(select_tuple)
        print(t.draw())

    def get_companies_and_vacancies_count(self):
        """Получаем список всех компаний и количество вакансий у каждой компании"""
        query = """SELECT employer_id, name AS company, open_vacancies FROM employers
                    ORDER BY name"""
        result = self.create_execute(query)
        return self.tuple_in_table(result)

    def get_all_vacancies(self):
        """Получаем список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию"""
        query = """SELECT e.name AS company, v.name AS vacancy, v.salary_from, v.salary_to, v.vacancy_url
                            FROM vacancies AS v
                            INNER JOIN employers AS e USING (employer_id)"""
        result = self.create_execute(query)
        return self.tuple_in_table(result)

    def get_avg_salary(self):
        """Получаем среднюю зарплату по вакансиям"""
        query = "SELECT AVG(salary_from) AS salary_avg FROM vacancies"
        result = self.create_execute(query)
        return self.tuple_in_table(result)

    def get_vacancies_with_higher_salary(self):
        """Получаем список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        query = """SELECT e.name AS company, v.name AS vacancy, v.salary_from, v.salary_to, v.vacancy_url
                    FROM vacancies AS v
                    INNER JOIN employers AS e USING (employer_id)
                    WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)
                    ORDER BY salary_from DESC"""
        result = self.create_execute(query)
        return self.tuple_in_table(result)

    def get_vacancies_with_keyword(self, word: str):
        """Получаем список всех вакансий, в названии которых содержатся переданные в метод слова"""
        query = f"""SELECT e.name AS company, v.name AS vacancy, v.salary_from, v.salary_to, v.vacancy_url
                    FROM vacancies AS v
                    INNER JOIN employers AS e USING (employer_id)
                    WHERE v.name LIKE '%{word}%'
                    ORDER BY salary_from DESC NULLS LAST"""
        result = self.create_execute(query)
        return self.tuple_in_table(result)
