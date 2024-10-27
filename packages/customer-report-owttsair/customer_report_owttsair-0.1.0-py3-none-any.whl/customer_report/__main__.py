import argparse
from .report import load_data, generate_report, save_report

def main():
    parser = argparse.ArgumentParser(description="Generate customer report from CSV file.")
    parser.add_argument("--input-file", required=True, help="Path to input CSV file.")
    parser.add_argument("--output-file", required=True, help="Path to output text file.")
    args = parser.parse_args()

    data = load_data(args.input_file)
    report_content = generate_report(data)
    save_report(report_content, args.output_file)
    print("Customer report generated successfully.")

if __name__ == "__main__":
    main()
