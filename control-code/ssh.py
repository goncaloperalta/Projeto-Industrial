import paramiko
import shared_memory as sh
import credentials
from time import sleep

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
        print("\033[96m[SSH] Polling command: dmesg | grep \"Button\|PTIN\|ptin_hotplug_state\"\033[00m")
        while not sh.timeout:
            stdin, stdout, stderr = client.exec_command("dmesg | grep \"Button\|PTIN\|ptin_hotplug_state\"")

            # Get first line
            tag = ""
            for line in stdout:
                tag = line
                break
            # If valid break
            if "Button" in tag:
                break

            sleep(0.5)  # Wait between iterations

        print("\033[96m[SSH] Got a feedback from a button\033[00m")

        # Proccess
        sh.feedback = ""
        for line in stdout:
            sh.feedback += line

        print("\033[96m[SSH] Closing connection to gateway...\033[00m")
        client.close()
        print("\033[96m[SSH] Connection closed\033[00m")

        # Alert the API that the feedback is ready
        sh.sem_feedback_ready.release()
