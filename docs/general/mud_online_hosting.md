**This guide requires that  you use Windows Subsystem for Linux. I make no attempt to account for deviation from the steps I have taken while writing this guide.**

**Please use this [Evennia referral link](https://m.do.co/c/8f64fec2670c) when signing up for a new Digital Ocean account to get free credit, good for the first 60 days of hosting.** 

Following this link helps out production of Evennia by providing referral credit toward hosting the [Evennia Demo](https://demo.evennia.com/) server. This link grants new accounts free bonus credit. The credit amount changes at times, but it is generally anywhere from $25 to $100 for the first 60 days.

### Table of Contents
* [TLDR Setup Guide](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#tldr-setup-guide)
* [Introduction](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#introduction)
* [Windows Subsystem for Linux](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#windows-subsystem-for-linux)
    * [WSL Quick Reference](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#wsl-quick-reference)
* [Setting Up Ubuntu](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#setting-up-ubuntu)
* [Creating a Digital Ocean Droplet](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#creating-a-digital-ocean-droplet)
* [Logging into the Droplet](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#logging-into-the-droplet)
* [SSH Setup](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#ssh-setup)
* [Disabling Password Authentication](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#disabling-password-authentication)
* [Creating a New User](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#creating-a-new-user)
* [Setting Up Evennia](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#setting-up-evennia)

### TLDR Setup Guide
1) Install [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) with Ubuntu 20.04. This is used to login to the Droplet.
2) Run `sudo apt update && sudo apt upgrade` on the new Linux install. Run it again on the new Droplet once connected.
3) Create a [Digital Ocean](https://www.digitalocean.com/) account, create a new [Project](https://www.digitalocean.com/docs/projects/quickstart/), and setup a new [Droplet](https://www.digitalocean.com/docs/droplets/quickstart/) with **password authentication**.
4) Setup [SSH](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-20-04) on the new Droplet. Be certain to [disable password authentication](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-20-04#step-4-%E2%80%94-disabling-password-authentication-on-your-server) once SSH is functioning.
5) Add a new [sudo-enabled user](https://www.digitalocean.com/community/tutorials/how-to-create-a-new-sudo-enabled-user-on-ubuntu-20-04-quickstart). Enable [SSH access](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04#step-5-%E2%80%94-enabling-external-access-for-your-regular-user) for this new sudo-enabled user.
6) Follow Evennia's [Getting Started](https://github.com/evennia/evennia/wiki/Getting-Started#linux-install) instructions for Linux and clone your project folder from GitHub, rather than using `evennia --init mygame`.

***
### Introduction
* [Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#table-of-contents)

This tutorial is geared toward those using Windows 10. It can still be used as a reference for Linux users. 

Online hosting covered in this tutorial is presented via **[Digital Ocean](https://www.digitalocean.com/)**, but [Linode](https://www.linode.com/) is pretty much exactly the same. Both options are paid hosting and will cost roughly $5 USD a month. There is a free option through Amazon Web Services (AWS), but it is generally more complex and it is not covered in this tutorial.

You can find a list of recommended hosting options [here](https://github.com/evennia/evennia/wiki/Online-Setup#hosting-options) in the Evennia documentation.

Another important thing to keep in mind is that Long-term Support versions of Linux will not always support the latest version of Python. Be certain to check the highest version of Python supported on the Linux distribution that you are planning to use and compare it with the Python version you wish to use for Evennia.

***
### Windows Subsystem for Linux
* [Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#table-of-contents)
* [Microsft - WSL Installation Guide](https://docs.microsoft.com/en-us/windows/wsl/install-win10)

The first thing that needs doing is the setting up of Windows Subsystem for Linux. This will be the method used to connect to the remote server that hosts the game.

**All steps within the WSL installation section must be executed via the Windows PowerShell, ran as administrator.**

> **TIP:** The Windows PowerShell can be opened by bringing up the [Windows start menu](https://i.imgur.com/yTeHBnX.png) and typing `powershell` and it can also be pinned to the [taskbar](https://i.imgur.com/iBgASIc.png).

#### WSL Quick Reference

1) Enable the WSL feature.
    * `dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart`
2) Meet the [requirements for WSL 2](https://docs.microsoft.com/en-us/windows/wsl/install-win10#requirements).
3) Enable the Virtual Machine Platform feature.
    * `dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart`
4) Restart the computer.
5) [Download](https://docs.microsoft.com/en-us/windows/wsl/install-win10#step-4---download-the-linux-kernel-update-package) and install the WSL update to get WSL 2.
6) Set WSL 2 as the default version.
    * `wsl --set-default-version 2`
7) Install the Linux distribution.
    * [Check here](https://docs.microsoft.com/en-us/windows/wsl/install-win10#step-6---install-your-linux-distribution-of-choice) for the currently supported versions. They can either be installed via searching the Microsoft Store or by opening the store link directly from the listed options. This tutorial will cover the installation of the most recent Long Term Support version of Ubuntu ([20.04](https://www.microsoft.com/store/apps/9n6svws3rx71)).

![Ubuntu 20.04 LTS Microsoft Store](https://i.imgur.com/YhSVNs5.png)

Once Ubuntu is installed, it can be found in the start menu under the `All apps` menu. Right-click on the listing to open additional options. It can be pinned to the start menu or the taskbar.

![Ubuntu 20.04 LTS Start Menu Listing](https://i.imgur.com/wphpaLi.png)

***
### Setting Up Ubuntu
* [Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#table-of-contents)

Opening up Ubuntu will launch a command prompt. It will take a moment to install and then begin the new user creation process.

![Ubuntu First Step Username](https://i.imgur.com/L9LZxbA.png)

After creating a new username and password, Ubuntu is ready to receive commands.

![Ubuntu Ready to Begin](https://i.imgur.com/3MnFwDe.png)

The first command that should be executed in any new Ubuntu distribution is `sudo apt update && sudo apt upgrade`. This command will first find and download all of the most up-to-date information on packages installed in the distribution and then upgrade the packages based on this updated information.

> **TIP:** Right-clicking on the Ubuntu command prompt window will paste text directly to the prompt.

Now that the Ubuntu distro is fully up-to-date, it is ready for use with SSH. The next step is to get a server up and running on Digital Ocean in order to SSH into. It doesn't hurt to leave the Ubuntu window open in the background.

***
### Creating a Digital Ocean Droplet
* [Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#table-of-contents)
* [Digital Ocean - Droplet Quickstart Guide](https://www.digitalocean.com/docs/droplets/quickstart/)

Login to your Digital Ocean account and click the `+ New Project` option in the menu on the left side of the screen.

![Digital Ocean New Project](https://i.imgur.com/w3iV3Zw.png)

In the next step `Move resources into Tutorial`, select `Skip for now` at the bottom.

A new project has been created and is ready for a new Droplet to be added. The Droplet is the server itself.

![Digital Ocean Project Landing Page](https://i.imgur.com/cOWD9E4.png)

Click the option to `Get Started with a Droplet`.

The first section of the Droplet page should default to the most basic options, which is fine for hosting a MUD.

![Digital Ocean Droplet Creation Options 1](https://i.imgur.com/kc1BEJS.png)

In the next section, the defaults are also acceptable. Change the region the Droplet is hosted in based on the needs of the project.

![Digital Ocean Droplet Creation Options 2](https://i.imgur.com/1NrmBkS.png)

In the Authentication section, **DO NOT ADD THE SSH KEY HERE!!** It will break the entire process. The SSH key will be created later. Add a password for the Ubuntu distro and give the Droplet a hostname.

![Digital Ocean Droplet Creation Options 3](https://i.imgur.com/Qu4K1KH.png)

The final section doesn't require anything to be changed. Adding backups will help for long term projects, but for testing purposes, it's not a requirement. Click the `Create Droplet` button.

![Digital Ocean Droplet Creation Options 4](https://i.imgur.com/R57x8nU.png)

If everything went well, the Droplet should be added to the project. It will have a progress bar that shows it is getting setup and then it will finally populate information about the Droplet once it's ready.

![Digital Ocean Droplet Creation Success](https://i.imgur.com/05AoKas.png)

***
### Logging into the Droplet
* [Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#table-of-contents)
* [Digital Ocean - Connect to Droplets](https://www.digitalocean.com/docs/droplets/quickstart/#connect-to-droplets)

Hover over the new IP address of the Droplet and click the `Copy` option. Navigate over to the Ubuntu 20.04 WSL command prompt and enter:

`ssh root@ip-address`

Replace `ip-address` with the copied IP address from the Digital Ocean page. Right-click to paste.

Press `Enter` to execute the command. The console may complain that the authenticity of the host can't be established and ask if it should continue connecting. Enter `Yes`. Now enter the password created during the Droplet setup. If the connection closes suddenly, the password may have been entered incorrectly. Try to connect again and enter the password.

If all went well, Ubuntu will show some welcome information and the console will have a prompt `root@server-name:~#`.

![Droplet Successful Login](https://i.imgur.com/dAacIsS.png)

Now run `sudo apt update && sudo apt upgrade` to upgrade the server's packages.

***
### SSH Setup
* [Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#table-of-contents)
* [Digital Ocean - How to Set Up SSH Keys on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-20-04)

To setup SSH you must be back on the local Windows Subsystem for Linux Ubuntu distribution. Type `exit` to close the connection to the Droplet and return to the local machine.

Type in `ssh-keygen` to begin the key generation process. When prompted for a file to save the key to just press `Enter` to keep the default displayed location. Next, create a passphrase for the key. The key will be generated and a fingerprint is shown.

Next, the SSH ID must be copied to the Droplet server. Use the command `ssh-copy-id root@ip-address` and replace `ip-address` with the Droplet's IP address. It will request the root password of the Droplet, the same password used to login earlier.

If the copy was successful, it will say that 1 key has been added and suggest attempting to login again.

Login to the Droplet using `ssh root@ip-address`, but this time enter the passphrase that was created when the SSH key was generated.

![Droplet Successful SSH Login](https://i.imgur.com/TFtqFZ0.png)

> **TIP:** If Ubuntu requests a system restart, enter the command `sudo reboot`. This will restart the server and return the console to the local machine. SSH back into the server again.

***
### Disabling Password Authentication
* [Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#table-of-contents)
* [Digital Ocean - Disabling Password Authentication On Your Server](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-20-04#step-4-%E2%80%94-disabling-password-authentication-on-your-server)

Now that SSH is working properly, the root password is no longer required to connect to the server.

SSH into the remote server, if not already logged in.

Open up the SSH daemon’s configuration file with the command: `sudo nano /etc/ssh/sshd_config`

Press `CTRL + W` to open a search field and enter `PasswordAuthentication`.

![Nano PasswordAuthentication Search](https://i.imgur.com/0lNu3ry.png)

Press `Enter` to jump to the line containing the search parameter.

If this line is commented out with `#`, make sure to remove the `#`. Change the `yes` to `no`. 

> **TIP:** Navigate to the end of the line by pressing `END` or use `RIGHT ARROW KEY` until the end of line is reached. Use `BACKSPACE` to remove the letters. Type out the changes.

Use `CTRL + X` to close out of the file. 

It will prompt: `Save modified buffer?`

Press `y` to save the changes.

It will then prompt for a file name to save as. Leave it as the default to overwrite the current file and press `Enter`.

Now the SSH service must be restarted for the changes to take effect by entering the command: `sudo systemctl restart ssh`

There shouldn't be any output after entering the command, but instead return directly to a new prompt, waiting for commands.

Before closing out this session, open a second WSL instance. If WSL is saved to the taskbar, simply right click the icon and select the Ubuntu option. This will open a second WSL window.

In this new window, SSH into the server again. Enter the SSH passphrase. It should now result in a root prompt waiting commands.

SSH is now fully functional and password authentication has been disabled. It is safe to exit from any remote sessions.

***
### Creating a New User
* [Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#table-of-contents)
* [Digital Ocean - Create a New Sudo-Enabled User Guide](https://www.digitalocean.com/community/tutorials/how-to-create-a-new-sudo-enabled-user-on-ubuntu-20-04-quickstart)

Ensure you are logged into your Droplet as root user.

Execute the `adduser newusername` command, replacing `newusername` with your desired username.

Create a new password. Optionally fill in the user personal information fields.

Add this new user to the sudo group, to allow for root privileges, by executing the command: `usermod -aG sudo username`

Execute the `su - username` command to switch to the new user.

Test the privileges of the new user by attempting to list the directory of root, using the command: `sudo ls -la /root`

This will prompt you to enter the new user's password you just created.

If all went well, you should see a listing of the `/root/` directory.

![Testing New User Permissions](https://i.imgur.com/FcZvUpz.png)

***
* [Digital Ocean - Enabling SSH Keys For Regular Users](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04#step-5-%E2%80%94-enabling-external-access-for-your-regular-user)

Now it's time to add the public SSH key to the new user's profile, to allow them to also SSH in using the keys generated earlier.

If you are still using the Droplet as your new user, execute `su - root` to swap back to the root user.

Execute the command `rsync --archive --chown=username:username ~/.ssh /home/username` and replace the `username` bits with the new user you want to copy the SSH key to.

![Copying SSH Key to New User](https://i.imgur.com/ljBhVzc.png)

**BEFORE YOU CLOSE THIS SESSION**, right click on your Ubuntu WSL icon and open up a second console window. 

Attempt to ssh in as your new user. `ssh username@your_server_ip`

It will ask you for a passphrase. This is the same passphrase created when the SSH keys were created and the same you used to SSH in as root.

If all went well, you should be able to SSH in as the new user.

***
### Setting Up Evennia
* [Table of Contents](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#table-of-contents)
* [Evennia - Getting Started - Linux Setup](https://github.com/evennia/evennia/wiki/Getting-Started#linux-install)

> At the moment of this tutorial's writing, Evennia has only been reported to work properly with 3.7 or 3.8, but you can check the [Getting Started](https://www.evennia.com/docs/latest/Getting-Started.html) instructions to see if there are any changes. For installation of later Python versions, simply change the 3.8 sections of the following command to 3.9, for example. If you are uncertain or lost, ask the community for help. Elements of the installation process change, whereas documents such as this one may not be updated to reflect those changes.

Connect to the Droplet server with SSH as your regular user, if not already connected. If already connected and logged in as root, use `su - username` to switch to your normal user account. 

Use `sudo apt-get update` just to be certain all package information is up-to-date.

Ubuntu 20.04 is currently using Python 3.8.5, so you must install 3.8 versions.

Install Python using: `sudo apt-get install python3.8 python3-pip python3.8-dev python3-setuptools virtualenv gcc`

After a bit of processing, the console will prompt you to continue by pressing `y` and then all of the packages will install.

![Installing Python Packages](https://i.imgur.com/lz7qAdl.png)

***

> **TIP:** GitHub no longer uses passwords and requires that you setup an authentication token.

Now you must make your mud development main folder.

Execute `mkdir muddev` (You can name it anything, not just muddev) and also then execute `cd muddev` to change your location to that new directory.

![muddev directory creation](https://i.imgur.com/nIIafgz.png)

Now you need to clone the Evennia engine. Execute `git clone https://github.com/evennia/evennia.git` while inside of the muddev directory.

![Cloning the Evennia Engine](https://i.imgur.com/5qPrqdi.png)

***

Before proceeding, you should check your Python version. Execute the command `python3 -V` just to ensure your Python version is OK.

Now you must create a virtual environment to work within. Execute the command: `virtualenv evenv` to make a new virtual environment directory named `evenv`.

![Installing Python3 Virtual Environment](https://i.imgur.com/4ID9m7M.png)

Activate the new virtual environment by executing the command: `source evenv/bin/activate`

![Activating the Virtual Environment](https://i.imgur.com/aDzKE64.png)

Install Evennia into the new virtual environment with the command `pip install -e evennia`

> **TIP:** Evennia was installed in the new virtual environment if all of the text output stays white and no errors are presented. If you get red errors stating that the twisted wheel failed to build, then your Python is missing dependencies. So long as you are on Python 3.8 and followed all of the instructions in this tutorial, this shouldn't be the case.

***

Clone your project into the `/muddev` directory by executing the command: `git clone url`

For example, to clone Hecate into the directory, use `git clone https://github.com/kovitikus/hecate.git`

You can find your project's URL via the main GitHub page under the green `Code` drop-down box.

![Github Project URL](https://i.imgur.com/XkioHCm.png)

Once your project is cloned into the `/muddev` directory, you can execute the `ls` command to verify that the 3 sub-directories exist. Evennia, the virtual environment, and your project folder.

![Cloned Project Directory](https://i.imgur.com/A7qiTpi.png)

Be aware, this project will come without a database. If you need to preserve an old database and add it to this new server, you must [transfer the `evennia.db3` database file manually](https://github.com/kovitikus/hecate/blob/master/docs/general/mud_online_hosting.md#transferring-an-existing-database). It is located in `project-directory/server`.

You must also use the same `secret_settings.py` file located in `project-directory/server/conf`. The secret settings file contains a secret key that validates already registered users' existing sessions.

> **TIP:** Neither of these files should -ever- be uploaded to Github, for security reasons. Files ignored by git are specified within the project directory inside `.gitignore`.

If you are OK with starting with a fresh database, navigate to your project's directory and use the command `evennia migrate`

> **WARNING!**
> Some users have reported that the migration step fails. If this happens, it is likely you are attempting to create a new empty Evennia project. You must follow the normal Evennia [Getting Started](https://www.evennia.com/docs/latest/Getting-Started.html#linux-install) instructions to generate a new project. `evennia migrate` will only work after the initial `evennia --init newgamefolder`.

After some output, your new database file will be generated. But your secret_settings.py file will still be missing. To fix that, run `evennia --initmissing`

![Evennia Generate Missing Secret Settings File](https://i.imgur.com/m1xIN5j.png)

Execute the command: `evennia start` to turn the Evennia server on.

Evennia will ask you to create your superuser and then the portal and server will start.

![Evennia First Start](https://i.imgur.com/AFuQtB9.png)

Open your web browser and navigate to the server address, port 4001. For example: `999.999.99.99:4001`

![Evennia Server Web Page](https://i.imgur.com/LjSMHyp.png)

Click the `Online Client` link and you should now be able to connect and login to your server!

![Evennia Web Client Connect](https://i.imgur.com/H7FhW65.png)

***
### Transferring an Existing Database

To transfer your `evennia.db3` and `secret_settings.py` files to your new remote server from your Windows machine, you must re-enable password authentication logins on the remote server. Do so by opening `sudo nano /etc/ssh/sshd_config` on your remote server as `root` user and changing the `PasswordAuthentication` line back to yes. Restart the SSH service `sudo systemctl restart ssh`. Make sure you remember to reverse this once you've finished copying over your files!

Open up a new Windows PowerShell session by navigating to the Windows menu and typing in `powershell`.

![Windows PowerShell Launch](https://i.imgur.com/gPkopU4.png)

Within PowerShell navigate to your project's server directory.

![PowerShell Directory Navigation](https://i.imgur.com/v9soVjk.png)

You will now use secure copy to transfer the database file over to your server.

`scp evennia.db3 username@server-address:~/muddev/project/server`

![PowerShell Database File Secure Copy](https://i.imgur.com/v92js4O.png)

Check your remote server's directory to see that the database copied over properly.

![Secure Copy Database Confirmation](https://i.imgur.com/VqLZshC.png)

You can now do the same for the `secret_settings.py` file by navigating into the `conf` directory within PowerShell.

![Secure Copy Secret Settings File](https://i.imgur.com/zblwvNk.png)

![Secure Copy Secret Settings Confirmation](https://i.imgur.com/S1nPMp3.png)

***

This concludes the tutorial. Thanks for reading and good luck!
