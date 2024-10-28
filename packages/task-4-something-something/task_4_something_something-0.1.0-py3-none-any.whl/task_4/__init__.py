import json

def check(json_path, txt_path):
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)

    with open(txt_path, 'w', newline='') as txt_file:
        txt_file.write(f'Имя: {data["customer_name"]}\nТовары:')
        for i in data['items']:
            txt_file.write(f'\t{i["name"]}\t\tx{i["quantity"]}\t\t{i["price"]}')
        txt_file.write(f'Общая стоимость: {sum(i["quantity"] * i["price"] for i in data["items"])}')
