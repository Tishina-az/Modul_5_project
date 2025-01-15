import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


class DataBaseCreate:
    """ Класс для создания и заполнения базы данных """

    def __init__(self, db_new_name='hh_ru'):
        """ Конструктор класса """
        self.dbname: str = os.getenv('DB_NAME')
        self.__user: str = os.getenv('DB_USER')
        self.__password: str = os.getenv('DB_PASSWORD')
        self.__host: str = os.getenv('DB_HOST')
        self.__port: str = os.getenv('DB_PORT')
        self.db_new_name: str = db_new_name

    def create_execute(self, query: str, params: tuple = None):
        """ Метод для создания подключения к PostgreSQL и отправке запросов """

        conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.__user,
            password=self.__password,
            host=self.__host,
            port=self.__port
        )
        conn.autocommit = True
        try:
            if 'select'.upper() in query.upper():
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    name_column = [d[0] for d in cursor.description]
                    rows = cursor.fetchall()
                    result = [tuple(name_column)] + rows
            else:
                with conn.cursor() as cursor:
                    result = cursor.execute(query, params)
                    print(f'Успешное выполнение запроса: {query}')
        except psycopg2.Error as e:
            print(f'Ошибка выполнения запроса: {e}')
        finally:
            conn.close()
            return result

    def delete_database(self):
        """ Удаление указанной базы данных, если она существует """
        query = f'DROP DATABASE IF EXISTS {self.db_new_name}'
        self.create_execute(query)

    def create_database(self):
        """ Метод для создания новой базы данных """
        self.delete_database()
        query = f'CREATE DATABASE {self.db_new_name}'
        self.create_execute(query)

    def create_table_employers(self):
        """ Создание таблицы с работодателями """
        self.dbname = self.db_new_name
        query = '''CREATE TABLE IF NOT EXISTS employers
                    (
                        employer_id varchar PRIMARY KEY,
                        name varchar(50) NOT NULL,
                        area varchar(50),
                        open_vacancies int,
                        site_url varchar,
                        description text
                    )'''
        self.create_execute(query)

    def create_table_vacancies(self):
        """ Создание таблицы с работодателями """
        self.dbname = self.db_new_name
        query = '''CREATE TABLE IF NOT EXISTS vacancies
                    (
                        vacancy_id serial PRIMARY KEY,
                        name varchar(100) NOT NULL,
                        employer_id varchar REFERENCES employers(employer_id),
                        area varchar(50),
                        salary_from int,
                        salary_to int,
                        vacancy_url varchar
                    )'''
        self.create_execute(query)

    def fill_table_from_list(self, table_name: str, data_list: list[dict]):
        """ Заполнение таблицы работодателей данными из списка словарей """
        for data in data_list:
            columns = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            query = f'INSERT INTO {table_name} ({columns}) VALUES({values})'
            self.create_execute(query, tuple(data.values()))
