import pandas as pd

class FinancialReport:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.data = None

    def load_data(self):
        """Загружает данные о транзакциях из CSV."""
        self.data = pd.read_csv(self.csv_file)

    def categorize_transactions(self):
        """Группирует транзакции по категориям."""
        grouped = self.data.groupby("category")["amount"].sum()
        return grouped

    def generate_report(self):
        """Создаёт отчёт с суммами для каждой категории."""
        report_data = self.categorize_transactions()
        report = ""
        for category, total in report_data.items():
            report += f"{category.capitalize()}: {total} руб.\n"
        return report
