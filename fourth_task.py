import csv

def read_csv(path):
    data = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'product_id': int(row['product_id']),
                'name': row['name'],
                'price': float(row['price']),
                'quantity': int(row['quantity']),
                'category': row['category'],
                'description': row['description'],
                'production_date': row['production_date'],
                'expiration_date': row['expiration_date'],
                # 'rating': float(row['rating']),
                'status': row['status']
            })
        return data

data = read_csv("data/fourth_task.txt")

size = len(data)
avg_price = 0
max_price = data[0]['price']
min_quantity = data[0]['quantity']

filtered_data = []

for item in data:
    avg_price += item['price']

    if max_price < item['price']:
        max_price = item['price']

    if min_quantity > item['quantity']:
        min_quantity = item['quantity']

    if item['category'] != 'Молочные продукты':
        filtered_data.append(item)

avg_price /= size

with open("result_fourth_task.txt", "w", encoding="utf-8") as f:
    f.write("Среднеарифметическая цена: "f"{avg_price}\n")
    f.write("Максимум price: "f"{max_price}\n")
    f.write("Минимум quantity: "f"{min_quantity}")
    
with open("result_fourth_task.csv", "w", encoding="utf-8", newline="")  as f:
    writer = csv.DictWriter(f, filtered_data[0].keys())
    writer.writeheader()
    for row in filtered_data:
        writer.writerow(row)