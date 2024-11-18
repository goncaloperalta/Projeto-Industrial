from threading import Semaphore

sem_api = Semaphore(0)
sem_readings_ready = Semaphore(0)

readings = {}
