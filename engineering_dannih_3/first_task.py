import os
import json
from bs4 import BeautifulSoup
from collections import Counter

folder_path = "data/1"

def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    data = {}
    try:
        type_div = soup.find('span', string=lambda t: t and 'Тип:' in t)
        data['type'] = type_div.text.split(':')[-1].strip().replace("\n", " ") if type_div else None

        title_element = soup.find('h1', class_='title')
        if title_element:
            tournament_text = title_element.text.split(':')
            data['tournament'] = tournament_text[-1].strip().replace("\n", " ") if len(tournament_text) > 1 else None

        address_p = soup.find('p', class_='address-p')
        if address_p:
            city_text = address_p.text.split('Город:')
            data['city'] = city_text[-1].split('Начало:')[0].strip().replace("\n", " ") if len(city_text) > 1 else None
            start_date_text = address_p.text.split('Начало:')
            data['start_date'] = start_date_text[-1].strip().replace("\n", " ") if len(start_date_text) > 1 else None

        rounds_div = soup.find('div', string=lambda t: t and 'Количество туров:' in t)
        if not rounds_div:  
            rounds_div = soup.find('span', class_='count')
        data['rounds'] = rounds_div.text.split(':')[-1].strip().replace("\n", " ") if rounds_div else None

        time_control_div = soup.find('div', string=lambda t: t and 'Контроль времени:' in t)
        if not time_control_div:  
            time_control_div = soup.find('span', class_='year')
        data['time_control'] = time_control_div.text.split(':')[-1].strip().replace("\n", " ") if time_control_div else None

        min_rating_div = soup.find('div', string=lambda t: t and 'Минимальный рейтинг' in t)
        if not min_rating_div:  # Если текст в отдельном span
            min_rating_div = soup.find('span', string=lambda t: t and 'Минимальный рейтинг' in t)
        data['min_rating'] = min_rating_div.text.split(':')[-1].strip().replace("\n", " ") if min_rating_div else None

        image_element = soup.find('img')
        data['image'] = image_element['src'].replace("\n", " ") if image_element else None

        rating_span = soup.find('span', string=lambda t: t and 'Рейтинг:' in t)
        data['rating'] = rating_span.text.split(':')[-1].strip().replace("\n", " ") if rating_span else None

        views_span = soup.find('span', string=lambda t: t and 'Просмотры:' in t)
        data['views'] = views_span.text.split(':')[-1].strip().replace("\n", " ") if views_span else None

    except Exception as e:
        print(f"Ошибка: {file_path}: {e}")

    return data

parsed_data = []
for file_name in os.listdir(folder_path):
    if file_name.endswith(".html"):
        file_path = os.path.join(folder_path, file_name)
        parsed_data.append(parse_html(file_path))

sorted_data = sorted(parsed_data, key=lambda x: float(x['rating']) if x['rating'] else 0, reverse=True)

filtered_data = [item for item in sorted_data if item['min_rating'] and int(item['min_rating']) >= 2500]

views = [int(item['views']) for item in sorted_data if item['views']]
statistics = {
    "total_views": sum(views),
    "min_views": min(views),
    "max_views": max(views),
    "average_views": sum(views) / len(views) if views else 0
}

types = [item['type'] for item in sorted_data if item['type']]
type_counts = Counter(types)

result = {
    "Сортировка по rating": sorted_data,
    "Статистика для views": statistics,
    "Частота меток для counts": dict(type_counts)
}

output_file_main = "result_first_task.json"
with open(output_file_main, "w", encoding="utf-8") as file:
    json.dump(result, file, ensure_ascii=False, indent=4)

output_file_filtered = "filtered_data_first_task.json"
with open(output_file_filtered, "w", encoding="utf-8") as file:
    json.dump(filtered_data, file, ensure_ascii=False, indent=4)

