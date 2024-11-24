import json
import msgpack
import os.path

def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

products = read_json("data/third_task.json")
products_stat ={}

for product in products:
    name = product['name']
    price = product['price']

    if name not in products_stat:
        products_stat[name] = {
            'name': name,
            'max_price': price,
            'avg_price': price,
            'count': 1,
            'min_price': price
        }

    else:
        stat = products_stat[name]
        if stat['max_price'] < price:
            stat['max_price'] = price 
        if stat['min_price'] < price:
            stat['min_price'] = price 
        stat['avg_price'] += price
        stat['count'] += 1


for name in products_stat:
    stat = products_stat[name]
    stat['avg_price'] /= stat['count']        

to_save = list(products_stat.values())
print(to_save)

with open("result_third_task.json", "w", encoding="utf-8") as f:
    json.dump(to_save, f, ensure_ascii=False)

with open("result_third_task.msgpack", "wb") as f:
    msgpack.dump(to_save, f)

json_size = os.path.getsize("result_third_task.json")
msgpack_size = os.path.getsize("result_third_task.msgpack")

print(json_size)
print(msgpack_size)
print(json_size - msgpack_size)
