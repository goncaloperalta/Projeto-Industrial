import re
import paramiko
import shared_memory as sh
import credentials
from time import sleep

def processCommand(cmd: str):
    regex = re.search(r"Button (\d+) Press --(.*?)\n", cmd)
    if regex:
        button = regex.group(1)
        func = regex.group(2).strip()
    else:
        button = None
        func = None

    if button == '2':
        button = 'WPS'
    else:
        button = 'INFO/WIFI'

    regex = re.search(r"timeInMs:(\d+)", cmd)
    if regex:
        timePressed = regex.group(1)
    else:
        timePressed = None
    
    regex = re.search(r"PTIN Botton: (PTIN_BP_BTN_FAMILY_\S+)", cmd)
    if regex:
        family = regex.group(1)
    else:
        family = None
    
    regex = re.search(r"cnt:(\d+)", cmd)
    if regex:
        counter = regex.group(1)
    else:
        counter = None
    
    return {
        'button': button,
        'func': func,
        'timePressed': timePressed,
        'family': family,
        'counter': counter
    }

def SSHConnect():
    while True:
        sh.sem_api.acquire()        # Wait for a request

        # Connect
        print("\033[96m[SSH] Connecting to gateway...\033[00m")
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect("192.168.1.1", username=credentials.host, password=credentials.passw)
        print("\033[96m[SSH] Connected to gateway\033[00m")
        client.exec_command("dmesg -c") # Clear the ring

        # Alert the sensor_reader and the control_signal that the SSH connection has been established
        sh.sem_SSH_ready.release(n=2)

        # Exec
        stdout = ""
        string = ""
        print("\033[96m[SSH] Polling command: dmesg | grep \"Button\|PTIN\|ptin_hotplug_state\"\033[00m")
        while not sh.timeout:
            string = ""  # Reset string
            stdin, stdout, stderr = client.exec_command("dmesg | grep \"Button\|PTIN\|ptin_hotplug_state\"")
            sleep(1)  # Wait between iterations
            for line in stdout:
                string += line

            stdin, stdout, stderr = client.exec_command("dmesg | grep \"Button\|PTIN\|ptin_hotplug_state\"")
            for line in stdout:
                string += line

            # If valid break
            if "Button" in string:
                break

        print("\033[96m[SSH] Got a feedback from a button\033[00m")

        # Close Connection
        print("\033[96m[SSH] Closing connection to gateway...\033[00m")
        client.close()
        print("\033[96m[SSH] Connection closed\033[00m")

        # Process command
        print("\033[96m[SSH] Processing command...\033[00m")
        print(string)
        sh.feedback = processCommand(string)

        # Alert the API that the feedback is ready
        sh.sem_feedback_ready.release()
