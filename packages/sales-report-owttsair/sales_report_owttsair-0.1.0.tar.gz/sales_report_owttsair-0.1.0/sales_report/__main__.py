import argparse
from .report_generator import load_data, generate_report, save_report

def main():
    parser = argparse.ArgumentParser(description="Generate sales report.")
    parser.add_argument("--input-file", required=True, help="Path to input CSV file.")
    parser.add_argument("--output-file", required=True, help="Path to output CSV file.")
    args = parser.parse_args()

    data = load_data(args.input_file)
    report = generate_report(data)
    save_report(report, args.output_file)

if __name__ == "__main__":
    main()
