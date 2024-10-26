import pandas as pd
import argparse


def load_transactions(input_file):
    """Загружает данные о транзакциях из CSV-файла."""
    return pd.read_csv(input_file)


def group_transactions(transactions):
    """Группирует транзакции по категориям."""
    income = transactions[transactions['type'] == 'income']['amount'].sum()
    expenses = transactions[transactions['type'] == 'expense']['amount'].sum()
    return income, expenses


def generate_report(income, expenses, output_file):
    """Генерирует отчет и сохраняет его в файл."""
    with open(output_file, 'w') as f:
        f.write(f"Доход: {income} руб.\n")
        f.write(f"Расход: {expenses} руб.\n")


def main():
    parser = argparse.ArgumentParser(description='Анализ доходов и расходов.')
    parser.add_argument('--input-file', required=True, help='Путь к входному файлу .csv')
    parser.add_argument('--output-file', required=True, help='Путь к выходному файлу .txt')

    args = parser.parse_args()

    transactions = load_transactions(args.input_file)
    income, expenses = group_transactions(transactions)
    generate_report(income, expenses, args.output_file)


if __name__ == '__main__':
    main()