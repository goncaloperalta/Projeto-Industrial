from threading import Semaphore

sem_api = Semaphore(0)              # Semaphore to wait for a api start call 
sem_SSH_ready = Semaphore(0)        # Semaphore to wait for a SSH connection
sem_readings_ready = Semaphore(0)   # Semaphore to wait while the readings are not ready

# Shared variable to hold the sensor readings
# {
#     "val": [*, *, *, ...],
#     "time": [*, *, *, ...]
# }
readings = {}
