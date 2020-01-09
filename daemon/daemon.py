import Pyro4
import os
import subprocess

from dotenv import load_dotenv
load_dotenv()

os.environ["PYRO_HMAC_KEY"] = os.getenv("DAEMON_HMAC")

subprocess.Popen(["py", "-3", "-m", "Pyro4.naming"])

print(os.getenv("DAEMON_HMAC"))

currentDir = os.path.abspath(__file__).replace(os.path.basename(__file__), "")


@Pyro4.expose
class LgsmcpDaemon(object):
    def connect(self, name):
        return 'Connected to {0}'.format(name)

daemon = Pyro4.Daemon()
daemon._pyroHmacKey = os.getenv("DAEMON_HMAC")

uri = daemon.register(LgsmcpDaemon)

nameserver = Pyro4.locateNS(hmac_key=os.getenv("DAEMON_HMAC"))
nameserver.register("lgsmcp.daemon", uri)


daemon.requestLoop()
