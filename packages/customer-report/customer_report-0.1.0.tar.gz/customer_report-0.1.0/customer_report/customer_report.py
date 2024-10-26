import pandas as pd
import argparse


class CustomerAnalyzer:
    def __init__(self, input_file):
        self.input_file = input_file
        self.data = self.load_data()

    def load_data(self):
        return pd.read_csv(self.input_file)

    def generate_report(self):
        total_customers = len(self.data)

        age_groups = {
            '18-25': 0,
            '26-35': 0,
            '36-45': 0,
            '46-60': 0,
            '60+': 0
        }

        for age in self.data['age']:
            if 18 <= age <= 25:
                age_groups['18-25'] += 1
            elif 26 <= age <= 35:
                age_groups['26-35'] += 1
            elif 36 <= age <= 45:
                age_groups['36-45'] += 1
            elif 46 <= age <= 60:
                age_groups['46-60'] += 1
            elif age > 60:
                age_groups['60+'] += 1

        city_distribution = self.data['city'].value_counts().to_dict()

        report_lines = [f'Общее количество клиентов: {total_customers}\n',
                        'Количество клиентов по возрастным группам:\n']

        for group, count in age_groups.items():
            report_lines.append(f'{group}: {count}\n')

        report_lines.append('Распределение клиентов по городам:\n')

        for city, count in city_distribution.items():
            report_lines.append(f'{city}: {count}\n')

        return ''.join(report_lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, required=True, help='Укажите входной файл .csv: ')
    parser.add_argument('--output-file', type=str, required=True, help='Укажите выходной файл .tx: ')

    args = parser.parse_args()

    analyzer = CustomerAnalyzer(args.input_file)
    report_content = analyzer.generate_report()

    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f'Отчёт сохранён в {args.output_file}')


if __name__ == '__main__':
    main()
