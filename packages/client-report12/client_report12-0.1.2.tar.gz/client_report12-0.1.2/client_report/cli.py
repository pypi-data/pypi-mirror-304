import argparse
from client_report.report import load_data, generate_report, save_report


def main():
    parser = argparse.ArgumentParser(description="Генерация отчёта по клиентам.")
    parser.add_argument('--input-file', required=True, help='Путь к входному файлу CSV.')
    parser.add_argument('--output-file', required=True, help='Путь к выходному файлу TXT.')

    args = parser.parse_args()

    # Загружаем данные
    df = load_data(args.input_file)

    # Генерируем отчёт
    report = generate_report(df)

    # Сохраняем отчёт
    save_report(args.output_file, report)


if __name__ == "__main__":
    main()
