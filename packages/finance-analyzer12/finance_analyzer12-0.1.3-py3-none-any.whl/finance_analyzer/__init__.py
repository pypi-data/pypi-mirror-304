from .analyzer import load_transactions, group_transactions, generate_report
import argparse


def main():
    """Основная функция для анализа финансов с интерфейсом для пользователя."""
    parser = argparse.ArgumentParser(description='Анализ доходов и расходов.')
    parser.add_argument('--input-file', required=True, help='Путь к входному файлу .csv')
    parser.add_argument('--output-file', required=True, help='Путь к выходному файлу .txt')

    args = parser.parse_args()

    # Загрузка данных
    transactions = load_transactions(args.input_file)

    # Группировка данных
    income, expenses = group_transactions(transactions)

    # Генерация отчета
    generate_report(income, expenses, args.output_file)


if __name__ == '__main__':
    main()