import random
from datetime import datetime, timedelta

TOTAL_LINES = 2_000
OUTPUT_FILE = f"nginx_{TOTAL_LINES}_ddos.log"

normal_ips = [f"192.168.1.{i}" for i in range(10, 150)]
ddos_ips = [f"45.33.32.{i}" for i in range(1, 6)]

paths_normal = [
    "/", "/dashboard", "/api/users", "/api/orders",
    "/static/css/main.css", "/static/js/app.js",
    "/health", "/metrics"
]

paths_ddos = [
    "/login", "/api/login", "/api/auth",
    "/api/users", "/"
]

user_agents_normal = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0)"
]

user_agents_bots = [
    "curl/8.1.0",
    "python-requests/2.31.0",
    "Go-http-client/1.1",
    "botnet/1.0"
]

status_normal = [200, 200, 200, 304, 404]
status_ddos = [429, 429, 444, 504, 403]

start_time = datetime.now() - timedelta(minutes=10)

def log_line(ip, path, status, size, ua, time):
    return (
        f'{ip} - - '
        f'[{time.strftime("%d/%b/%Y:%H:%M:%S +0000")}] '
        f'"GET {path} HTTP/1.1" {status} {size} "-" "{ua}"'
    )

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for i in range(TOTAL_LINES):
        timestamp = start_time + timedelta(milliseconds=i * random.randint(5, 30))

        # 30% traffic is DDoS
        if random.random() < 0.3:
            ip = random.choice(ddos_ips)
            path = random.choice(paths_ddos)
            ua = random.choice(user_agents_bots)
            status = random.choice(status_ddos)
            size = random.randint(0, 300)
        else:
            ip = random.choice(normal_ips)
            path = random.choice(paths_normal)
            ua = random.choice(user_agents_normal)
            status = random.choice(status_normal)
            size = random.randint(200, 15000)

        f.write(log_line(ip, path, status, size, ua, timestamp) + "\n")

print(f"Generated {TOTAL_LINES} lines in {OUTPUT_FILE}")
