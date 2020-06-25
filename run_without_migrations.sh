#!/bin/bash
DIRECTORY=`dirname $0`
echo $DIRECTORY
cd $DIRECTORY
# sudo docker rmi oc-image:octag -f
sudo docker-compose down
sudo docker-compose up
