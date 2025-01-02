from enum import Enum
from threading import Semaphore, Lock

access = Lock()
"""
Mutex to limit the access to the shared variables:
"""

startTest = Semaphore(0)
"""
#### Semaphore to start the test:
    * aquired by State module
    * released by the API module once a request to start the test is received 
"""

startSSH = Semaphore(0)
"""
#### Semaphore to start the SSH module:
    * aquired by SSH module
    * released by the State module 
"""

startSensorAndControl = Semaphore(0)
"""
#### Semaphore to start the Sensor-Reader and the Control-Signal modules:
    * aquired by Sensor-Reader and the Control-Signal modules
    * released by the SSH module once a connection has been established with the DUT 
"""

sensorReadingsReady = Semaphore(0)
"""
#### Semaphore for the API module send a response back:
    * aquired by API module
    * released by the Sensor-Reader module once the readings shared variable has the force and time values 
"""

feedbackReady = Semaphore(0)
"""
#### Semaphore to alert the modules other than the SSH that the feedback is done:
    * aquired by the API, Control-Signal and Sensor-Reader modules
    * released (n=3) by the SSH module once the connection is closed 
"""

buttonPressed = Semaphore(0)
"""
#### Semaphore for the actuator to stop extending and hold it's position:
    * aquired by the Control-Signal module
    * released by the Sensor-Reader module once a force above 2 newtons is read
"""

class state(Enum):
    """Enum with types of state"""
    READY = 1
    RUNNING = 2
    ABORT = 3

STATE = state.READY
"""Shared variable to store the current state of the system"""

class Parameters():
    pressTime : int
    nTimes : int
    interval : int
parameters : Parameters

readings = {}
"""
Shared variable to store the force sensor readings:

>>> readings = {
    'val' = []  # force values
    'time' = [] # time values
}
"""

feedback = {}
"""
Shared variable to store the button feedback:
>>> feedback = {
    'button': 'None',   # button pressed: wps/info/reset/none
    'success': success  # success: 1/0
}
"""

timeout = 0
"""
Timeout flag in case no feedback is sent by the button press
"""

stopSensor = 0
"""
Shared variable to stop the force reading loop
"""

pressTime = 0
"""
Shared variable to hold the argument from the /start endpoint
"""
