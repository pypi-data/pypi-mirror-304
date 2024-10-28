import pandas as pd

def generate_report(input_file: str, output_file: str):
    # Загружаем данные из CSV
    data = pd.read_csv(input_file)

    total_clients = len(data)

    # Определяем возрастные группы
    bins = [18, 26, 36, 46, 61]
    labels = ['18-25', '26-35', '36-45', '46-60']
    data['age_group'] = pd.cut(data['age'], bins=bins, labels=labels, right=False)

    # Генерируем распределение по возрастным группам
    age_distribution = data['age_group'].value_counts().sort_index()

    # Генерируем распределение по городам
    city_distribution = data['city'].value_counts()

    # Создаем отчет
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f'Общее количество клиентов: {total_clients}\n\n')
        f.write('Количество клиентов по возрастным группам:\n')
        for group, count in age_distribution.items():
            f.write(f'{group}: {count}\n')
        
        f.write('\nРаспределение клиентов по городам:\n')
        for city, count in city_distribution.items():
            f.write(f'{city}: {count}\n')
