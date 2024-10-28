import argparse

from .invoice_creator import create_invoice


def main():
    parser = argparse.ArgumentParser(description='Generate an invoice from a JSON file.')
    parser.add_argument('--input-file', required=True, help='Path to the input JSON file')
    parser.add_argument('--output-file', required=True, help='Path to the output text file')

    args = parser.parse_args()

    create_invoice(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
