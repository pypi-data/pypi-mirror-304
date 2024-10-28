from .scanner import main, check_file_inclusion, load_payloads, format_url

def scan(url, payload_file="inclusion/list.txt"):
    payloads = load_payloads(payload_file)
    return check_file_inclusion(format_url(url), payloads)
