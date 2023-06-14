import datetime
import json

import httpx
from fastapi import FastAPI, Request

watch_url = "http://192.168.0.7/post"
app = FastAPI()


@app.post("/")
async def root(request: Request):
    body = await request.body()  # Read the request body
    decoded_message = json.loads(body.decode())
    # event_timestamp = decoded_message.get("Time", "No time provided")
    # decoded_message["Time"] = datetime.datetime.fromtimestamp(event_timestamp)
    # print(decoded_message["Time"].strftime("%Y-%m-%d %H:%M:%S"))

    print(decoded_message)

    # Send a request to the watch
    payload = json.dumps({"Data": "Hello from the server"})
    headers = {"Content-Type": "application/json"}
    response = httpx.post(watch_url, data=payload, headers=headers, timeout=5)

    if response.status_code == 200:
        print("Request sent to watch successfully")
    else:
        print("Failed to send request to watch")

    return await request.json()
