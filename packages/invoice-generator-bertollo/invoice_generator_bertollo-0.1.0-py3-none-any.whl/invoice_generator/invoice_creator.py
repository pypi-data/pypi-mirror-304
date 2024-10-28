import json

def create_invoice(input_file: str, output_file: str):
    with open(input_file, 'r', encoding='utf-8') as f:
        order_data = json.load(f)

    customer_name = order_data['customer_name']
    items = order_data['items']
    total_amount = sum(item['quantity'] * item['price'] for item in items)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f'Чек для клиента: {customer_name}\n')
        f.write('Товары:\n')
        for item in items:
            f.write(f"- {item['name']}: {item['quantity']} x {item['price']} = {item['quantity'] * item['price']}\n")
        f.write(f'Общая сумма: {total_amount}\n')
