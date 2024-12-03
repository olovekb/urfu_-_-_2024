import os
import json
import statistics
import xml.etree.ElementTree as ET
from collections import Counter
from typing import List, Dict, Any

# Путь к папке с XML-файлами
path_folder = "data/4"
output_file = "result_fourth_task.json"
filtered_file = "filtered_data_fourth_task.json"

def parse_xml_file(file_path: str) -> List[Dict[str, Any]]:
    tree = ET.parse(file_path)
    root = tree.getroot()

    items = []
    for item in root.findall(".//clothing"):
        clothing_dict = {}
        for child in item:
            text = child.text.strip() if child.text else None

            if child.tag in ["id", "reviews", "price"]:
                clothing_dict[child.tag] = int(text) if text else None
            elif child.tag == "rating":
                clothing_dict[child.tag] = float(text) if text else None
            else:
                clothing_dict[child.tag] = text
        items.append(clothing_dict)
    return items

def process_data(path_folder: str) -> Dict[str, Any]:
    all_items: List[Dict[str, Any]] = []

    for filename in os.listdir(path_folder):
        if filename.endswith(".xml"):
            file_path = os.path.join(path_folder, filename)
            items = parse_xml_file(file_path)
            all_items.extend(items)

    # 1. Сортировка по цене
    sorted_data = sorted(
        all_items,
        key=lambda x: x.get("price", float("-inf")) if x.get("price") is not None else float("-inf"),
    )

    # 2. Фильтрация: только "эксклюзивные" товары
    filtered_data = [item for item in all_items if item.get("exclusive") == "yes"]

    with open(filtered_file, "w", encoding="utf-8") as f:
        json.dump({"filtered_data": filtered_data}, f, ensure_ascii=False, indent=2)

    prices = [item["price"] for item in all_items if item.get("price") is not None]
    price_stats = {
        "min": min(prices) if prices else None,
        "max": max(prices) if prices else None,
        "mean": statistics.mean(prices) if prices else None,
        "median": statistics.median(prices) if prices else None,
        "sum": sum(prices) if prices else None,
    }

    # 4. Частота категорий
    material_frequency = Counter(item.get("material") for item in all_items if item.get("material"))

    # Сохранение всех данных
    result = {
        "parsed_data & sorted_data": sorted_data,
        "price_stats": price_stats,
        "material_frequency": dict(material_frequency),
    }
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result

results = process_data(path_folder)
