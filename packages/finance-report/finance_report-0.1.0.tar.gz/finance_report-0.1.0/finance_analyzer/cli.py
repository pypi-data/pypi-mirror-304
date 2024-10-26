import argparse
from finance_analyzer.report_generator import load_transactions, calculate_totals, generate_report


def main():
    parser = argparse.ArgumentParser(description="Генератор отчёта по доходам и расходам.")
    parser.add_argument("--input-file", required=True, help="Путь к входному CSV-файлу")
    parser.add_argument("--output-file", help="Путь к выходному TXT-файлу (опционально)")

    args = parser.parse_args()

    data = load_transactions(args.input_file)
    totals = calculate_totals(data)
    report = generate_report(totals, args.output_file)

    print(report)
