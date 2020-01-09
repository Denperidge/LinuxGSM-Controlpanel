import subprocess
from os import system
from os import path

currentDir = path.abspath(__file__).replace(path.basename(__file__), "")
try: 

    server = subprocess.Popen(["python3", currentDir + "/lgsmcp/manage.py", "runserver", "--noreload", "0.0.0.0:8000"])
    daemon = subprocess.Popen(["sudo", "python3", currentDir + "/daemon/daemon.py"])
    daemon.communicate()
except:
    server.kill()
    system("sudo kill " + daemon.pid)
