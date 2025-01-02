import re
import logging
import paramiko
import threading
import credentials
import shared_memory as sh

paramiko.util.log_to_file("app.log", level="WARN")
logger = logging.getLogger(__name__)

def processCommand(cmd):
    counters = []
    for button in cmd[1:]:
        regex = re.search(r":(\d+)", button)
        counters.append(int(regex.group(1)))

    return counters

def getButtonPressed(initial, changed):
    for i in range(len(initial)):
        if initial[i] != changed[i]:
            return i

    return -1

def breakLoop():
    sh.timeout = 1

def SSHConnect():
    while True:
        sh.startSSH.acquire()

        # Connect
        print("\033[96m[SSH] Connecting to gateway...\033[00m")
        logger.info("Atempting connection to SSH server")
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect("192.168.1.1", username=credentials.host, password=credentials.passw)
        print("\033[96m[SSH] Connected to gateway\033[00m")
        logger.info("Connection to DUT established")
        client.exec_command("dmesg -c") # Clear the ring

        # Get initial counters
        stdin, stdout, stderr = client.exec_command("/3party/ptinBoardDiagXSR150DX 0")
        output = stdout.readlines()
        initialCounters = processCommand(output)

        # Exec
        success = 0
        buttonPressed = -1
        sh.timeout = 0
        threading.Timer(5, breakLoop).start()
        print("\033[96m[SSH] Polling command: /3party/ptinBoardDiagXSR150DX 0\033[00m")
        logger.info("Polling command: /3party/ptinBoardDiagXSR150DX 0")
        
        # Alert the sensor_reader and the control_signal that the SSH connection has been established
        sh.startSensorAndControl.release(2)

        while True:
            stdin, stdout, stderr = client.exec_command("/3party/ptinBoardDiagXSR150DX 0")
            output = stdout.readlines()
            counters = processCommand(output)

            buttonPressed = getButtonPressed(initialCounters, counters)
            if buttonPressed != -1:
                success = 1
                break
            
            if sh.timeout == 1:
                sh.timeout = 0
                break

        # Close Connection
        stdin.close()
        stdout.close()
        stderr.close()
        client.close()
        print("\033[96m[SSH] Connection closed\033[00m")
        logger.info("Connection to the DUT closed")

        arr = ['RESET', 'WPS', 'INFO/WIFI']
        if success:
            print("\033[96m[SSH] Got a feedback from a button: " + arr[buttonPressed] + "\033[00m")
            logger.info(f"Got a feedback from button: {arr[buttonPressed]}")
            sh.feedback = {
                'button': arr[buttonPressed],
                'success': success
            }
        else:
            print("\033[96m[SSH] Could not get a feedback from any button\033[00m")
            logger.info("Could not get a feedback from any button: timed out")
            sh.feedback = {
                'button': 'None',
                'success': success
            }
        
        # Alert the API, control and sensor that the feedback is ready
        sh.feedbackReady.release(3)
