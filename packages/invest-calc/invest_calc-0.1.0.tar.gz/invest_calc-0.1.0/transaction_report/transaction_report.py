import pandas as pd
import argparse


class TransactionReport:
    def __init__(self, input_file):
        self.input_file = input_file
        self.data = self.load_data()

    def load_data(self):
        return pd.read_csv(self.input_file)

    def generate_report(self):
        report = self.data.groupby('category')['amount'].sum()
        return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, required=True, help='Укажите входной файл .csv.')
    parser.add_argument('--output-file', type=str, required=True, help='Укажите выходной файл .txt.')

    args = parser.parse_args()

    report_generator = TransactionReport(args.input_file)
    report = report_generator.generate_report()

    with open(args.output_file, 'w') as f:
        for category, amount in report.items():
            f.write(f'{category}: {amount:.2f} руб.\n')


if __name__ == '__main__':
    main()
