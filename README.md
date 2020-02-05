# LGSM_CP

A simple proof of concept control panel for LGSM. The goal of the project is to allow people - if I've given them access - to turn any LGSM gameserver on or off, without allowing them to fully SSH into my server.

## Installation

- Simply clone the repository (or download the zip) and run ```./install.sh```. Fill in the prompts and the installation is done!
- Run the server using start.py (example usage: ```nohup python3 start.py```)
- Configuration: add servers from ip:8000/admin

    ![Screenshot of admin login page](/screenshots/adminlogin.png)

    ![Screenshot of admin index landing page](/screenshots/adminindex.png)

    ![Screenshot](/screenshots/adminadd.png)

- Usage: login from ip:8000 using linux_username/lgsm_servername and the password configured from ip:8000/admin. Start, stop or restart your server using the buttons!

    (For security reasons, if a server is not configured on the admin page, it can't be logged into from the control panel)

    ![Screenshot of server login page](/screenshots/serverlogin.png)

    ![Screenshot of server index landing page](/screenshots/serverindex.png)
    
    ![Screenshot of output from starting a server](/screenshots/serverstart.png)


## Future plans

I have no current plans of expanding on this program. Although a full GUI complete with installation, proper async commands etc. would be interesting to see, it would require a lot of development time and resources that do not outweigh how non-essential it is (seeing that to use LGSM in the first place, you have to be at least a *bit* handy with Linux).
