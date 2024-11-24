from threading import Semaphore

sem_api = Semaphore(0)              # Semaphore to wait for a api start call 
sem_SSH_ready = Semaphore(0)        # Semaphore to wait for a SSH connection
sem_readings_ready = Semaphore(0)   # Semaphore to wait while the readings are not ready
sem_feedback_ready = Semaphore(0)   # Semaphore to wait while the feedback has not happened

readings = {}   # Holds the sensor readings
feedback = ""   # Holds the button feedback
timeout = 0     # Flag for timeout
