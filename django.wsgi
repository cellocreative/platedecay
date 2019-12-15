import os
import sys

path='/var/www/vhosts/softxinnovations.com/httpdocs/backend'

if path not in sys.path:
  sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'dentistry.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
