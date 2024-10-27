import pandas as pd


def load_transactions(file_path):

    try:
        data = pd.read_csv(file_path)
    except Exception as e:
        raise Exception(f"Ошибка при загрузке файла: {e}")

    if 'category' not in data.columns or 'amount' not in data.columns:
        raise ValueError("Файл должен содержать колонки 'category' и 'amount'")

    return data


def calculate_totals(data):

    grouped = data.groupby('category')['amount'].sum()
    return grouped.to_dict()


def generate_report(totals, output_file=None):

    report_lines = [f"{category.capitalize()}: {amount} руб." for category, amount in totals.items()]
    report = "\n".join(report_lines)

    if output_file:
        with open(output_file, 'w') as f:
            f.write(report)

    return report
