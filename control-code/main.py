import uvicorn
import logging
import threading
from api import app
from state import State
from ssh import SSHConnect
from sensor_reader import SensorReader
from control_signal import ControlCode

def setupLogging():
    logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def StartAPI():
    uvicorn.run(app, host='0.0.0.0', port=8000, timeout_keep_alive=10000)

def main():
    setupLogging()

    APIth = threading.Thread(target=StartAPI)
    STATEth = threading.Thread(target=State)
    SSHth = threading.Thread(target=SSHConnect)
    CONTROLth = threading.Thread(target=ControlCode)
    SENSORth = threading.Thread(target=SensorReader)
    
    APIth.start()
    STATEth.start()
    SSHth.start()
    CONTROLth.start()
    SENSORth.start()

    APIth.join()
    STATEth.join()
    SSHth.join()
    CONTROLth.join()
    SENSORth.join()

if __name__ == '__main__':
    main()
