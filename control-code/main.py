import threading
from api import app
from sensor_reader import SensorReader
import uvicorn

def start_api():
    uvicorn.run(app, host='0.0.0.0', port=8000, timeout_keep_alive=5000)

def start_sensor():
    SensorReader()

def main():
    APIth = threading.Thread(target=start_api)
    SENSORth = threading.Thread(target=start_sensor)

    APIth.start()
    SENSORth.start()

    APIth.join()
    SENSORth.join()

if __name__ == '__main__':
    main()