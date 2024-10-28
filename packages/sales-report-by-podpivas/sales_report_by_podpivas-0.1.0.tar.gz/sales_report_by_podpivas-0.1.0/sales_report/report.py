import pandas as pd

def generate_report(input_file: str):
    # Загрузка данных
    data = pd.read_csv(input_file)

    # Группировка данных по категории
    report = data.groupby('category').agg(
        sales=('sales', 'sum'),
        quantity=('quantity', 'sum')
    ).reset_index()

    return report
