import argparse
from .report_generator import load_data, calculate_totals, save_report

def main():
    parser = argparse.ArgumentParser(description="Generate financial report.")
    parser.add_argument("--input-file", required=True, help="Path to input CSV file.")
    parser.add_argument("--output-file", required=True, help="Path to output TXT file.")
    args = parser.parse_args()

    data = load_data(args.input_file)
    totals = calculate_totals(data)
    save_report(totals, args.output_file)

if __name__ == "__main__":
    main()
