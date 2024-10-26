import pandas as pd
import argparse


class SalesAnalyzer:
    def __init__(self, input_file):
        self.input_file = input_file
        self.data = self.load_data()

    def load_data(self):
        return pd.read_csv(self.input_file)

    def generate_report(self):
        report = self.data.groupby('category').agg(
            sales=('amount', 'sum'),  # Сумма продаж
            quantity=('quantity', 'sum')  # Количество проданных товаров
        ).reset_index()
        return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, required=True, help='Укажите входной файл .csv.')
    parser.add_argument('--output-file', type=str, required=True, help='Укажите выходной файл .csv.')

    args = parser.parse_args()

    analyzer = SalesAnalyzer(args.input_file)
    report = analyzer.generate_report()

    report.to_csv(args.output_file, index=False)
    print(f'Отчёт сохранён в {args.output_file}')


if __name__ == '__main__':
    main()
