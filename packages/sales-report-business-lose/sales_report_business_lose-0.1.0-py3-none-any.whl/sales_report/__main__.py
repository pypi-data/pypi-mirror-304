import argparse
from .report_generator import load_sales_data, generate_report, save_report


def main():
    parser = argparse.ArgumentParser(description='Анализ данных о продажах.')

    parser.add_argument(
        '--input-file', type=str, required=True,
        help='Путь к входному CSV-файлу с данными о продажах.')
    parser.add_argument(
        '--output-file', type=str, required=True,
        help='Путь к выходному CSV-файлу для отчета.')

    args = parser.parse_args()

    sales_data = load_sales_data(args.input_file)
    report = generate_report(sales_data)

    save_report(report, args.output_file)

    print(f'Отчет успешно сохранен в {args.output_file}')


if __name__ == '__main__':
    main()
