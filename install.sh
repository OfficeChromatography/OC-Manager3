# #!/bin/bash
echo 'Welcome to OC-MANAGER installation'
echo 'Please Insert your password:'

sudo apt-get update && sudo apt-get upgrade

# Install docker
sudo curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo docker version

# Install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create the desktop executable file
python3 create_desktop_launcher.py $(cd "$(dirname "$0")" && pwd)
