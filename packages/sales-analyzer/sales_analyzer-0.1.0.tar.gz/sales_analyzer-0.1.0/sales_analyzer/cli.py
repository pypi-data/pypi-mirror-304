import argparse
from .analyze import analyze_sales


def main():
    parser = argparse.ArgumentParser(description='Analyze sales data and generate a report.')

    parser.add_argument('--input-file', required=True, help='Path to the input CSV file')
    parser.add_argument('--output-file', required=True, help='Path to the output CSV file')

    args = parser.parse_args()

    analyze_sales(args.input_file, args.output_file)


if __name__ == '__main__':
    main()
