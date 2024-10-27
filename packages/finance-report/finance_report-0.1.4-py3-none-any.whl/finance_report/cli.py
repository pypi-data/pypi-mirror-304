# finance_report/cli.py

import argparse
from task_2.finance_report.report_generator import load_transactions, calculate_totals, generate_report


def main():
    parser = argparse.ArgumentParser(description="Генератор отчёта по доходам и расходам.")
    parser.add_argument("--input-file", required=True, help="Путь к входному CSV-файлу")
    parser.add_argument("--output-file", help="Путь к выходному TXT-файлу (необязательный)")

    args = parser.parse_args()

    # Загрузка данных из CSV-файла
    data = load_transactions(args.input_file)

    # Вычисление итогов
    totals = calculate_totals(data)

    # Генерация отчёта
    report = generate_report(totals, args.output_file)

    print(report)


if __name__ == "__main__":
    main()
