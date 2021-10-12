# OC-Manager 3.0
## Install
The installation process is really simple. 

OC-Manager 3.0 works fine on a 'Raspberry Pi 4' with 4Gb ram memory and Ubuntu 20.04 installed on it.  

### 0. Install git
Before we begin with the installation, we need to install git.
```bash
sudo apt-get update && sudo apt-get -y upgrade
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
git clone https://github.com/ocmanager/oc-manager-v3.git
```

### 2. Execute 'install.py'
The next step is to execute a bash script which contains, the necessary softwares to run the OC-Manager. If you close the Terminal open it again (remember, `Ctrl+t`). Now go to the folder that contains the OC-Lab files, it is

*cd* follow by the path to the folder.

```bash
cd /path/to/your/OC-files
```
Then execute,
```bash
python3 install.py
```

this will install:
```
docker
docker-compose
```
Now OC-Manager it's installed in your device.

### 3.Execute OC-Manager

In case of using OC-LAB, before you execute the OC-Manager, be sure that it is connected to your device (PC, MAC, raspi, etc.)
Navigate to the path where OC-Manager was installed and execute ./run.py file.
```
python3 run.py 
```
# FIRMWARE
Firmware installation 
[OcLab3Firmware](https://github.com/OfficeChromatography/OCLab3-Hardware)
