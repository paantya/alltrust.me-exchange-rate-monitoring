import os
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

# URL для загрузки данных
url = "https://alltrust.me/service/export/xml"

# Путь для сохранения CSV файла
csv_file = '../data/data_log.csv'

# Создаем директорию, если она не существует
os.makedirs(os.path.dirname(csv_file), exist_ok=True)


def fetch_and_save_data():
    """
    Функция для загрузки данных с указанного URL, их парсинга и сохранения в CSV файл.
    Если файл уже существует, новые данные добавляются к существующим.
    Возвращаемое значение:
    None
    """

    response = requests.get(url)

    # Проверка, удалось ли загрузить данные
    if response.status_code == 200:
        xml_data = response.content
        root = ET.fromstring(xml_data)

        data_rows = []

        # Проход по каждому элементу 'item' в XML-данных
        for item in root.findall('.//item'):
            from_tag = item.find('from')
            to_tag = item.find('to')

            # Проверка на соответствие условиям
            if from_tag is not None and to_tag is not None:
                if from_tag.text == 'CASHUSD' and to_tag.text.startswith('USDT'):
                    # Извлечение необходимых полей
                    out_value = item.find('out').text if item.find('out') is not None else None
                    in_value = item.find('in').text if item.find('in') is not None else None
                    amount_value = item.find('amount').text if item.find('amount') is not None else None
                    minamount_value = item.find('minamount').text if item.find('minamount') is not None else None
                    maxamount_value = item.find('maxamount').text if item.find('maxamount') is not None else None
                    city_value = item.find('city').text if item.find('city') is not None else None

                    # Добавление строки данных в список
                    data_rows.append({
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'from': from_tag.text,
                        'to': to_tag.text,
                        'out': out_value,
                        'in': in_value,
                        'amount': amount_value,
                        'minamount': minamount_value,
                        'maxamount': maxamount_value,
                        'city': city_value
                    })

        # Загрузка существующего DataFrame или создание нового
        try:
            df_existing = pd.read_csv(csv_file)
            df_new = pd.DataFrame(data_rows)
            df = pd.concat([df_existing, df_new], ignore_index=True)
        except FileNotFoundError:
            df = pd.DataFrame(data_rows)

        # Сохранение данных в CSV файл
        df.to_csv(csv_file, index=False)
        print(f"Данные сохранены в {csv_file} в {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    else:
        print(f"Не удалось загрузить данные, код ответа: {response.status_code}")


# Вызов функции
fetch_and_save_data()
