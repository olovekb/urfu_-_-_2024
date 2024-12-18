from pymongo import MongoClient
import csv
import os
import json


file_path = "data/task_2_item.csv"

def connect_db():
    client = MongoClient()
    db = client["db-2024-urfu"]
    return db.jobs

def read_csv(filename):
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";") # DictReader отображает информацию о каждой строке как словарь 
        for row in reader:
            row["salary"] = int(row["salary"])
            row["id"] = int(row["id"])
            row["year"] = int(row["year"])
            row["age"] = int(row["age"])
            data.append(row)
    return data

def save_json(data, filename):
    # Если данные это список документов, удаляю поле _id. Решил удалять т.к это объект, создаваемый монгой для идентификации объектов, в json он нам не нужен. 
    if isinstance(data, list):
        for record in data:
            record.pop("_id", None)
    with open(os.path.join("results", filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 1. Вывод минимальной, средней, максимальной salary
def salary_stats(collection):
    pipeline = [
        {"$group": {
            "_id": None,
            "min_salary": {"$min": "$salary"},
            "avg_salary": {"$avg": "$salary"},
            "max_salary": {"$max": "$salary"}
        }}
    ]
    return list(collection.aggregate(pipeline))

# 2. Вывод количества данных по представленным профессиям - здесь не понял, что значит "количество данных" в профессиях 
def count_by_job(collection):
    pipeline = [
        {"$group": {
            "_id": "$job",
            "count": {"$sum": 1}
        }}
    ]
    return list(collection.aggregate(pipeline))

# 3. Вывод минимальной, средней, максимальной salary по городу
def salary_stats_by_city(collection):
    pipeline = [
        {"$group": {
            "_id": "$city",
            "city": {"$first": "$city"},
            "min_salary": {"$min": "$salary"},
            "avg_salary": {"$avg": "$salary"},
            "max_salary": {"$max": "$salary"}
        }}
    ]
    return list(collection.aggregate(pipeline))

# 4. Вывод минимальной, средней, максимальной salary по профессии
def salary_stats_by_job(collection):
    pipeline = [
        {"$group": {
            "_id": "$job",
            "job": {"$first": "$job"},
            "min_salary": {"$min": "$salary"},
            "avg_salary": {"$avg": "$salary"},
            "max_salary": {"$max": "$salary"}
        }}
    ]
    return list(collection.aggregate(pipeline))

# 5. Вывод минимального, среднего, максимального возраста по городу
def age_stats_by_city(collection):
    pipeline = [
        {"$group": {
            "_id": "$city",
            "city": {"$first": "$city"},
            "min_age": {"$min": "$age"},
            "avg_age": {"$avg": "$age"},
            "max_age": {"$max": "$age"}
        }},
    ]
    return list(collection.aggregate(pipeline))

# 6. Вывод минимального, среднего, максимального возраста по профессии
def age_stats_by_job(collection):
    pipeline = [
        {"$group": {
            "_id": "$job",
            "job": {"$first": "$job"},
            "min_age": {"$min": "$age"},
            "avg_age": {"$avg": "$age"},
            "max_age": {"$max": "$age"}
        }}
    ]
    return list(collection.aggregate(pipeline))

# 7. Вывод максимальной заработной платы при минимальном возрасте
def max_salary_min_age(collection):
    pipeline = [
        {"$sort": {"age": 1, "salary": -1}},
        {"$limit": 1}
    ]
    return list(collection.aggregate(pipeline))

# 8. Вывод минимальной заработной платы при максимальной возрасте
def min_salary_max_age(collection):
    pipeline = [
        {"$sort": {"age": -1, "salary": 1}},
        {"$limit": 1}
    ]
    return list(collection.aggregate(pipeline))

# 9. Вывод минимального, среднего, максимального возраста по городу, при условии, что заработная плата больше 50 000, отсортировать вывод по убыванию по полю avg
def age_stats_by_city_with_salary(collection):
    pipeline = [
        {"$match": {"salary": {"$gt": 50000}}},
        {"$group": {
            "_id": "$city",
            "city": {"$first": "$city"},
            "min_age": {"$min": "$age"},
            "avg_age": {"$avg": "$age"},
            "max_age": {"$max": "$age"}
        }},
        {"$sort": {"avg_age": -1}}
    ]
    return list(collection.aggregate(pipeline))

# 10. Вывод минимальной, средней, максимальной salary в произвольно заданных диапазонах по городу, профессии, и возрасту: 18<age<25 & 50<age<65
def salary_stats_by_age_city_job(collection):
    # здесь диапазоны по городам и профессиям
    selected_cities = ["Минск", "Санкт-Петербург", "Москва"]
    selected_jobs = ["IT-специалист", "Программист", "Инженер"]

    pipeline = [
        {"$match": {
            "$and": [
                {"city": {"$in": selected_cities}},
                {"job": {"$in": selected_jobs}},
                {
                    "$or": [
                        {"age": {"$gt": 18, "$lt": 25}},
                        {"age": {"$gt": 50, "$lt": 65}}
                    ]
                }
            ]
        }},
        {"$group": {
            "_id": {"city": "$city", "job": "$job"},
            "city": {"$first": "$city"},
            "job": {"$first": "$job"},
            "min_salary": {"$min": "$salary"},
            "avg_salary": {"$avg": "$salary"},
            "max_salary": {"$max": "$salary"}
        }}
    ]
    return list(collection.aggregate(pipeline))


# 11. Произвольный запрос с $match, $group, $sort: средняя зарплата и возраст по профессии в диапазоне зарплат
def random_request(collection):
    pipeline = [
        {"$match": {"salary": {"$gte": 50000, "$lte": 150000}}},
        {"$group": {
            "_id": "$job",
            "job": {"$first": "$job"},
            "avg_salary": {"$avg": "$salary"},
            "avg_age": {"$avg": "$age"}
        }},
        {"$sort": {"avg_salary": -1}}
    ]
    return list(collection.aggregate(pipeline))


collection = connect_db()
read_csv(file_path)

#collection.insert_many(read_csv(file_path))

save_json(salary_stats(collection), "second_task_result_1.json")
save_json(count_by_job(collection), "second_task_result_2.json")
save_json(salary_stats_by_city(collection), "second_task_result_3.json")
save_json(salary_stats_by_job(collection), "second_task_result_4.json")
save_json(age_stats_by_city(collection), "second_task_result_5.json")
save_json(age_stats_by_job(collection), "second_task_result_6.json")
save_json(max_salary_min_age(collection), "second_task_result_7.json")
save_json(min_salary_max_age(collection), "second_task_result_8.json")
save_json(age_stats_by_city_with_salary(collection), "second_task_result_9.json")
save_json(salary_stats_by_age_city_job(collection), "second_task_result_10.json")
save_json(random_request(collection), "second_task_result_11.json")