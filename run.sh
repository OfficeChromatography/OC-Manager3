#!/bin/bash
DIRECTORY=`dirname $0`
echo $DIRECTORY
cd $DIRECTORY
sudo docker rmi oc-image:octag -f
sudo docker-compose down
sudo docker-compose run app sh -c "python manage.py makemigrations"
sudo docker-compose run app sh -c "python manage.py migrate"
sudo docker-compose up
