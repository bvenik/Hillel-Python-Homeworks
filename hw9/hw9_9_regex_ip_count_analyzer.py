from collections import Counter
from hw9_7_regex_ip_finder import extract_ip_addresses as extract_ips


def analyze_server_logs(log_data: str):
    """
    Аналізує дані логів і підраховує кількість запитів з кожної IP-адреси.
    """
    ips = extract_ips(log_data)
    ip_counts = Counter(ips)

    for ip, count in ip_counts.most_common():
        print(f"IP: {ip} ---- Appear count: {count}")


if __name__ == "__main__":
    server_logs = """
    192.168.1.1 - - [12/Apr/2026:14:20:01] "GET /index.html HTTP/1.1" 200
    10.0.0.5 - - [12/Apr/2026:14:20:05] "POST /login HTTP/1.1" 401
    192.168.1.1 - - [12/Apr/2026:14:21:10] "GET /styles.css HTTP/1.1" 200
    172.16.254.1 - - [12/Apr/2026:14:22:15] "GET /logo.png HTTP/1.1" 200
    192.168.1.1 - - [12/Apr/2026:14:23:01] "GET /favicon.ico HTTP/1.1" 404
    10.0.0.5 - - [12/Apr/2026:14:23:45] "GET /home HTTP/1.1" 200
    """

    analyze_server_logs(server_logs)
