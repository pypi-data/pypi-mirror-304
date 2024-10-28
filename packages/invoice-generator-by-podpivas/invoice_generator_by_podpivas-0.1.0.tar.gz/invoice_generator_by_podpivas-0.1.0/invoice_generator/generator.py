import json
import os


def generate_invoice(input_file, output_file):
    # Проверка существования входного файла
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' not found.")

    # Чтение данных из JSON-файла
    with open(input_file, 'r', encoding='utf-8') as f:
        order_data = json.load(f)

    customer_name = order_data['customer_name']
    items = order_data['items']

    # Форматирование чека
    total_amount = sum(item['quantity'] * item['price'] for item in items)
    invoice_lines = [f"Имя клиента: {customer_name}\n"]
    invoice_lines.append("Список товаров:\n")

    for item in items:
        invoice_lines.append(
            f"{item['name']}: {item['quantity']} x {item['price']} = {item['quantity'] * item['price']} руб.\n")

    invoice_lines.append(f"\nОбщая сумма: {total_amount} руб.")

    # Запись чека в текстовый файл
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(invoice_lines)

    print(f"Чек успешно сгенерирован и сохранён в '{output_file}'.")
