import paramiko
import paramiko.hostkeys
import os

s = paramiko.hostkeys.HostKeys
w = s.load(s, os.path.expanduser("~/.ssh/known_hosts"))

print(w)