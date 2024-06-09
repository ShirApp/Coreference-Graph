import json

with open("output/indices_chains.txt", "r") as f:
    for line in f.readlines():
        result = json.loads(line)
        order_array = [res[0] for res in result]
        if order_array != sorted(order_array):
            print(order_array)
