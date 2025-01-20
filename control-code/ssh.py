import re
import logging
import paramiko
import credentials
from os import system
from time import sleep
import shared_memory as sh

paramiko.util.log_to_file("app.log", level="WARN")
logger = logging.getLogger("SSH")

arr = ['RESET', 'WPS', 'INFO/WIFI']

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

def errorHandler(err):
    logger.error(err)
    with sh.access:
        sh.ERROR = err
        sh.modulesData['button'] = 'No Feedback'
        sh.modulesData['success'] = 0
        sh.modulesData['force_val'] = [0]
        sh.modulesData['time_val'] = [0]
        
        sh.feedbackReady.release()
        sh.sensorReadingsReady.release()

def SSHConnect():
    while True:
        # SSH Loop
        # 1 - Wait to Start
        # 2 - Connect to the DUT
        # 3 - Start the sensor and the control signal modules
        # 4 - Wait for the actuator to press something
        # 5 - Execute the command to read the feedback
        # 6 - Store the results on the shared dictionary
        # 7 - Resume the state module
        # Repeat
 
        sh.startSSH.acquire()

        # Connect
        print("\033[96m[SSH] Connecting to gateway...\033[00m")
        logger.info("Atempting connection to SSH server")
        system("ssh-keygen -f \"/home/rpi400/.ssh/known_hosts\" -R \"192.168.1.1\"")
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect("192.168.1.1", username=credentials.host, password=credentials.passw)
        except (paramiko.BadHostKeyException, paramiko.AuthenticationException, paramiko.SSHException):
            errorHandler("Couldn't connect to DUT via SSH")
            continue
        
        print("\033[96m[SSH] Connected to gateway\033[00m")
        logger.info("Connection to DUT established")

        # Get initial counters
        stdin, stdout, stderr = client.exec_command("/3party/ptinBoardDiagXSR150DX 0")
        output = stdout.readlines()
        print(output)
        initialCounters = processCommand(output)
        print(initialCounters)

        # Exec
        buttonPressed = -1
        
        # Alert the sensor_reader and the control_signal that the SSH connection has been established
        sh.startSensorAndControl.release(2)

        # Wait for a press
        sh.buttonPressed.acquire()

        with sh.access:
            sleep(0.1)
            stdin, stdout, stderr = client.exec_command("/3party/ptinBoardDiagXSR150DX 0")
            output = stdout.readlines()
            print(output)
            counters = processCommand(output)
            print(counters)
            buttonPressed = getButtonPressed(initialCounters, counters)
            print(buttonPressed)
            if buttonPressed != -1:
                print("\033[96m[SSH] Got a feedback from a button: " + arr[buttonPressed] + "\033[00m")
                logger.info(f"Got a feedback from button: {arr[buttonPressed]}")
                sh.modulesData['button'] = arr[buttonPressed]
                sh.modulesData['success'] = 1
            else:
                print("\033[96m[SSH] Could not get a feedback from any button\033[00m")
                logger.warning("Could not get a feedback from any button")
                sh.modulesData['button'] = 'No Feedback'
                sh.modulesData['success'] = 0
            stdin.close()
            stdout.close()
            stderr.close()
            client.close()

        print("\033[96m[SSH] Connection closed\033[00m")
        logger.info("Closed SSH connection to the DUT")
        
        # Feedback is ready
        sh.feedbackReady.release()
