import json
import argparse


class OrderReceipt:
    def __init__(self, input_file):
        self.input_file = input_file
        self.order_data = self.load_data()

    def load_data(self):
        with open(self.input_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def generate_receipt(self):
        customer_name = self.order_data['customer_name']
        items = self.order_data['items']

        total_amount = sum(item['quantity'] * item['price'] for item in items)

        receipt_lines = [f'Имя клиента: {customer_name}\n', 'Список товаров:\n']

        for item in items:
            line = f"{item['name']}: {item['quantity']} шт. по {item['price']} руб.\n"
            receipt_lines.append(line)

        receipt_lines.append(f'\nОбщая сумма заказа: {total_amount} руб.\n')

        return ''.join(receipt_lines)


def main():
    parser = argparse.ArgumentParser(description='Генерация чека на основе заказа.')
    parser.add_argument('--input-file', type=str, required=True, help='Укажите входной файл .json.')
    parser.add_argument('--output-file', type=str, required=True, help='Укажите выходной файл .txt.')

    args = parser.parse_args()

    receipt_generator = OrderReceipt(args.input_file)
    receipt_content = receipt_generator.generate_receipt()

    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(receipt_content)

    print(f'Чек сохранён в {args.output_file}')


if __name__ == '__main__':
    main()
