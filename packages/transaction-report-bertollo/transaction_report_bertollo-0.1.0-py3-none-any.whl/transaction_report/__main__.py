import argparse
from .transaction_report import TransactionReport

def main():
    parser = argparse.ArgumentParser(description='Generate a transaction report from a CSV file.')
    parser.add_argument('--input-file', type=str, required=True, help='Path to the input CSV file.')
    parser.add_argument('--output-file', type=str, required=True, help='Path to the output TXT file.')

    args = parser.parse_args()

    report = TransactionReport(args.input_file)
    report.save_report(args.output_file)


if __name__ == '__main__':
    main()
