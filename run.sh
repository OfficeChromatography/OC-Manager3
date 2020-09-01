#!/bin/bash
DIRECTORY=`dirname $0`
echo $DIRECTORY
cd $DIRECTORY
# sudo docker rmi oc-image:octag -f
sudo docker-compose down
sudo docker-compose run app sh -c "python -m pip install opencv-python"
sudo docker-compose run app sh -c "python manage.py makemigrations"
sudo docker-compose run app sh -c "python manage.py migrate --run-syncdb"
sudo docker-compose up
