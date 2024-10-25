import argparse
from .analyze import analyze_transactions

def main():
    parser = argparse.ArgumentParser(description='Analyze financial transactions and generate a report.')
    parser.add_argument('--input-file', required=True, help='Path to the input CSV file')
    parser.add_argument('--output-file', required=True, help='Path to the output text file')

    args = parser.parse_args()

    analyze_transactions(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
