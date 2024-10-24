import argparse
from .calculations import load_transactions, group_transactions, generate_report


def main():
    parser = argparse.ArgumentParser(
        description="Загрузка, группировка транзакций и генерация отчёта."
    )
    parser.add_argument(
        '--input-file',
        type=str,
        required=True,
        help='Путь к входному CSV-файлу с транзакциями.'
    )
    parser.add_argument(
        '--output-file',
        type=str,
        required=True,
        help='Путь к выходному текстовому файлу для отчёта.'
    )

    args = parser.parse_args()

    try:
        df = load_transactions(args.input_file)
        report_data = group_transactions(df)
        generate_report(report_data, args.output_file)
        print(f"Отчёт успешно сгенерирован и сохранён в {args.output_file}")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
