import argparse
from .report_generator import load_sales_data, generate_sales_report, save_report


def main():
    parser = argparse.ArgumentParser(description="Генератор отчёта по продажам.")
    parser.add_argument("--input-file", required=True, help="Путь к входному CSV-файлу с данными о продажах")
    parser.add_argument("--output-file", required=True, help="Путь к выходному CSV-файлу для отчёта")

    args = parser.parse_args()

    data = load_sales_data(args.input_file)
    report = generate_sales_report(data)
    save_report(report, args.output_file)

    print(f"Отчёт успешно сохранен в файл {args.output_file}")
