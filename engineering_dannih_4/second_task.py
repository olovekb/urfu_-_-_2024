from common import connect_to_db
import csv
import json

file_path = "data/1-2/subitem.csv"

def load_csv(filename):
    items = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        reader.__next__()
        for row in reader:
            if len(row) == 0: continue
            item = {
                'name': row[0],
                'place': int(row[1]),
                'prise': int(row[2])
            }
            items.append(item)
    return items
            

def create_prise_table(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prise (
            id INTEGER PRIMARY KEY, 
            tournament_name TEXT REFERENCES tournament(name),
            place INTEGER,
            prise INTEGER
        )           
    """)

def insert_data(db, items):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO prise (tournament_name, place, prise)
        VALUES (:name, :place, :prise)
    """, items)
    db.commit()


def first_query(db):
    cursor = db.cursor()
    res = cursor.execute(f"""
        SELECT *
        FROM prise
        WHERE tournament_name = 'Кубок мира 1978'
        ORDER BY place
    """)

    items = [dict(row) for row in res.fetchall()]  
    
    with open("results/second_task_result_1.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=4)    
    
    return items

def second_query(db):
    cursor = db.cursor()
    res = cursor.execute(f"""
        SELECT t.name, t.id, p.prise
        FROM tournament t
        JOIN prise p ON t.name = p.tournament_name
        WHERE p.place = 0
        LIMIT 7
    """)

    items = [dict(row) for row in res.fetchall()]  
    
    with open("results/second_task_result_2.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=4)  
    
    return items

def third_query(db):
    cursor = db.cursor()
    res = cursor.execute(f"""
        SELECT t.name, sum(p.prise) as prise_found, max(p.place) as place_ccount
        FROM tournament t
        JOIN prise p ON t.name = p.tournament_name
        GROUP BY t.name
        ORDER BY prise_found DESC
        LIMIT 3
    """)

    items = [dict(row) for row in res.fetchall()]  
    
    with open("results/second_task_result_3.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=4)  
    
    return items

# STEP 1. 
# data = load_csv("data/1-2/subitem.csv")
# STEP 2.
db = connect_to_db("first.db")
# create_prise_table(db)
# STEP 3.
# insert_data(db, data)
# STEP 4.
print("Первый запрос:")
for row in first_query(db):
    print(row)

print("Второй запрос:")
for row in second_query(db):
    print(row)

print("Третий запрос:")
for row in third_query(db):
    print(row)