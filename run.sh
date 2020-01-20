#!/bin/bash
sudo docker-compose down
sudo docker-compose run app sh -c "python manage.py makemigrations"
sudo docker-compose run app sh -c "python manage.py migrate"
sudo docker-compose up
