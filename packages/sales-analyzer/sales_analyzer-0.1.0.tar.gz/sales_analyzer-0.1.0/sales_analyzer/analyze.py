import pandas as pd


def analyze_sales(input_file: str, output_file: str):
    data = pd.read_csv(input_file)

    report = data.groupby('category').agg(
        sales=('sales', 'sum'),
        quantity=('quantity', 'sum')
    ).reset_index()

    # Сохранение отчёта в выходной CSV-файл
    report.to_csv(output_file, index=False)
