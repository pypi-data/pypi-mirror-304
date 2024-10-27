import json

def json_to_check(json_path, output_path):
    summ = 0
    with open(json_path, 'r') as f:
        data = json.load(f)

    f = open(output_path, 'w')
    customer_name = data['customer_name']
    f.write(f'Покупатель: {customer_name}\n')
    f.write('-' * 10 +'\n')

    for item in data['items']:
        f.write(f'Товар: {item["name"]}, Количество: {item["quantity"]}, Цена за единицу: {item["price"]}\n')
        f.write('-' * 10 +'\n')
        summ += item['quantity'] * item['price']
    f.write(f'Общая сумма заказа: {summ}')

json_to_check('/Users/elhuel/Documents/CU/devHW/Class06K/data4/order.json', '/Users/elhuel/Documents/CU/devHW/Class06K/data4/order.txt')


