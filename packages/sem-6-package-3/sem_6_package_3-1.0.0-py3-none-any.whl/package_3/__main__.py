import argparse
import pandas as pd
from package_3 import analyze_sales

def main():
    parser = argparse.ArgumentParser(description="Анализ данных о продажах")
    parser.add_argument("--input-file", required=True, help="Путь к входному файлу .csv")
    parser.add_argument("--output-file", required=True, help="Путь к выходному файлу .csv")
    args = parser.parse_args()

    sales_data = pd.read_csv(args.input_file)

    report = analyze_sales(sales_data)

    report.to_csv(args.output_file, index=False)

if __name__ == "__main__":
    main()