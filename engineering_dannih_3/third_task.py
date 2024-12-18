import json
import os
import statistics
import xml.etree.ElementTree as ET
from collections import Counter

path_folder = "data/3"
output_file = "result_third_task.json"
filtered_file = "filtered_data_third_task.json"

def parse_xml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    star_data = {}
    for child in root:
        if child.text is not None:
            value = child.text.strip()
            if child.tag == "radius":
                value = int(value)
            elif child.tag == "distance":
                value = float(value.split()[0])
            elif child.tag == "age":
                value = float(value.split()[0])
            star_data[child.tag] = value

    return star_data

def process_data(path_folder):
    stars_data = []

    for filename in os.listdir(path_folder):
        if filename.endswith(".xml"):
            file_path = os.path.join(path_folder, filename)
            star_data = parse_xml_file(file_path)
            stars_data.append(star_data)

    sorted_by_rotation = sorted(stars_data, key=lambda x: x.get("rotation", 0))

    filtered_data = [star for star in stars_data if star.get("constellation") == "Рак"]

    with open(filtered_file, "w", encoding="utf-8") as f:
        json.dump({"filtered_data": filtered_data}, f, ensure_ascii=False, indent=2)

    distance = [star["distance"] for star in stars_data if "distance" in star]
    radius_stats = {
        "min": min(distance) if distance else None,
        "max": max(distance) if distance else None,
        "mean": statistics.mean(distance) if distance else None,
        "median": statistics.median(distance) if distance else None,
        "sum": sum(distance) if distance else None,
    }

    constellation_freq = Counter(star.get("constellation") for star in stars_data if "constellation" in star)

    result = {
        "parsed_data & sorted_data": sorted_by_rotation,
        "radius_stats": radius_stats,
        "constellation_freq": dict(constellation_freq),
    }
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result

results = process_data(path_folder)
