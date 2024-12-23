from threading import Semaphore

sem_api = Semaphore(0)
"""
#### Semaphore to start the SSH module:
    * aquired by SSH module
    * released by the API module once a request to start the test is received 
"""

sem_SSH_ready = Semaphore(0)
"""
#### Semaphore to start the Sensor-Reader and the Control-Signal modules:
    * aquired by Sensor-Reader and the Control-Signal modules
    * released by the SSH module once a connection has been established with the DUT 
"""

sem_readings_ready = Semaphore(0)
"""
#### Semaphore for the API module send a response back:
    * aquired by API module
    * released by the Sensor-Reader module once the readings shared variable has the force and time values 
"""

sem_feedback_ready = Semaphore(0)
"""
#### Semaphore to alert the modules other than the SSH that the feedback is done:
    * aquired by the API, Control-Signal and Sensor-Reader modules
    * released (n=3) by the SSH module once the connection is closed 
"""

sem_force_read = Semaphore(0)
"""
#### Semaphore for the actuator to stop extending and hold it's position:
    * aquired by the Control-Signal module
    * released by the Sensor-Reader module once a force above 2 newtons is read
"""

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
