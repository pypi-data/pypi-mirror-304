import argparse
from financial_report import FinancialReport


def main():
    parser = argparse.ArgumentParser(description="Анализ финансовых транзакций.")
    parser.add_argument("--input-file", required=True, help="Путь к входному CSV-файлу.")
    parser.add_argument("--output-file", required=True, help="Путь к выходному TXT-файлу.")

    args = parser.parse_args()

    report = FinancialReport(args.input_file)
    report.load_data()
    output = report.generate_report()

    with open(args.output_file, "w") as file:
        file.write(output)


if __name__ == "__main__":
    main()
