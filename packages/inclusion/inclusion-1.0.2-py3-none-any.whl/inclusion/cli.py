import argparse
from inclusion import scan  # Adjust if your file is named differently

def print_vulnerability(test_url):
    print(f"Inclusion vulnerability found: {test_url}")

def main():
    parser = argparse.ArgumentParser(description="Check for file inclusion vulnerabilities on a given URL.")
    parser.add_argument("--url", required=True, help="The URL of the website to check (e.g., example.com)")
    parser.add_argument("--payload", help="Path to a custom payload file")

    args = parser.parse_args()

    scan(args.url, args.payload, print_vulnerability)  # Pass the print function

if __name__ == "__main__":
    main()
