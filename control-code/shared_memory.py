from threading import Semaphore

sem_api = Semaphore(0)              # Semaphore to wait for a api start call
sem_SSH_ready = Semaphore(0)        # Semaphore to wait for a SSH connection
sem_readings_ready = Semaphore(0)   # Semaphore to wait while the readings are not ready
sem_feedback_ready = Semaphore(0)   # Semaphore to wait while the feedback has not happened
sem_actuator_end = Semaphore(0)
sem_stop_control = Semaphore(0)
sem_force_read = Semaphore(0)

readings = {}   # Holds the sensor readings
feedback = {}   # Holds the button feedback
timeout = 0
stopSensor = 0
pressTime = 0
