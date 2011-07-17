#!/bin/bash
workon nowandthen
cd /usr/local/src/nowandthen
git pull
pip install -r requirements/project.txt
python manage.py migrate fusion
python manage.py collectstatic -i cache
sudo /etc/init.d/apache2 reload
