import os
import json
from bs4 import BeautifulSoup
from collections import Counter
from statistics import median


path_folder = "data/2"
output_file = "result_second_task.json"
filtered_file = "filtered_data_second_task.json"

parsed_data = []

def extract_number(value):
    try:
        return int("".join(filter(str.isdigit, value)))
    except ValueError:
        return 0
    
def parse_html(file_path):
    data_list = []
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        
        product_items = soup.find_all("div", class_="product-item")
        for product in product_items:
            item = {}
            
            id_tag = product.find("a", class_="add-to-favorite")
            item["id"] = id_tag["data-id"] if id_tag and "data-id" in id_tag.attrs else None
            
            img_tag = product.find("img")
            item["image"] = img_tag["src"] if img_tag else None
            
            name_tag = product.find("span")
            item["name"] = name_tag.text.strip() if name_tag else None
            
            price_tag = product.find("price")
            item["price"] = extract_number(price_tag.text)

            link_tag = product.find("a", href=lambda href: href and "/product/" in href)
            item["link"] = link_tag["href"] if link_tag else None
            
            bonus_tag = product.find("strong")
            if bonus_tag and "начислим" in bonus_tag.text:
                item["bonus"] = extract_number(bonus_tag.text)
            else:
                item["bonus"] = 0
            
            for li in product.find_all("li"):
                key = li.get("type")
                value = li.text.strip()
                if key:
                    item[key] = value
            
            data_list.append(item)
    
    return data_list

for file_name in os.listdir(path_folder):
    if file_name.endswith(".html"):
        file_path = os.path.join(path_folder, file_name)
        file_data = parse_html(file_path)
        parsed_data.extend(file_data)

sorted_data = sorted(parsed_data, key=lambda x: x['price'], reverse=True)

filtered_bonus = [item for item in parsed_data if item['bonus'] > 1000]

with open(filtered_file, "w", encoding="utf-8") as json_file:
    json.dump(filtered_bonus, json_file, ensure_ascii=False, indent=4)

prices = [item['price'] for item in parsed_data if item['price'] > 0]
price_stats = {
    "total": sum(prices),
    "min": min(prices) if prices else 0,
    "max": max(prices) if prices else 0,
    "average": sum(prices) / len(prices) if prices else 0,
    "median": median(prices) if prices else 0,
    "total": sum(prices) if prices else 0
}

ram_counts = Counter(item.get('ram') for item in parsed_data if 'ram' in item and item.get('ram'))

result = {
    "parsed_data & sorted_data": sorted_data,
    "price_stats": price_stats,
    "ram_counts": dict(ram_counts)
}

with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=4)
