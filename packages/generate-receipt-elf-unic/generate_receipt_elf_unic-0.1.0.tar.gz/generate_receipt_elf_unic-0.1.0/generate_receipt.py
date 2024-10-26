import argparse
import json


def generate_receipt(input_file: str, output_file: str):
    with open(input_file, 'r') as f:
        order_data = json.load(f)
        customer_name = order_data['customer_name']
        items = order_data['items']
        total_amount = sum(item['quantity'] * item['price'] for item in items)
        receipt = [f"Имя клиента: {customer_name}\n"]
        receipt.append("Список товаров:\n")

        for item in items:
            line = f"{item['name']}: {item['quantity']} шт. по {item['price']} руб.\n"
            receipt.append(line)

        receipt.append(f"\nОбщая сумма заказа: {total_amount} руб.\n")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(''.join(receipt))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--input_file',
        action='store',
        required=True,
    )

    parser.add_argument(
        '--output_file',
        action='store',
        required=True,
    )

    args = parser.parse_args()


    generate_receipt(args.input_file, args.output_file)


if __name__ == '__main__':
    main()
