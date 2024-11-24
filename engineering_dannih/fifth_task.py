import csv

from bs4 import BeautifulSoup

columns = ["product_id", "name","price", "quantity", "category", "description", "production_date", "expiration_date", "rating", "status"]

to_float = ['price', 'rating']
to_int = ['product_id', 'quantity']

with open("data/fifth_task.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

data = []

for row in soup.find_all("tr"):
    cols = row.find_all("td")
    item = {}

    columns_index = 0
    for col in cols:
        val = col.get_text(strip=True)
        curr_column = columns[columns_index]
        columns_index += 1
        item[curr_column] = val

        if curr_column in to_float:
            item[curr_column] = float(val)
        elif curr_column in to_int:
            item[curr_column] = int(val)

    if len(item) > 0:
        data.append(item)

# здесь не понял, надо ли все считывать или только строку своего варианта, поэтому считываю 33 строку согласно своему варианту 
def get_row_by_product_id_33(data, product_id):
    for item in data:
        if item.get("product_id") == product_id:
            return item
    return None

product_id = 33
result = get_row_by_product_id_33(data, product_id)

# записываю в csv-файл 33 строку
with open("fifth_task.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, columns)
    writer.writeheader()
    
    row_33 = get_row_by_product_id_33(data, product_id)
    writer.writerow(row_33)
