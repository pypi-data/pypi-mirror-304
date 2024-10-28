import json

def check(json_path, txt_path):
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)

    with open(txt_path, 'w', newline='') as txt_file:
        txt_file.write(f'Имя: {data["customer_name"]}\nТовары:\n')
        for i in data['items']:
            txt_file.write(f'\t{i["name"] + " " * (30 - len(i["name"]))}x{i["quantity"]}\t\t{i["price"]}\n')
        txt_file.write(f'Общая стоимость: {sum(i["quantity"] * i["price"] for i in data["items"])}')
