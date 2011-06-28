#!/bin/bash
workon nowandthen
cd /usr/local/src/nowandthen
git pull
python manage.py migrate fusion
python manage.py collectstatic -i cache
