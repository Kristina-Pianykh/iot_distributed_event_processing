import datetime
import json

from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/")
async def root(request: Request):
    body = await request.body()  # Read the request body
    decoded_message = json.loads(body.decode())
    # event_timestamp = decoded_message.get("Time", "No time provided")
    # decoded_message["Time"] = datetime.datetime.fromtimestamp(event_timestamp)
    # print(decoded_message["Time"].strftime("%Y-%m-%d %H:%M:%S"))

    print(decoded_message)
    return await request.json()
