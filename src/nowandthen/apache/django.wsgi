import os
import sys
import site

site.addsitedir('/home/roger/.virtualenvs/nowandthen/lib/python2.6/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'nowandthen.settings'

sys.path.append('/home/roger/.virtualenvs/nowandthen')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
