import pickle
import json

with open("data/fourth_task_products.json", "rb") as f:
    products = pickle.load(f)

with open("data/fourth_task_updates.json", "r", encoding="utf-8") as f:
    updates = json.load(f)


products_map = {}

for product in products:
    products_map[product['name']] = product


methods = {
    'percent-': lambda price, param: price * (1 - param),
    'percent+': lambda price, param: price * (1 + param),
    'add': lambda price, param: price + param,
    'sub': lambda price, param: price - param,
}


for update in updates:
    product = products_map[update['name']]
    product['price'] = methods[update['method']](product['price'], update['param'])


product = list(products_map.values())
print(products)
with open("result_fourth_task.pkl", "wb") as f:
    pickle.dump(product, f)