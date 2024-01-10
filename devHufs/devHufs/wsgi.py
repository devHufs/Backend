"""
WSGI config for devHufs project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
#추가
import sys

from django.core.wsgi import get_wsgi_application

#추가
path = os.path.abspath(__file__+'/../..')
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devHufs.settings')

application = get_wsgi_application()
