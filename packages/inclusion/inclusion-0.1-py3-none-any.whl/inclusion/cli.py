import argparse
from inclusion.scanner import main

def print_report(report_data):
    if report_data:
        for line in report_data:
            print(line, end='')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check for file inclusion vulnerabilities.")
    parser.add_argument("--url", help="The URL of the website to check (e.g., https://example.com)", required=True)
    parser.add_argument("--list", help="Path to file containing custom payloads", default="inclusion/list.txt")
    args = parser.parse_args()
    report_data = main(url=args.url, payload_file=args.list)
    print_report(report_data)
