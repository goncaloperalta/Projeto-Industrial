import paramiko
import shared_memory as sh
import credentials

def SSHConnect():
    while True:
        sh.sem_api.acquire()

        # Connect
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('192.168.1.1', username=credentials.host, password=credentials.passw)

        sh.sem_SSH_ready.release()

        # Exec
        # dmesg | grep "Button \|PTIN\|ptin_hotplug_state"
        stdin, stdout, stderr = client.exec_command("dmesg | grep \"Button\|PTIN\|ptin_hotplug_state\"")

        # Proccess
        for line in stdout:
            print(line.strip())

        client.close()
