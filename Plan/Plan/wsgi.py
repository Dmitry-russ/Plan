"""
WSGI config for Plan project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
from os.path import abspath, join

for root, _, files in os.walk('/usr/local/lib/python3.4/site-packages/django'):
    for f in files:
        os.system('dos2unix %s' % abspath(join(root, f)))
