import json
import os
from parse import Event

from rainbow_leds import flash_rainbow

from PySiddhi.core.SiddhiManager import SiddhiManager
from PySiddhi.core.query.output.callback.QueryCallback import QueryCallback
from PySiddhi.core.util.EventPrinter import PrintEvent
from fastapi import FastAPI, Request


app = FastAPI()
os.environ["SIDDHISDK_HOME"] = f"{os.getcwd()}/../siddhi-sdk-5.1.2"


siddhiManager = SiddhiManager()
query_names = ["test1", "test2"]
siddhiAppRuntime = None


@app.on_event("startup")
def startup_event():
    # Start the Siddhi app pn fastapi startup
    siddhiApp = f"""
    define stream cseEventStream (device_id string, sensor_id string, sensor_value float, timestamp int);
    define stream outputStream (device_id string, sensor_id string, sensor_value float, timestamp int);

    @info(name = 'test1')
    from every e1 = cseEventStream[sensor_id == 'joystick' and sensor_value == 1.0] ->
                 e2 = cseEventStream[sensor_id == 'sound' and sensor_value == 1.0 and timestamp - e1.timestamp <= 5000]
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
            flash_rainbow()  # Flash the rainbow LEDs on the watch

    for query_name in ["test1"]:
        siddhiAppRuntime.addCallback(query_name, QueryCallbackImpl())

    # Starting event processing
    siddhiAppRuntime.start()


@app.post("/")
async def recieve_event(request: Request):
    body = await request.body()  # Read the request body
    message = json.loads(body)
    try:
        event = Event.from_pi(message)  # if an event comes from a pi
    except Exception:
        event = Event.from_watch(message)

    inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")
    inputHandler.send(
        [event.device_id, event.sensor_id, event.sensor_value, event.timestamp]
    )
    print(event)


@app.get("/match")
async def flash_lights(request: Request):
    flash_rainbow()
    return "OK"


@app.get("/health")
async def check_health(request: Request):
    """check if the server is healthy"""
    return "OK"
