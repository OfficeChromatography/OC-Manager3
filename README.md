# OC-Manager 3.0
## Install
The installation process is really simple. 

OC-Manager 3.0 works fine on a 'Raspberry Pi 4' with 4Gb RAM memory and [Ubuntu 20.04](https://releases.ubuntu-mate.org/20.04/arm64/) installed on it.  
During and after the development phase, we used Ubuntu 20.04 LTS, for which security 
updates are available until April 2025. The long-term service (LTS) can be extended by 
5 years after registering at [Ubuntu](https://ubuntu.com/security/esm) and is free 
for personal use on three machines.

Newer releases of Ubuntu unfortunately do not support the raspistill command to capture plate images.

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
git clone https://github.com/OfficeChromatography/OC-Manager3.git
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

### 3.Before the first execution 

#### With Raspberry Pi
Depending on the OS change on the docker_compose.yml file:

For a 64bits OS:

```dockerfile
    image: ocmanager/ocmanager:arm64
```

To activate the camera, follow the corresponding instruction: 

##### [Activate the PiCamera in Ubuntu distributions](https://ubuntu.com/blog/how-to-stream-video-with-raspberry-pi-hq-camera-on-ubuntu-core)
##### [Activate the PiCamera in Raspbian distributions](https://thepihut.com/blogs/raspberry-pi-tutorials/16021420-how-to-install-use-the-raspberry-pi-camera)

#### With Linux-PC (No Pi-Camera, instead uses the pc-webcam)
If you want to run OC-Manager with a PC running a Linux instance, you can download the docker image for it by changing the docker-compose.yml file.

```dockerfile
    image: ocmanager/ocmanager:amd64
``` 

### 4.OC Manager execution 

Navigate to the path where OC-Manager was installed and execute ./run.py file.
```
python3 run.py 
```

OC-Manager supports at the moment only linux/amd64, linux/arm/v7 and linux/arm64 architecutes.

OC-Manager3 was intensively tested with Chromium as browser. Therefore, it is recommended to install this browser:

```
sudo apt install chromium-browser
```

# FIRMWARE
Firmware installation 
[OcLab3Firmware](https://github.com/OfficeChromatography/OCLab3-Hardware)

# Useful guides

[Docker Commands](https://towardsdatascience.com/15-docker-commands-you-should-know-970ea5203421)

[Remove Migrations](https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html)

All commands must be executed inside the docker-compose. To enter to the docker-compose running instance:

In a running container:
```sh
sudo docker-compose exec -ti app bash
```
To initialize and enter the terminal
```sh
sudo docker-compose run -ti app bash
```
