import argparse
import pandas as pd
from package_5 import analyze_customers

def main():
    parser = argparse.ArgumentParser(description="Анализ клиентской базы")
    parser.add_argument("--input-file", required=True, help="Путь к входному файлу .csv")
    parser.add_argument("--output-file", required=True, help="Путь к выходному файлу .txt")
    args = parser.parse_args()

    customers_data = pd.read_csv(args.input_file)

    report = analyze_customers(customers_data)

    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(report)

if __name__ == "__main__":
    main()
