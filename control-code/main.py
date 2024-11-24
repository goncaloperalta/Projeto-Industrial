import uvicorn
import threading
from api import app
from ssh import SSHConnect
from control_signal import ControlCode
from sensor_reader import SensorReader

def StartAPI():
    uvicorn.run(app, host='0.0.0.0', port=8000, timeout_keep_alive=10000)

def main():
    APIth = threading.Thread(target=StartAPI)
    SSHth = threading.Thread(target=SSHConnect)
    CONTROLth = threading.Thread(target=ControlCode)
    SENSORth = threading.Thread(target=SensorReader)
    
    APIth.start()
    SSHth.start()
    CONTROLth.start()
    SENSORth.start()

    APIth.join()
    SSHth.join()
    CONTROLth.join()
    SENSORth.join()

if __name__ == '__main__':
    main()