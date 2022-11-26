import csv
import re
from collections import Counter


convert_currency = {
    "AZN": 35.68,
    "BYR": 23.91,
    "EUR": 59.90,
    "GEL": 21.74,
    "KGS": 0.76,
    "KZT": 0.13,
    "RUR": 1,
    "UAH": 1.64,
    "USD": 60.66,
    "UZS": 0.0055,
}


class DataSet:
    def __init__(self, name, spec):
        self.file_name = name
        self.vacancies_objects, self.header = self.csv_reader()
        self.vacancies_objects = self.csv_filer()
        self.speciality = spec
        self.mean_salary = {}
        self.vacancies_count = {}
        self.spec_salary = {}
        self.spec_count = {}
        self.cities_salary = {}
        self.cities_salary_final = {}
        self.cities_vacancies_count = {}
        self.vacancy_fraction = {}


    def clear_string(text):
        text = re.sub(r'\<[^>]*\>', '', text)
        text = text.replace("\xa0", " ")
        text = text.replace(' ', " ")
        text = text.strip()
        text = re.sub(" +", " ", text)
        return text


    def csv_reader(self):
        file = open(self.file_name, encoding="utf-8-sig")
        reader = list(csv.reader(file))
        if not reader:
            print('Пустой файл')
            quit()
        header = reader[0]
        info = [x for x in reader[1:] if '' not in x and len(x) == len(header)]
        if len(info) == 0:
            print('Нет данных')
            quit()
        return info, header


    def csv_filer(self) -> list:
        output = []
        for i in range(len(self.vacancies_objects)):
            vacancy_info = []
            for j in range(len(self.vacancies_objects[i])):
                text = DataSet.clear_string(self.vacancies_objects[i][j])
                vacancy_info.append(text)
            output.append(vacancy_info)
        return output


    def find_year_item(self):
        vacancy_count = 0
        for vacancy in self.vacancies_objects:
            for i in range(len(vacancy)):
                if self.header[i] == 'name':
                    name = vacancy[i]
                if self.header[i] == 'salary_from':
                    salary_from = float(vacancy[i])
                elif self.header[i] == 'salary_to':
                    salary_to = float(vacancy[i])
                elif self.header[i] == 'salary_currency':
                    currency = vacancy[i]
                elif self.header[i] == 'area_name':
                    area = vacancy[i]
                    if area not in self.cities_salary.keys():
                        self.cities_salary[area] = []
                    if area not in self.cities_vacancies_count.keys():
                        self.cities_vacancies_count[area] = 0
                elif self.header[i] == 'published_at':
                    year = int(vacancy[i].split('-')[0])
                    if year not in self.mean_salary.keys():
                        self.mean_salary[year] = []
                    if year not in self.spec_salary.keys():
                        self.spec_salary[year] = []
                    if year not in self.vacancies_count.keys():
                        self.vacancies_count[year] = 0
                    if year not in self.spec_count.keys():
                        self.spec_count[year] = 0
            salary_average = int((salary_from + salary_to) // 2)
            salary_average = int(salary_average * convert_currency[currency])
            self.mean_salary[year].append(salary_average)
            self.cities_salary[area].append(salary_average)
            self.vacancies_count[year] += 1
            if self.speciality in name:
                self.spec_count[year] += 1
                self.spec_salary[year].append(salary_average)
            self.cities_vacancies_count[area] += 1
            vacancy_count += 1
        for year in self.mean_salary:
            if len(self.mean_salary[year]) == 0:
                self.mean_salary[year] = 0
            else:
                self.mean_salary[year] = int(sum(self.mean_salary[year]) // len(self.mean_salary[year]))
        for year in self.spec_salary:
            if len(self.spec_salary[year]) == 0:
                self.spec_salary[year] = 0
            else:
                self.spec_salary[year] = int(sum(self.spec_salary[year]) // len(self.spec_salary[year]))
        for area in self.cities_salary:
            if self.cities_vacancies_count[area] / vacancy_count >= 0.01 and len(self.cities_salary[area]) != 0:
                self.cities_salary_final[area] = int(sum(self.cities_salary[area]) // len(self.cities_salary[area]))
        for area in self.cities_vacancies_count:
            fraction = self.cities_vacancies_count[area] / vacancy_count
            if fraction >= 0.01:
                self.vacancy_fraction[area] = round(fraction, 4)


name = input('Введите название файла: ')
spec = input('Введите название профессии: ')
data_set = DataSet(name, spec)
data_set.find_year_item()
print(f'Динамика уровня зарплат по годам: {data_set.mean_salary}')
print(f'Динамика количества вакансий по годам: {data_set.vacancies_count}')
print(f'Динамика уровня зарплат по годам для выбранной профессии: {data_set.spec_salary}')
print(f'Динамика количества вакансий по годам для выбранной профессии: {data_set.spec_count}')
print(f'Уровень зарплат по городам (в порядке убывания): {dict(Counter(data_set.cities_salary_final).most_common(10))}')
print(f'Доля вакансий по городам (в порядке убывания): {dict(Counter(data_set.vacancy_fraction).most_common(10))}')

'''
vacancies_by_year.csv
Аналитик
'''
