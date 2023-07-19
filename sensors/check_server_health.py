import httpx
import time
from utils import set_constants
import sys

constants = set_constants()
health_endpoints = [f"{url}/health" for url in constants["urls"]]
time_update = {endpoint: time.time() for endpoint in health_endpoints}

idx = 0
while idx < len(health_endpoints):
    url = health_endpoints[idx]
    try:
        response = httpx.get(url)
        if response.status_code == 200:
            print(f"Server on {url} is healthy")
            idx += 1
    except Exception as e:
        if time.time() - time_update[url] > 2:
            print(f"Waiting for the http server on {url} to start up...")
            sys.stdout.flush() # flush the buffer
            time_update[url] = time.time()
        continue

print("All urls are healthy")
