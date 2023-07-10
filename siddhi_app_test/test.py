import os
import time
from typing import Optional, Union
from pydantic import BaseModel
from PySiddhi.core.SiddhiManager import SiddhiManager
from PySiddhi.core.query.output.callback.QueryCallback import QueryCallback
from PySiddhi.core.util.EventPrinter import PrintEvent

# os.environ["SIDDHISDK_HOME"] = f"{os.getcwd()}/siddhi-sdk-5.1.0"
# print(os.getenv("SIDDHISDK_HOME"))
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


siddhiAppRuntime = None



# Start the Siddhi app pn fastapi startup
siddhiApp = f"""
define stream cseEventStream (device_id string, sensor_id string, sensor_value float, timestamp int);

@info(name = '{query_name}')
from every e1 = cseEventStream[sensor_id == 'joystick' and sensor_value == 1.0] ->
                e2 = cseEventStream[sensor_id == 'joystick' and sensor_value == -1.0 and timestamp - e1.timestamp <= 5000]
select e1.device_id as device_id_1, e2.device_id as device_id_2, e1.sensor_id as sensor_id_1, e2.sensor_id as sensor_id_2, e1.sensor_value as sensor_value_1, e2.sensor_value as sensor_value_2, e1.timestamp as timestamp1, e2.timestamp as timestamp2
insert into outputStream;
"""

# Generate runtime
siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(siddhiApp)
# Add listener to capture output events
class QueryCallbackImpl(QueryCallback):
    def receive(self, timestamp, inEvents, outEvents):
        PrintEvent(timestamp, inEvents, outEvents)

siddhiAppRuntime.addCallback(query_name, QueryCallbackImpl())

# Starting event processing
siddhiAppRuntime.start()

event1 = Event(device_id="1", sensor_id="joystick", sensor_value=1.0, timestamp=int(time.time()))
time.sleep(1)
event2 = Event(device_id="2", sensor_id="joystick", sensor_value=1.0, timestamp=int(time.time()))
time.sleep(0.5)
event3 = Event(device_id="3", sensor_id="joystick", sensor_value=0.1, timestamp=int(time.time()))
event4 = Event(device_id="4", sensor_id="joystick", sensor_value=1.0, timestamp=int(time.time()))
time.sleep(0.8)
event5 = Event(device_id="5", sensor_id="joystick", sensor_value=-0.1, timestamp=int(time.time()))
event6 = Event(device_id="6", sensor_id="joystick", sensor_value=-1.0, timestamp=int(time.time()))



inputHandler = siddhiAppRuntime.getInputHandler("cseEventStream")
for event in [event1, event2, event3, event4, event5, event6]:
    inputHandler.send(
        [event.device_id, event.sensor_id, event.sensor_value, event.timestamp]
    )
    # print(event)
