import os

import Pyro4
from dotenv import load_dotenv
load_dotenv()

daemon = Pyro4.Proxy('PYRONAME:lgsmcp.daemon')
daemon._pyroHmacKey = os.getenv("DAEMON_HMAC")

# The daemon expects three parameters: linux_username, server_name and command
def daemonGet(gameserver, command):
    return daemon.lgsmCommand(gameserver.linux_username, gameserver.lgsm_servername, "details")
