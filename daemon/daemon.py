import Pyro4
import os
import sys
import pwd
import subprocess

from dotenv import load_dotenv
load_dotenv()

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

# General purpose function: run command as user
# linuxUsername should be str, command list
@Pyro4.expose
class LgsmcpDaemon(object):
    def runAsUser(self, linuxUsername, command):
        output = "Error"

        try:  # Succesful reply returns bytes, and can thus be serialized to string
            output = subprocess.check_output(command, preexec_fn=runAsUser(linuxUsername))
        except subprocess.CalledProcessError as e:
            # Unsuccesful reply returns CalledProcessError, which throws a CalledProcessError
            output = "[" + str(e.returncode) + "] " + str(e.output)
        
        output = str(output)

        print("Returning: " + output)
        return output

        

daemon = Pyro4.Daemon()
daemon._pyroHmacKey = os.getenv("DAEMON_HMAC")

uri = daemon.register(LgsmcpDaemon)

nameserver = Pyro4.locateNS(hmac_key=os.getenv("DAEMON_HMAC"))
nameserver.register("lgsmcp.daemon", uri)


daemon.requestLoop()
