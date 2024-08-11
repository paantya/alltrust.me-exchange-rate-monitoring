import pandas as pd
import matplotlib.pyplot as plt
import re

# Путь к CSV файлу
csv_file = '../data/data_log.csv'


def extract_numeric_value(amount_str):
    """
    Функция для извлечения числового значения из строки с валютой.

    Параметры:
    amount_str (str): строка, содержащая числовое значение и текст (например, '123221 USD')

    Возвращаемое значение:
    float: числовое значение из строки (например, 123221.0)
    """

    # Используем регулярное выражение для извлечения числового значения
    match = re.search(r'(\d+\.?\d*)', amount_str)
    return float(match.group(1)) if match else None


# Загрузка данных из CSV файла
df = pd.read_csv(csv_file)

# Преобразование колонки timestamp в формат datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Преобразование minamount и maxamount в числовые значения
df['minamount_numeric'] = df['minamount'].apply(extract_numeric_value)
df['maxamount_numeric'] = df['maxamount'].apply(extract_numeric_value)


def visualize_data_by_to(df):
    """
    Функция для построения и сохранения графиков, отображающих данные по времени и по различным валютным парам (to).

    Параметры:
    df (DataFrame): DataFrame, содержащий данные для визуализации

    Возвращаемое значение:
    None
    """

    # График 1: amount по времени для каждого to
    plt.figure(figsize=(12, 8))
    grouped = df.groupby('to')

    for to_value, group in grouped:
        plt.plot(group['timestamp'], group['amount'], marker='o', label=f'{to_value}')

    plt.xlabel('Время')
    plt.ylabel('Amount')
    plt.title('Значение Amount по времени для разных to')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend(title='to')
    plt.savefig('../plots/amount_by_to.png')  # Сохранение графика
    plt.show()

    # График 2: in по времени для каждого to
    plt.figure(figsize=(12, 8))

    for to_value, group in grouped:
        plt.plot(group['timestamp'], group['in'], marker='o', label=f'{to_value}')

    plt.xlabel('Время')
    plt.ylabel('In')
    plt.title('Значение In по времени для разных to')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend(title='to')
    plt.savefig('../plots/in_by_to.png')  # Сохранение графика
    plt.show()

    # График 3: minamount по времени для каждого to
    plt.figure(figsize=(12, 8))

    for to_value, group in grouped:
        plt.plot(group['timestamp'], group['minamount_numeric'], marker='o', label=f'{to_value}')

    plt.xlabel('Время')
    plt.ylabel('Min Amount (USD)')
    plt.title('Значение Min Amount по времени для разных to')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend(title='to')
    plt.savefig('../plots/minamount_by_to.png')  # Сохранение графика
    plt.show()

    # График 4: maxamount по времени для каждого to
    plt.figure(figsize=(12, 8))

    for to_value, group in grouped:
        plt.plot(group['timestamp'], group['maxamount_numeric'], marker='o', label=f'{to_value}')

    plt.xlabel('Время')
    plt.ylabel('Max Amount (USD)')
    plt.title('Значение Max Amount по времени для разных to')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend(title='to')
    plt.savefig('../plots/maxamount_by_to.png')  # Сохранение графика
    plt.show()


# Вызов функции визуализации
visualize_data_by_to(df)
