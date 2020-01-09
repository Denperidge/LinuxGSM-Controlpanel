import Pyro4
import os
import pwd
import subprocess

from dotenv import load_dotenv
load_dotenv()

os.environ["PYRO_HMAC_KEY"] = os.getenv("DAEMON_HMAC")

subprocess.Popen(["python3", "-m", "Pyro4.naming"])

@Pyro4.expose
class LgsmcpDaemon(object):
    def lgsmCommand(self, linuxUsername, serverUsername, command):
        return 'Connected to {0} {1} {2}'.format(linuxUsername, serverUsername, command)

daemon = Pyro4.Daemon()
daemon._pyroHmacKey = os.getenv("DAEMON_HMAC")

uri = daemon.register(LgsmcpDaemon)

nameserver = Pyro4.locateNS(hmac_key=os.getenv("DAEMON_HMAC"))
nameserver.register("lgsmcp.daemon", uri)


daemon.requestLoop()
