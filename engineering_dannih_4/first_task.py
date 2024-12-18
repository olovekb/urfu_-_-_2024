import pickle
import os
import json
from common import connect_to_db

file_path = "data/1-2/item.pkl"
var = 33

def load_pkl(filename):
    items = []
    with open(file_path, "rb") as file:
        load = pickle.load(file)
        
        # Проверяем, что данные - список словарей
        if isinstance(load, list) and all(isinstance(row, dict) for row in load):
            for row in load:
                # Создаем словарь только с нужными ключами и добавляем проверки
                item = {
                    'id': int(row.get('id', 0)),  # Если 'id' отсутствует, ставим 0
                    'name': row.get('name', 'Unknown'),
                    'city': row.get('city', 'Unknown'),
                    'begin': row.get('begin', None),
                    'system': row.get('system', 'Unknown'),
                    'tours_count': int(row.get('tours_count', 0)),
                    'min_rating': int(row.get('min_rating', 0)),
                    'time_on_game': int(row.get('time_on_game', 0))
                }
                items.append(item)
    
    # Удаляем дублирующиеся id
    unique_items = {item['id']: item for item in items}.values()
    return list(unique_items)

def create_tournament_table(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tournament (
            id INTEGER PRIMARY KEY, 
            name TEXT, 
            city TEXT,
            begin TEXT, 
            system TEXT, 
            tours_count INTEGER, 
            min_rating INTEGER, 
            time_on_game INTEGER
        )           
    """)
    db.commit()

def insert_data(db, items):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT OR IGNORE INTO tournament (id, name, city, begin, system, tours_count, min_rating, time_on_game)
        VALUES (:id, :name, :city, :begin, :system, :tours_count, :min_rating, :time_on_game)
    """, items)
    db.commit()



def first_query(db):
    cursor = db.cursor()
    res = cursor.execute(f"""
        SELECT *
        FROM tournament
        ORDER BY min_rating
        LIMIT {var + 10}
    """)

    items = [dict(row) for row in res.fetchall()] 

    with open("results/first_task_result_1.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=4)

def second_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT
            SUM(time_on_game) as sum_time_on_game_count,
            MIN(time_on_game) as min_time_on_game_count,
            MAX(time_on_game) as max_time_on_game_count,
            ROUND(AVG(time_on_game), 2) as avg_time_on_game_count    
        FROM tournament                              
    """)

    items = [dict(row) for row in res.fetchall()]  
    return items[0]

def third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT
            COUNT(*) as count,
            system
        FROM tournament
        GROUP BY system
    """)

    items = [dict(row) for row in res.fetchall()]  
    return items

def fourth_query(db):
    cursor = db.cursor()
    res = cursor.execute(f"""
        SELECT *
        FROM tournament
        WHERE min_rating > 2500
        ORDER BY min_rating DESC
        LIMIT {var + 10}
    """)

    items = [dict(row) for row in res.fetchall()]  
    
    with open("results/first_task_result_4.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=4)

# ----------------------------------------------------------

# Step 1.
create_tournament_table(connect_to_db("first.db"))

# Step 2.
db = connect_to_db("first.db")  
items = load_pkl(file_path)  
insert_data(db, items) 

# Step 3.
first_query(db)
print (second_query(db))
print (third_query(db))
fourth_query(db)



