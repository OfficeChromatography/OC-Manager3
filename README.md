# OC-Lab-2.0
## Install
The installation process is really simple. You just need to follow the next steps.

### 0. Install git
Before we begin with the installation, we need to install git.
```bash
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install git
```

### 1. Clone the git repository
The simplest way to clone a git repository is opening a Terminal (`Ctrl+t`), then go to the directory where you would like to have the folder that contains all the configuration files of your OC-LAB **(and between those, it is included the OC-Manager files too)**  

E.g.
```bash
cd ~/Desktop
```
Finally, copy and paste the next command and press enter.

```bash
git clone https://github.com/lucassing/OC-Lab-2.0.git
```


### 2. Execute 'install.py'
The next step is to execute a bash script which contains, the necessary softwares to run the OC-Manager. If you close the Terminal open it again (remember, `Ctrl+t`). Now go to the folder that contains the OC-Lab files, it is

*cd* follow by the path to the folder.

```bash
cd /path/to/your/OC-files
```
Then execute,
```bash
python install.py
```

this will install:
```
docker
docker-compose
```
If everything was correctly execute, you should see a shortcut of OC-Manager in your Desktop.
Now OC-Manager it's installed in your device.

### 3.Execute OC-Manager

In case of using OC-LAB, before you execute the OC-Manager, be sure that it is connected to your device (PC, MAC, raspi, etc.)
Double click in your Desktop shortcut.
