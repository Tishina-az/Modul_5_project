import json
import os.path

import requests


def get_employers_id() -> list:
    """Получение списка ID работодателей из файла"""

    path_to_json = os.path.join(os.path.dirname(__file__), "..", "data", "employers_id.json")
    with open(path_to_json) as file:
        data = json.load(file)
        employers_id = data.get("employers", [])

    return employers_id


def get_employers(employers_id: list) -> list[dict]:
    """Получение информации о работодателях в виде списка словарей"""

    employers = []
    for employer_id in employers_id:
        url = f"https://api.hh.ru/employers/{employer_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            employers.append(
                {
                    "employer_id": data.get("id"),
                    "name": data.get("name"),
                    "area": data.get("area").get("name", "Не указано"),
                    "open_vacancies": data.get("open_vacancies"),
                    "site_url": data.get("site_url"),
                    "description": data.get("description"),
                }
            )
        else:
            raise ValueError(f"Error: {response.status_code} - {response.text}")
    return employers


def get_vacancies(employers_id: list) -> list[dict]:
    """Получение списка вакансий для заданных работодателей"""

    vacancies = []

    url = "https://api.hh.ru/vacancies"
    headers = {"User-Agent": "HH-User-Agent"}
    params = {"employer_id": employers_id, "page": 0, "per_page": 100}

    while params["page"] < 20:
        response = requests.get(url=url, headers=headers, params=params)
        if response.status_code == 200:
            vacancies_list = response.json().get("items", [])
            for data in vacancies_list:
                vacancies.append(
                    {
                        "name": data.get("name"),
                        "employer_id": data.get("employer").get("id"),
                        "area": data.get("area").get("name"),
                        "salary_from": data.get("salary").get("from") if data.get("salary") else None,
                        "salary_to": data.get("salary").get("to") if data.get("salary") else None,
                        "vacancy_url": data.get("alternate_url"),
                    }
                )
            params["page"] += 1
        else:
            raise ValueError(f"Error: {response.status_code} - {response.text}")

    return vacancies


if __name__ == "__main__":
    for vacancy in get_vacancies(get_employers_id()):
        print(vacancy)
    print(len(get_vacancies(get_employers_id())))

    for company in get_employers(get_employers_id()):
        print(company)
