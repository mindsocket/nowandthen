# pinax.wsgi is configured to live in projects/nowandthen/deploy.

import os
import sys

from os.path import abspath, dirname, join
from site import addsitedir
addsitedir('/home/roger/.virtualenvs/nowandthen/lib/python2.6/site-packages')
sys.path.insert(0, abspath(join(dirname(__file__), "../../")))
sys.path.insert(0, abspath(join(dirname(__file__), "../apps")))

os.environ["DJANGO_SETTINGS_MODULE"] = "nowandthen.settings"

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
