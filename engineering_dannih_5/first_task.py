from pymongo import MongoClient
import json
import os

file_path = "data/task_1_item.text"

def connect_db():
    client = MongoClient()
    db = client["db-2024-urfu"]
    print(db.jobs)
    return db.jobs

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = []
            # здесь разделил на блоки по "====="
        for block in f.read().split("====="):
            block = block.strip()
            if block:  
                record = {}
                # здесь разделил строки в блоке на пары ключ::значение
                for line in block.splitlines():
                    key, value = line.split("::")
                    if key  in ["salary", "age", "id", "year"]:
                        value = int(value)
                    record[key] = value
                data.append(record)
    return data


def sort_by_salary(collection):
    return list(collection.find(limit = 10).sort({"salary": -1}))

def filter_by_age(collection):
    return list(collection.find({"age": {"$lt": 30}}, limit = 15).sort({"salary": -1}))

def hard_filter(collection):
    return list(collection.find({"city": "Баку", "job": {"$in": ["Менеджер", "Программист", "Архитектор"]}}, limit = 10).sort({"age": 1}))

def range_filter(collection):
    return collection.count_documents({
        "age": {"$gt": 27, "$lte": 57},
        "year": {"$gte": 2019, "$lte": 2022},
        "$or": [
            {"salary": {"$gt": 50000, "$lte": 75000}},
            {"salary": {"$gt": 120000, "$lte": 150000}}
        ]
    })

def save_json(data, filename):
    # Если данные это список документов, удаляю поле _id. Решил удалять т.к это объект, создаваемый Монгой для идентификации объектов, в json он нам не нужен. 
    if isinstance(data, list):
        for record in data:
            record.pop("_id", None)
    with open(os.path.join("results", filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


collection = connect_db()
#collection.insert_many(read_file(file_path))


sort_by_salary(collection)
sort_by_salary_result = sort_by_salary(collection)
save_json(sort_by_salary_result, "first_task_result_1.json")
#print("Вывод первых 10 записей, отсортированных по убыванию по полю salary:") 
#for line in sort_by_salary_result:
#    print(line)

filter_by_age(collection)
filter_by_age_result = filter_by_age(collection)
save_json(filter_by_age_result, "first_task_result_2.json")
#print("Вывод первых 15 записей, отфильтрованных по предикату age < 30, отсортировать по убыванию по полю salary:")
#for line in filter_by_age_result:
#   print(line)

hard_filter(collection)
hard_filter_result = hard_filter(collection)
save_json(hard_filter_result, "first_task_result_3.json")
#print("Вывод первых 10 записей, отфильтрованных по сложному предикату: (записи только из произвольного города, записи только из трех произвольно взятых профессий), отсортировать по возрастанию по полю age:")
#for line in hard_filter_result:
#    print(line)  

range_filter(collection)
range_filter_result = range_filter(collection)
save_json({"Количество записей": range_filter_result}, "first_task_result_4.json")
#print("Вывод количества записей, получаемых в результате следующей фильтрации (age в произвольном диапазоне, year в [2019,2022], 50 000 < salary <= 75 000 || 125 000 < salary < 150 000):")
#print(range_filter(collection))    