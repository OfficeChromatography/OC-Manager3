#!/bin/bash
DIRECTORY=`dirname $0`
echo $DIRECTORY
cd $DIRECTORY
# sudo docker rmi oc-image:octag -f
sudo docker-compose down
xdg-open http://127.0.0.1:8000/
sudo docker-compose up

