import subprocess
from os import system
from os import path

currentDir = path.abspath(__file__).replace(path.basename(__file__), "")

# Call echo with sudo so that the sudo password won't be asked for the daemon
# (as the input gets muddled and confusing with the server launches)
subprocess.check_output(["sudo", "echo", "\"Starting lgsmcp!\""])

try:
    server = subprocess.Popen(["python3", currentDir + "/lgsmcp/manage.py", "runserver", "--noreload", "0.0.0.0:8000"])
    daemon = subprocess.Popen(["sudo", "python3", currentDir + "/daemon/daemon.py"])
    daemon.communicate()
except:
    server.kill()
    system("sudo kill " + str(daemon.pid))
