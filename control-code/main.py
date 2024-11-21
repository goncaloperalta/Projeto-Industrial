import threading
from api import app
from sensor_reader import SensorReader
from ssh import SSHConnect
import uvicorn

def start_api():
    uvicorn.run(app, host='0.0.0.0', port=8000, timeout_keep_alive=5000)

def start_ssh():
    SHHConnect()

def start_sensor():
    SensorReader()

def main():
    SENSORth = threading.Thread(target=start_sensor)
    SSHth = threading.Thread(target=start_ssh)
    APIth = threading.Thread(target=start_api)

    APIth.start()
    SENSORth.start()
    SSHth.start()

    APIth.join()
    SENSORth.join()
    SSHth.join()

if __name__ == '__main__':
    main()