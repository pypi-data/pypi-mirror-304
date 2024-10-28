import argparse
import pandas as pd
from .report import generate_report

def main():
    parser = argparse.ArgumentParser(description='Sales report generator.')
    parser.add_argument('--input-file', type=str, required=True, help='Path to input CSV file')
    parser.add_argument('--output-file', type=str, required=True, help='Path to output CSV file')

    args = parser.parse_args()

    # Генерация отчета
    report = generate_report(args.input_file)

    # Сохранение отчета в файл
    report.to_csv(args.output_file, index=False)

if __name__ == '__main__':
    main()
