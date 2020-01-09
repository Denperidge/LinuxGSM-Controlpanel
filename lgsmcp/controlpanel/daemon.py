import os

import Pyro4
from dotenv import load_dotenv
load_dotenv()

daemon = Pyro4.Proxy('PYRONAME:lgsmcp.daemon')
daemon._pyroHmacKey = os.getenv("DAEMON_HMAC")

def getServer(command):
    return daemon.connect("details")