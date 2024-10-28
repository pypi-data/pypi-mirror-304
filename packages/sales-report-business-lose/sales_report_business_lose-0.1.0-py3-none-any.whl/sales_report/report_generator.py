import pandas as pd


def load_sales_data(input_file):
    # Загружаем данные из CSV файла
    df = pd.read_csv(input_file)
    return df


def generate_report(sales_data):
    # Группируем данные по категориям и вычисляем сумму и количество
    report = sales_data.groupby('category').agg(
        sales=('amount', 'sum'),
        quantity=('quantity', 'sum')
    ).reset_index()

    return report


def save_report(report, output_file):
    # Сохраняем отчет в CSV файл
    report.to_csv(output_file, index=False)
