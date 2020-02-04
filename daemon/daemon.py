import Pyro4
import os
import sys
import pwd
import subprocess
import re

from dotenv import load_dotenv
load_dotenv()

regexCleanConsoleOutput = r"\\.*?]"

os.environ["PYRO_HMAC_KEY"] = os.getenv("DAEMON_HMAC")

subprocess.Popen(["python3", "-m", "Pyro4.naming"])

def runAsUser(username):
    uid = pwd.getpwnam(username)[2]
    #guid = pwd.getpwnam(username)[3]

    def setUser():
        os.setuid(uid)
        #os.setgid(guid)
        os.chdir("/home/" +username)
        
    return setUser

def cleanConsoleOutput(outputBytes):
    # Convert bytes to string
    rawOutput = str(outputBytes).split("\\n")
    output = []
    for line in rawOutput:
        # If a singular character gets through (or somehow an empty line),
        # check if alphanumeric. If not, don't pass through. 
        if (len(line)) < 2 and not line.isalnum():
            continue

        cleaned_line = re.sub(regexCleanConsoleOutput, "", line, 0).replace("b'", "").strip()
                    
        # LGSM sends a string of what it's doing to the console, clears, and then the same thing with the result.
        # This causes check_output to capture it like this: Starting nmrihserver: Check IP Starting nmrihserver: Check IP: x.x.x.x
        # TODO: fix that

        output.append(cleaned_line)

    return output

# General purpose function: run command as user
# linuxUsername should be str, command list
@Pyro4.expose
class LgsmcpDaemon(object):
    def runAsUser(self, linuxUsername, command):
        output = "Error"

        try:  # Succesful reply returns bytes, and can thus be serialized into a str and to a list
            output = subprocess.check_output(command, preexec_fn=runAsUser(linuxUsername))
            output = cleanConsoleOutput(output)
            
        except subprocess.CalledProcessError as e:
            # Unsuccesful reply returns subprocess.CalledProcessError eventargs, which need some extra steps
            output = ["(" + str(e.returncode) + ")"] + cleanConsoleOutput(e.output)

        # Daemon needs to send str
        output = str(output)

        return output

daemon = Pyro4.Daemon()
daemon._pyroHmacKey = os.getenv("DAEMON_HMAC")

uri = daemon.register(LgsmcpDaemon)

nameserver = Pyro4.locateNS(hmac_key=os.getenv("DAEMON_HMAC"))
nameserver.register("lgsmcp.daemon", uri)


daemon.requestLoop()
