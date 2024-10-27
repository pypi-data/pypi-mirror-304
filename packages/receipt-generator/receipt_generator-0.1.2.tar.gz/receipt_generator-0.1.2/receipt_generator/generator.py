import json

def load_order_data(file_path):

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def generate_receipt(order_data):

    customer_name = order_data['customer_name']
    items = order_data['items']

    receipt_lines = [f"Чек для: {customer_name}\n"]
    total_amount = 0

    receipt_lines.append("Товары:\n")
    for item in items:
        name = item['name']
        quantity = item['quantity']
        price = item['price']
        total_price = quantity * price
        total_amount += total_price
        receipt_lines.append(f"{name} - {quantity} шт. по {price} руб. = {total_price} руб.\n")

    receipt_lines.append(f"\nОбщая сумма: {total_amount} руб.")
    return ''.join(receipt_lines)


def save_receipt(receipt, output_file):

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(receipt)
