import pandas as pd

def load_sales_data(file_path):

    try:
        data = pd.read_csv(file_path)
    except Exception as e:
        raise Exception(f"Ошибка при загрузке файла: {e}")

    if 'category' not in data.columns or 'sales' not in data.columns or 'quantity' not in data.columns:
        raise ValueError("Файл должен содержать колонки 'category', 'sales' и 'quantity'")

    return data


def generate_sales_report(data):

    report = data.groupby('category').agg({
        'sales': 'sum',
        'quantity': 'sum'
    }).reset_index()

    return report


def save_report(report, output_file):

    report.to_csv(output_file, index=False)
