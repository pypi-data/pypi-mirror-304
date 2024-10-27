import argparse
import pandas as pd
from package_2 import analyze_transactions

def main():
    parser = argparse.ArgumentParser(description="Анализ финансовых транзакций")
    parser.add_argument("--input-file", required=True, help="Путь к входному файлу .csv")
    parser.add_argument("--output-file", required=True, help="Путь к выходному файлу .txt")
    args = parser.parse_args()

    transactions = pd.read_csv(args.input_file)

    report = analyze_transactions(transactions)

    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(report)

if __name__ == "__main__":
    main()