#!/usr/bin/python3
import subprocess
subprocess.run(["sudo", "docker", "exec", "-ti", "oc_manager_cont", "bash", "-c", "python manage.py makemigrations"], stderr=subprocess.PIPE)
subprocess.run(["sudo", "docker", "exec", "-ti", "oc_manager_cont", "bash", "-c", "python manage.py migrate"], stderr=subprocess.PIPE)
