import argparse
from client_analysis import ClientAnalysis


def main():
    parser = argparse.ArgumentParser(description='Анализ данных о клиентах из CSV-файла.')
    parser.add_argument('--input-file', type=str, required=True, help='Путь к входному CSV-файлу')
    parser.add_argument('--output-file', type=str, required=True, help='Путь к выходному TXT-файлу')

    args = parser.parse_args()

    analysis = ClientAnalysis(args.input_file)

    total_clients = analysis.total_clients()
    age_dist = analysis.age_distribution()
    city_dist = analysis.city_distribution()

    with open(args.output_file, 'w') as f:
        f.write(f'Общее количество клиентов: {total_clients}\n\n')

        f.write('Количество клиентов по возрастным группам:\n')
        for age_group, count in age_dist.items():
            f.write(f'{age_group}: {count}\n')
        f.write('\n')

        f.write('Распределение клиентов по городам:\n')
        for city, count in city_dist.items():
            f.write(f'{city}: {count}\n')


if __name__ == '__main__':
    main()
