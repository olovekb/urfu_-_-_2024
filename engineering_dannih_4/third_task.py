import json
import msgpack
from common import connect_to_db

json_file_path = "data/3/_part_1.json"
msgpack_file_path = "data/3/_part_2.msgpack"
db_path = "unified_music_data.db"

var = 33  

def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_msgpack(file_path):
    with open(file_path, "rb") as f:
        return msgpack.unpack(f, raw=False)

# Решил удалять дубликаты, потому что песни могут повторяться в разных файлах.
def remove_duplicates(data):
    seen = set()
    unique_data = []

    for item in data:
        key = (item["artist"], item["song"])
        if key not in seen:
            seen.add(key)
            unique_data.append(item)

    return unique_data

def create_music_table(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS music_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist TEXT,
            song TEXT,
            year INTEGER,
            genre TEXT,
            popularity INTEGER,
            UNIQUE(artist, song)
        )
    """)
    db.commit()

def insert_music_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT OR IGNORE INTO music_data (artist, song, year, genre, popularity)
        VALUES (:artist, :song, :year, :genre, :popularity)
    """, data)
    db.commit()

def unify_data(json_data, msgpack_data):
    unified_data = []

    for item in json_data:
        unified_data.append({
            "artist": item.get("artist", "Unknown"),
            "song": item.get("song", "Unknown"),
            "year": int(item.get("year", 0)),
            "genre": item.get("genre", "Unknown"),
            "popularity": int(item.get("popularity", 0)),
        })

    for item in msgpack_data:
        unified_data.append({
            "artist": item.get("artist", "Unknown"),
            "song": item.get("song", "Unknown"),
            "year": int(item.get("year", 0)),
            "genre": item.get("genre", "Unknown"),
            "popularity": int(item.get("popularity", 0)),
        })

    return unified_data

def first_query(db):
    cursor = db.cursor()
    res = cursor.execute(f"""
        SELECT *
        FROM music_data
        ORDER BY popularity DESC
        LIMIT {var + 10}
    """)
    items = [dict(row) for row in res.fetchall()]
    
    with open("results/third_task_result_1.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=4)

def second_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT
            SUM(popularity) as sum_popularity,
            MIN(popularity) as min_popularity,
            MAX(popularity) as max_popularity,
            ROUND(AVG(popularity), 2) as avg_popularity
        FROM music_data
    """)
    return dict(res.fetchone())

def third_query(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT genre, COUNT(*) as count
        FROM music_data
        GROUP BY genre
        ORDER BY count DESC
    """)
    return [dict(row) for row in res.fetchall()]

def fourth_query(db):
    cursor = db.cursor()
    res = cursor.execute(f"""
        SELECT *
        FROM music_data
        WHERE year > 2000
        ORDER BY year DESC
        LIMIT {var + 15}
    """)
    items = [dict(row) for row in res.fetchall()]
    
    with open("results/third_task_result_4.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":

    json_data = load_json(json_file_path)
    msgpack_data = load_msgpack(msgpack_file_path)

    unified_data = unify_data(json_data, msgpack_data)
    unified_data = remove_duplicates(unified_data)

    db = connect_to_db(db_path)
    create_music_table(db)
    insert_music_data(db, unified_data)

    first_query(db)
    print("Второй запрос:")
    print(second_query(db))
    print("Третий запрос:")
    print(third_query(db))
    fourth_query(db)

