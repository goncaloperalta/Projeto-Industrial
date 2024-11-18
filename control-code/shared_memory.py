from threading import Semaphore

sem_api = Semaphore(0)              # Semaphore to wait for the api start 
sem_readings_ready = Semaphore(0)   # Semaphore to wait until the readings are not ready

# Shared variable to hold the sensor readings
# {
#     "val": [*, *, *, ...],
#     "time": [*, *, *, ...]
# }
readings = {}
