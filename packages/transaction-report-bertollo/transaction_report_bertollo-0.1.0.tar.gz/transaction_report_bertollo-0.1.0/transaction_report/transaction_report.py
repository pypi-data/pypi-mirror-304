import pandas as pd


class TransactionReport:
    def __init__(self, input_file):
        self.input_file = input_file
        self.data = pd.read_csv(input_file)

    def generate_report(self):
        income = self.data[self.data['category'] == 'Доход']['amount'].sum()
        expenses = self.data[self.data['category'] == 'Расход']['amount'].sum()

        report = {}
        report['Income'] = income.sum()
        report['Expense'] = expenses.sum()

        return report

    def save_report(self, output_file):
        report = self.generate_report()
        with open(output_file, 'w') as f:
            for category, amount in report.items():
                f.write(f'{category}: {amount} руб.\n')
