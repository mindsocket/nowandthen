import os
import sys
import site

site.addsitedir('/home/roger/.virtualenvs/nowandthen/lib/python2.5/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'nowandthen.settings'

sys.path.append('/home/roger/.virtualenvs/nowandthen/nowandthen')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
