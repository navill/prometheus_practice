import random
import time

import requests

while True:
    rand_int = random.randint(0, 2000)
    time.sleep(random.uniform(0, 5))
    if rand_int == 0:
        print("not found")
    if 1000 <= rand_int <= 1500:
        requests.get(f"http://localhost:8080/api/")
    else:
        # rand_int: 1~1000일 경우 status 200, 1501~2000일 경우 status 404
        requests.get(f"http://localhost:8080/api/{rand_int}/")
