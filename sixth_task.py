import json
from bs4 import BeautifulSoup
json_data = """
[
    {
        "id": 9223372036854745000,
        "photoUrls": [
        "http://example.com/photo.jpg"
        ],
        "tags": [],
        "status": "available"
    },
    {
        "id": 9223372036854745000,
        "category": {
        "id": 0,
        "name": "string"
        },
        "name": "fish",
        "photoUrls": [
        "string"
        ],
        "tags": [
        {
            "id": 0,
            "name": "string"
        }
        ],
        "status": "available"
    },
    {
        "id": 9223372036854745000,
        "category": {
        "id": 100,
        "name": "Dinosaur"
        },
        "name": "Tyrannosaurus",
        "photoUrls": [
        "http://en.wikipedia.org/wiki/Tyrannosaurus#/media/File:Tyrannosaurus_rex_mmartyniuk.png"
        ],
        "tags": [
        {
            "id": 100,
            "name": "reptile"
        },
        {
            "id": 101,
            "name": "dinosaur"
        }
        ],
        "status": "available"
    }
]    
"""

data = json.loads(json_data)

soup = BeautifulSoup("<html><head><title>JSON Data</title></head><body></body></html>", "html.parser")
body = soup.body

for item in data:
    item_div = soup.new_tag("div", **{"class": "item"})

    id_tag = soup.new_tag("p")
    id_tag.string = f"ID: {item['id']}"
    item_div.append(id_tag)

    if "category" in item:
        category_tag = soup.new_tag("p")
        category_name = item["category"]["name"]
        category_tag.string = f"Category: {category_name}"
        item_div.append(category_tag)

    if "name" in item:
        name_tag = soup.new_tag("p")
        name_tag.string = f"Name: {item['name']}"
        item_div.append(name_tag)

    photo_urls = item.get("photoUrls", [])
    if photo_urls:
        photo_div = soup.new_tag("div", **{"class": "photos"})
        for url in photo_urls:
            photo_tag = soup.new_tag("a", href=url)
            photo_tag.string = url
            photo_div.append(photo_tag)
        item_div.append(photo_div)

    tags = item.get("tags", [])
    if tags:
        tags_div = soup.new_tag("div", **{"class": "tags"})
        for tag in tags:
            tag_p = soup.new_tag("p")
            tag_p.string = f"Tag: {tag['name']}"
            tags_div.append(tag_p)
        item_div.append(tags_div)

    status_tag = soup.new_tag("p")
    status_tag.string = f"Status: {item['status']}"
    item_div.append(status_tag)

    body.append(item_div)

with open("result_sixth_task.html", "w", encoding="utf-8") as file:
    file.write(soup.prettify())
