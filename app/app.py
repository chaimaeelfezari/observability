from prometheus_client import start_http_server, Counter, Gauge
import time, random

REQUESTS = Counter('app_requests_total', 'Total requests')
ACTIVE_USERS = Gauge('app_active_users', 'Active users')

if __name__ == '__main__':
    start_http_server(8000)
    print("App running on :8000")
    while True:
        REQUESTS.inc()
        ACTIVE_USERS.set(random.randint(1, 100))
        time.sleep(5)