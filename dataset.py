import xml.etree.ElementTree as ET
import csv
import json
import re
import sys


def read_cvs(file_name, cv_ids):
    columns_info = {
        'localityName': 'Местоположение',
        'positionName': 'Желаемая должность',
        'age': 'Возраст',
        'gender': 'Пол',
        'salary': 'Зарплата',
        'scheduleType': 'Тип расписания',
        'busyType': 'Тип занятости',
        'educationList': 'Образование',
        'experience': 'Опыт работы(года)',
        'workExperienceList': 'Опыт работы'
    }

    def format_list_of_dicts(list_of_dicts):
        """ Форматирует список словарей в текст. """
        return '. '.join(['; '.join([f'{k}: {v}' for k, v in d.items()]) for d in list_of_dicts])

    data = {}
    with open(file_name, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')
        for row in reader:
            if row['id'] in cv_ids:
                text_data = []
                for col in columns_info:
                    if col in ['educationList', 'workExperienceList']:
                        if row[col]:
                            try:
                                list_of_dicts = json.loads(row[col].replace("'", "\""))  # Предполагается, что данные в формате JSON
                                formatted_text = format_list_of_dicts(list_of_dicts)
                                text_data.append(f"{columns_info[col]}: {formatted_text}")
                            except json.JSONDecodeError:
                                pass  # Неверный формат JSON, пропускаем
                    else:
                        if row[col]:
                            text_data.append(f"{columns_info[col]}: {row[col]}")
                text_data = '. '.join(text_data)
                text_data = re.sub(r'\<[^>]*\>', '', text_data)
                data[row['id']] = text_data
    return data


def read_vacancies(file_name, vacancy_ids):
    columns_info = {
        'vacancy_name': 'Название вакансии',
        'busy_type': 'Тип занятости',
        'schedule_type': 'Тип расписания',
        'education': 'Образование',
        'position_requirements': 'Требования к кандидату',
        'position_responsibilities': 'Обязанности',
        'additional_requirements': 'Дополнительные требования',
        'salary': 'Зарплата',
        'vacancy_address': 'Адрес',
        'full_company_name': 'Название компании',
        'professionalSphereName': 'Профессиональная сфера'
    }
    data = {}
    with open(file_name, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')
        for row in reader:
            if row['id'] in vacancy_ids:
                text_data = '. '.join([f"{columns_info[col]}: {row[col]}" for col in columns_info if row[col]])
                text_data = re.sub(r'\<[^>]*\>', '', text_data)
                data[row['id']] = text_data
    return data


maxInt = sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)


# Чтение XML файла с откликами
responses = {}
cv_ids = set()
vacancy_ids = set()
tree = ET.parse('data-20231207T094006-structure-20161130T143000.xml')
root = tree.getroot()

for response in root.findall('.//response'):
    try:
        id_cv = response.find('.//idCv').text
        id_vacancy = response.find('.//idVacancy').text
        response_type = 1 if response.find('.//responseType').text == 'Приглашение' else 0
        responses[(id_cv, id_vacancy)] = response_type
        cv_ids.add(id_cv)
        vacancy_ids.add(id_vacancy)
    except:
        pass

print(len(responses))

# Чтение CSV файла с вакансиями
vacancies = read_vacancies('vacancy.csv', vacancy_ids)
print(len(vacancies))

# Чтение CSV файла с резюме
cvs = read_cvs('cv.csv', cv_ids)
print(len(cvs))

# Сбор данных в кортежи
data_tuples = []
for (id_cv, id_vacancy), response in responses.items():
    if id_cv in cvs and id_vacancy in vacancies:
        data_tuples.append((vacancies[id_vacancy], cvs[id_cv], response))

# Запись данных в csv файл
with open('combined_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='|')
    for data in data_tuples:
        writer.writerow(data)