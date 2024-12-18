import os
import json
from pymongo import MongoClient
import pickle

file_path = "data/task_3_item.pkl"

def connect_db():
    client = MongoClient()
    db = client["db-2024-urfu"]
    return db.jobs

def save_json(data, filename):
    if isinstance(data, list):
        for record in data:
            record.pop("_id", None)  # Удаляем ObjectId для удобства
    with open(os.path.join("results", filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def read_pkl(filename):
    with open(file_path, "rb") as file:
        data = pickle.load(file) 
        for row in data:
            row["salary"] = int(row["salary"])
            row["id"] = int(row["id"])
            row["year"] = int(row["year"])
            row["age"] = int(row["age"])
    return data

# 1. Удалить из коллекции документы по предикату: salary < 25 000 || salary > 175000
def delete_by_salary(collection):
    collection.delete_many({
        "$or": [
            {"salary": {"$lt": 25000}},
            {"salary": {"$gt": 175000}}
        ] 
    })

# 2. Увеличить возраст (age) всех документов на 1
def increase_age(collection):
    return collection.update_many({}, {
        "$inc": {"age": 1}
        })

# 3. Поднять зарплату на 5% для произвольно выбранных профессий
def increase_salary_for_jobs(collection):
    return collection.update_many({
        "job": {"$in": ["Врач", "Инженер"]}
    }, {
        "$mul": {"salary": 1.05}
    })

# 4. Поднять зарплату на 7% для произвольно выбранных городов
def increase_salary_for_cities(collection):
    return collection.update_many({
        "city": {"$in": ["Сьюдад-Реаль", "Санкт-Петербург"]}
        }, {
            "$mul": {"salary": 1.07}
        })

# 5. Поднять зарплату на 10% по сложному предикату (город, профессии, возраст)
def increase_salary_complex_predicate(collection):
    return collection.update_many({
            "city": {"$in": ["Ереван", "Кишинев"]},
            "job": {"$in": ["Строитель", "Врач"]},
            "age": {"$gte": 30, "$lte": 45}
        },
        {"$mul": {"salary": 1.10}}
    )

# 6. Удалить документы по произвольному предикату
def delete_by_predicate(collection):
    return collection.delete_many(
        {"$and": [
            {"age": {"$gte": 55, "$lte": 70}},
            {"job": "Продавец"}
        ]}
    )

read_pkl(file_path)
#print(read_pkl(file_path))

collection = connect_db()
collection.insert_many(read_pkl(file_path))

# 1. Удалить из коллекции документы по предикату: salary < 25 000 || salary > 175000
print(delete_by_salary(collection))

# 2. Увеличить возраст (age) всех документов на 1
print(increase_age(collection))

# 3. Поднять зарплату на 5% для произвольно выбранных профессий
print(increase_salary_for_jobs(collection))

# 4. Поднять зарплату на 7% для произвольно выбранных городов
print(increase_salary_for_cities(collection))

# 5. Поднять зарплату на 10% по сложному предикату (город, профессии, возраст)
print(increase_salary_complex_predicate(collection))

# 6. Удалить документы по произвольному предикату
print(delete_by_predicate(collection))
