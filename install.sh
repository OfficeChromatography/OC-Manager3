# #!/bin/bash
echo 'Welcome to OC-MANAGER installation'
echo 'Please Insert your password:'

sudo apt-get update && sudo apt-get upgrade

# Install docker
sudo curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo docker version

# Install docker-compose
sudo apt-get install -y libffi-dev libssl-dev
sudo apt-get install -y python3 python3-pip
sudo apt-get remove python-configparser

sudo pip3 install docker-compose

# Create the desktop executable file
python3 create_desktop_launcher.py $(cd "$(dirname "$0")" && pwd)
