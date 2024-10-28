import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def load_payloads(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []

def format_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return url

def check_file_inclusion(url, payloads):
    vulnerabilities = []
    for vector in payloads:
        test_url = f"{url}?file={vector}"
        try:
            response = requests.get(test_url, timeout=5)
            if response.status_code == 200 and "root" in response.text:
                vulnerabilities.append(vector)
        except requests.RequestException:
            continue
    return vulnerabilities

def main(url=None, payload_file="inclusion/list.txt"):
    payloads = load_payloads(payload_file)
    if url:
        formatted_url = format_url(url)
        return check_file_inclusion(formatted_url, payloads)
    return ["Please provide a URL using --url."]
