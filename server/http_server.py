import json
import os
from parse import Event, send_event, config, watch_events

from rainbow_leds import flash_rainbow

from PySiddhi.core.SiddhiManager import SiddhiManager
from PySiddhi.core.query.output.callback.QueryCallback import QueryCallback
from PySiddhi.core.util.EventPrinter import PrintEvent
from fastapi import FastAPI, Request


device_id = os.getenv("DEVICE_ID")
app = FastAPI()
os.environ["SIDDHISDK_HOME"] = f"{os.getcwd()}/../siddhi-sdk-5.1.2"


siddhiManager = SiddhiManager()
siddhiAppRuntime = None
pi4_url = f"http://{config['pis']['pi_4']['ip']}:8000"


@app.on_event("startup")
def startup_event():
    # Start the Siddhi app pn fastapi startup
    siddhiApp = f"""
    define stream cseEventStream (device_id string, sensor_id string, sensor_value float, timestamp int);
    define stream outputStream (device_id string, sensor_id string, sensor_value float, timestamp int,
                                device_id1 string, sensor_id1 string, sensor_value1 float, timestamp1 int);
    define stream complexOutputStream (device_id1 string, sensor_id1 string, sensor_value1 float, timestamp1 int,
                                        device_id2 string, sensor_id2 string, sensor_value2 float, timestamp2 int,
                                        device_id3 string, sensor_id3 string, sensor_value3 float, timestamp3 int,
                                        device_id4 string, sensor_id4 string, sensor_value4 float, timestamp4 int);

    @info(name = 'joystick')
    from every e1 = cseEventStream[sensor_id == 'joystick' and sensor_value == 1.0] ->
                 e2 = cseEventStream[sensor_id == 'joystick' and sensor_value == -1.0 and timestamp - e1.timestamp <= 5000]
    select e1.device_id, e1.sensor_id, e1.sensor_value, e1.timestamp,
            e2.device_id as device_id1, e2.sensor_id as sensor_id1, e2.sensor_value as sensor_value1, e2.timestamp as timestamp1
    insert into outputStream;

    @info(name = 'joystick_sound')
    from every e1 = cseEventStream[sensor_id == 'joystick' and sensor_value == 1.0] ->
                e2 = cseEventStream[sensor_id == 'joystick' and sensor_value == -1.0 and timestamp - e1.timestamp <= 5000] ->
                 e3 = cseEventStream[sensor_id == 'sound' and sensor_value == 1.0 and timestamp - e2.timestamp <= 5000]
    select e1.device_id, e1.sensor_id, e1.sensor_value, e1.timestamp,
            e2.device_id as device_id_pi3, e2.sensor_id as sensor_id_pi3, e2.sensor_value as sensor_value_pi3, e2.timestamp as timestamp_pi3,
            e3.device_id as device_id_pi4, e3.sensor_id as sensor_id_pi4, e3.sensor_value as sensor_value_pi4, e3.timestamp as timestamp_pi4
    insert into p4outputStream;

    @info(name = 'joystick_gyro')
    from every e1 = cseEventStream[sensor_id == 'joystick' and sensor_value == 1.0] ->
                e2 = cseEventStream[sensor_id == 'gyro' and sensor_value == 3.0 and timestamp - e1.timestamp <= 10000]
    select e1.device_id, e1.sensor_id, e1.sensor_value, e1.timestamp,
            e2.device_id as device_id1, e2.sensor_id as sensor_id1, e2.sensor_value as sensor_value1, e2.timestamp as timestamp1
    insert into outputStream;

    @info(name = 'complex_event')
    from every gyro = cseEventStream[sensor_id == 'gyro' and sensor_value == 3.0] ->
                touch = cseEventStream[sensor_id == 'touch' and sensor_value == 1.0 and timestamp - gyro.timestamp <= 1000] ->
                 timer = cseEventStream[sensor_id == 'timer' and sensor_value == 1.0 and (timestamp - touch.timestamp <= 10000 or timestamp - gyro.timestamp <= 10000)] or joystick = cseEventStream[sensor_id == 'joystick' and sensor_value == 1.0]
    select gyro.device_id as device_id1, gyro.sensor_id as sensor_id1, gyro.sensor_value as sensor_value1, gyro.timestamp as timestamp1,
            touch.device_id as device_id2, touch.sensor_id as sensor_id2, touch.sensor_value as sensor_value2, touch.timestamp as timestamp2,
            timer.device_id as device_id3, timer.sensor_id as sensor_id3, timer.sensor_value as sensor_value3, timer.timestamp as timestamp3,
            joystick.device_id as device_id4, joystick.sensor_id as sensor_id4, joystick.sensor_value as sensor_value4, joystick.timestamp as timestamp4
    insert into complexOutputStream;
    """
    # OR(SEQ(AND(gyro=3, touch=1), Timer=1), joystick)
    global siddhiAppRuntime

    # Generate runtime
    siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(siddhiApp)
    # Add listener to capture output events
    class QueryCallbackImpl(QueryCallback):
        def receive(self, timestamp, inEvents, outEvents):
            print("Printing inEvents")
            for event in inEvents:
                parsed_event = event.getData()
                print(parsed_event)
                if device_id == "pi_3":
                    send_event(urls=[pi4_url], device_id=parsed_event[0], sensor=parsed_event[1], sensor_val=parsed_event[2], timestamp=parsed_event[3])
            # PrintEvent(timestamp, inEvents, outEvents)
            flash_rainbow()  # Flash the rainbow LEDs on the watch

    for query_name in ["joystick_gyro"]:
        siddhiAppRuntime.addCallback(query_name, QueryCallbackImpl())

    # Starting event processing
    siddhiAppRuntime.start()


@app.post("/")
async def recieve_event(request: Request):
    body = await request.body()  # Read the request body
    message = json.loads(body)
    print(body)
    try:
        event = Event.from_pi(message)  # if an event comes from a pi
        inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")
        inputHandler.send(
            [event.device_id, event.sensor_id, event.sensor_value, event.timestamp]
        )
        print(event)
    except Exception:
        for sensor_id, metadata in message.items():
            if sensor_id.lower() != "timestamp": # dirty hack, change to is sensor id not in watch events
                event = Event.from_watch(sensor_id, metadata)
                inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")
                inputHandler.send(
                    [event.device_id, event.sensor_id, event.sensor_value, event.timestamp]
                )
                print(event)

    # inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")
    # inputHandler.send(
    #     [event.device_id, event.sensor_id, event.sensor_value, event.timestamp]
    # )
    # print(event)


@app.get("/match")
async def flash_lights(_: Request):
    flash_rainbow()
    return "OK"


@app.get("/health")
async def check_health(_: Request):
    """check if the server is healthy"""
    return "OK"
