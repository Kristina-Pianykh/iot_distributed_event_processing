import datetime
import json
import os
from typing import Optional, Union
from pydantic import BaseModel
# from threading import Thread
import httpx

from PySiddhi.DataTypes.LongType import LongType
from PySiddhi.core.SiddhiManager import SiddhiManager
from PySiddhi.core.query.output.callback.QueryCallback import QueryCallback
from PySiddhi.core.util.EventPrinter import PrintEvent
from fastapi import FastAPI, Request

watch_url = "http://192.168.0.7/post"
app = FastAPI()
os.environ["SIDDHISDK_HOME"] = f"{os.getcwd()}/siddhi-sdk-5.1.0"
# os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64/"
# os.environ["JVM_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"
# os.environ["JAVA_PATH"] = "/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server/libjsig.so"
siddhiManager = SiddhiManager()
query_name = "test"


class Event(BaseModel):
    device_id: str
    sensor_id: str
    sensor_value: Union[float, str]
    timestamp: int

    @classmethod
    def from_string(cls, event_str: str) -> 'Event':
        values = event_str.split(" | ")
        device_id = values[0]
        sensor_id = values[1]
        sensor_value = float(values[2])
        timestamp = int(values[3])
        return cls(device_id=device_id, sensor_id=sensor_id, sensor_value=sensor_value, timestamp=timestamp)


siddhiAppRuntime = None


@app.on_event("startup")
def startup_event():
    # Start the Siddhi app pn fastapi startup
    siddhiApp = f"""
    define stream cseEventStream (device_id string, sensor_id string, sensor_value float, timestamp int);
    define stream outputStream (device_id string, sensor_id string, sensor_value float, timestamp int);

    @info(name = '{query_name}')
    from every e1 = cseEventStream[sensor_id == 'joystick' and sensor_value == 1.0] ->
                 e2 = cseEventStream[sensor_id == 'joystick' and sensor_value == -1.0 and timestamp - e1.timestamp <= 5000]
    select e1.device_id, e1.sensor_id, e1.sensor_value, e1.timestamp
    insert into outputStream;
    """
    global siddhiAppRuntime

    # Generate runtime
    siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(siddhiApp)
    # Add listener to capture output events
    class QueryCallbackImpl(QueryCallback):
        def receive(self, timestamp, inEvents, outEvents):
            PrintEvent(timestamp, inEvents, outEvents)

    siddhiAppRuntime.addCallback(query_name, QueryCallbackImpl())

    # Starting event processing
    siddhiAppRuntime.start()


@app.post("/")
async def recieve_event(request: Request):
    body = await request.body()  # Read the request body
    message = json.loads(body)["Data"]
    event = Event.from_string(message)  # Parse the request body as JSON
    # event = json.loads(body.decode())
    # event_timestamp = decoded_message.get("Time", "No time provided")
    # decoded_message["Time"] = datetime.datetime.fromtimestamp(event_timestamp)
    # print(decoded_message["Time"].strftime("%Y-%m-%d %H:%M:%S"))

    inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")
    inputHandler.send(
        [event.device_id, event.sensor_id, event.sensor_value, event.timestamp]
    )
    print(event)

    # Send a request to the watch
    # payload = json.dumps({"Data": "Hello from the server"})
    # headers = {"Content-Type": "application/json"}
    # response = httpx.post(watch_url, data=payload, headers=headers, timeout=5)

    # if response.status_code == 200:
    #     print("Request sent to watch successfully")
    # else:
    #     print("Failed to send request to watch")

    # return await request.json()
    # return decoded_message
