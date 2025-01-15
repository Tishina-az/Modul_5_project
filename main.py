from src.api_query import get_employers, get_employers_id, get_vacancies
from src.db_create import DataBaseCreate
from src.user_interaction import user_interaction


def main() -> None:
    """ Главная функция взаимодействия с пользователем """

    db = DataBaseCreate()
    db.create_database()
    db.create_table_employers()
    db.create_table_vacancies()

    employers_list = get_employers(get_employers_id())
    db.fill_table_from_list('employers', employers_list)

    vacancies_list = get_vacancies(get_employers_id())
    db.fill_table_from_list('vacancies', vacancies_list)

    user_interaction()


if __name__ == "__main__":
    main()
