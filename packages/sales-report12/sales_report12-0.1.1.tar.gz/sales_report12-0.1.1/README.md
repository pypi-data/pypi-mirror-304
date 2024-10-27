Sales_Report — Python-пакет для создания отчета по продажам. Установка: `pip install sales_report12`. Использование: `sales_report --input-file sales_data.csv --output-file sales_report.csv`. Параметры: `--input-file` — путь к CSV с данными о продажах (обязательный), `--output-file` — путь для сохранения отчета (обязательный). Формат CSV: файл должен содержать колонки `category`, `sales`, `quantity`, например: 

```csv
category,sales,quantity
electronics,500,2
electronics,800,5
clothing,200,4
clothing,500,9
