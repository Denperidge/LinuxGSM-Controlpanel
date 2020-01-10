import os

import Pyro4
from dotenv import load_dotenv
load_dotenv()

daemon = Pyro4.Proxy('PYRONAME:lgsmcp.daemon')
daemon._pyroHmacKey = os.getenv("DAEMON_HMAC")

# The daemon expects two parameters: str(linux_username) and [command]
def lgsmCommand(gameserver, command):
    user = gameserver.linux_username
    server = gameserver.lgsm_servername
    command = ["/home/" + user + "/" + server, command]
    return daemon.runAsUser(user, command)