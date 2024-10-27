import json
def load_order(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        return json.load(file)
def generate_receipt(order_data):
    customer_name = order_data['customer_name']
    items = order_data['items']
    receipt_lines = [f"Имя клиента: {customer_name}\n", "Список товаров:\n"]
    total = 0
    for item in items:
        name = item['name']
        quantity = item['quantity']
        price = item['price']
        line_total = quantity * price
        total += line_total
        receipt_lines.append(f"{name} - {quantity} шт. по {price} руб. (всего {line_total} руб.)\n")
    receipt_lines.append(f"\nОбщая сумма заказа: {total} руб.\n")
    return ''.join(receipt_lines)
def save_receipt(receipt_content, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(receipt_content)
