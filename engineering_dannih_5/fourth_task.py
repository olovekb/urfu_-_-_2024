import json
import csv
from pymongo import MongoClient
import os

file_path_csv = "data/task_4_people.csv"
file_path_json = "data/task_4_movies.json"

def connect_db():
    client = MongoClient()
    db = client["db-2024-urfu"]
    return db.movies

def read_json(file_path_json):
    with open(file_path_json, "r", encoding="utf-8") as file:
        data = json.load(file)
        for row in data:
            row["id"] = int(row["id"])
            row["year"] = int(row["year"])
            row["rating"] = float(row["rating"])
    return data

def read_csv(filename):
    data = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";") # DictReader отображает информацию о каждой строке как словарь 
        for row in reader:
            row["id"] = int(row["id"])
            row["age"] = int(row["age"])
            data.append(row)
    return data

def merge_data(movies, people):
    people_dict = {person["id"]: person for person in people}
    for movie in movies:
        person = people_dict.get(movie["id"])
        if person:
            movie["actor"] = person["actor"]
            movie["age"] = person["age"]
            movie["city"] = person["city"]
    return movies

def save_json(data, filename):
    # Если данные это список документов, удаляю поле _id. Решил удалять т.к это объект, создаваемый монгой для идентификации объектов, в json он нам не нужен. 
    if isinstance(data, list):
        for record in data:
            record.pop("_id", None)
    with open(os.path.join("results", filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



# Задание №1
def higher_by_rating(collection):
    # Пример 1: Найти все фильмы с рейтингом выше 8.9
    result = collection.find({"rating": {"$gt": 8.9}})
    return list(result)


    # Пример 2: Найти все фильмы жанра Драма
def drama_count(collection):
    result = collection.find({"genre": "Drama"})
    return list(result)

def all_films_after_year(collection):
    # Пример 3: Найти все фильмы, вышедшие после 2000 года
    result = collection.find({"year": {"$gt": 2000}})
    return list(result)


def director_movies_count(collection):
    # Пример 4: Найти все фильмы определенного режиссера
    result = collection.find({"director": "Christopher Nolan"})
    return list(result)

    # Пример 5: Найти фильмы с указанным актером
def movies_with_actor(collection):
    result = collection.find({"actor": "Leonardo DiCaprio"})
    return list(result)


# Задание №2
def aggregation_genre_count(collection):
    #1: Подсчитать количество фильмов по жанрам
    pipeline = [
        {"$group": {
            "_id": "$genre",
            "genre": {"$first": "$genre"},
            "count": {"$sum": 1}
            }},
        {"$sort": {"count": -1}}
    ]
    return list(collection.aggregate(pipeline))

    #2: Средний рейтинг фильмов по городам с фильтрацией по возрасту актёров > 30
def aggregation_average_age_by_city(collection):
    pipeline = [
        {"$match": {
        "age": {"$gt": 30}
        }},
        {"$group": {
            "_id": "$city",
            "title": {"$first": "$title"},
            "average_rating": {"$avg": "$rating"}
        }},
        {"$sort": {
            "average_rating": -1
        }}
    ]
    return list(collection.aggregate(pipeline))

    #3: Средний рейтинг фильмов по режиссерам
def aggregation_average_rating_by_director(collection):
    result = collection.aggregate([
        {"$group": {
            "_id": "$director", 
            "director": {"$first": "$director"},
            "average_rating": {"$avg": "$rating"}
        }}
    ])
    return list(result)

    #4: Фильмы, отсортированные по году выпуска
def aggregation_sort_by_year(collection):
    result = collection.aggregate([
        {"$sort": {"year": -1}}
    ])
    return list(result)


    #5: Максимальный рейтинг по жанрам
def aggregation_max_rating_by_genre(collection):
    result = collection.aggregate([
        {"$group": {
            "_id": "$genre",
            "genre": {"$first": "$genre"}, 
            "max_rating": {"$max": "$rating"}
        }}
    ])
    return list(result)


# Задание №3
def update_genre(collection):
    #1: Обновить жанр фильма
    return collection.update_one(
        {"title": "Inception"}, 
        {"$set": {"genre": "Thriller"}})

def increase_age(collection):
    #2: Увеличить возраст всех актеров на 1
    return collection.update_many({}, 
        {"$inc": {"age": 1}})

def delete_movie_by_rating(collection):
    #3: Удалить фильмы с рейтингом ниже 8.6
    return collection.delete_many(
        {"rating": {"$lt": 8.6}})

    #4: Удалить фильмы, где возраст актера больше 70 
def delete_movie_by_age(collection):
    return collection.delete_many({"age": {"$gt": 70}})

    #5: Обновить город определенного актера
def update_city(collection):
    return collection.update_one({"actor": "Keanu Reeves"}, {"$set": {"city": "Los Angeles"}})


collection = connect_db()
movies_data = read_json(file_path_json)
people_data = read_csv(file_path_csv)

# Обьединение даннных и заполнение коллекции
#merged_data = merge_data(movies_data, people_data)
#collection.insert_many(merged_data)



# Выполнение функций

save_json(higher_by_rating(collection), "third_task_result_1.json")
save_json(drama_count(collection), "third_task_result_2.json")
save_json(all_films_after_year(collection), "third_task_result_3.json")
save_json(director_movies_count(collection), "third_task_result_4.json")
save_json(movies_with_actor(collection), "third_task_result_5.json")

save_json(aggregation_genre_count(collection), "third_task_result_6.json")
save_json(aggregation_average_age_by_city(collection), "third_task_result_7.json")
save_json(aggregation_average_rating_by_director(collection), "third_task_result_8.json")
save_json(aggregation_sort_by_year(collection), "third_task_result_9.json")
save_json(aggregation_max_rating_by_genre(collection), "third_task_result_10.json")

    #1: Обновить жанр фильма
print(update_genre(collection))

    # Пример 2: Увеличить возраст всех актеров на 1
print(increase_age(collection))

    # Пример 3: Удалить фильмы с рейтингом ниже 8.6
print(delete_movie_by_rating(collection))

    #4: Удалить фильмы, где возраст актера больше 70 
print(delete_movie_by_age(collection))

    #5: Обновить город определенного актера
print(update_city(collection))



