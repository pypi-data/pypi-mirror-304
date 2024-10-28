import argparse

from .sales_report import generate_report


def main():
    parser = argparse.ArgumentParser(description='Generate sales report from CSV file.')
    parser.add_argument('--input-file', required=True, help='Path to the input CSV file')
    parser.add_argument('--output-file', required=True, help='Path to the output CSV file')

    args = parser.parse_args()

    generate_report(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
