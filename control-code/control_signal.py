import shared_memory as sh
from time import sleep

def ControlCode():
    while True:
        sh.timeout = 0;
        sh.sem_SSH_ready.acquire()
        print("\033[93m[CONTROL]\033[00m")

        sleep(5)
        sh.timeout = 1;
