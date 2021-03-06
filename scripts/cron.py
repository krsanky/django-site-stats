#!/usr/bin/env python

"""
*/45 * * * * /var/www/vhost/oldcode.org/oldcode/apps/django-site-stats/scripts/cron.py > /dev/null 2>&1
"""

import sys, os

my_dir = os.path.dirname(os.path.realpath( __file__ ))
tmp1 = os.path.dirname(os.path.realpath(__file__))
tmp1 = tmp1.split('/')
tmp1.pop()
tmp1.pop()
tmp1.pop()
BASEDIR = '/'.join(tmp1)
#print BASEDIR

os.environ['DJANGO_SETTINGS_MODULE'] = "settings"
os.environ['INTERACTIVE_PYTHON_LOG'] = '%s/py.log' % (my_dir,)

PYTHONPATH = os.path.join(BASEDIR, 'src/python')
sys.path.insert(0, PYTHONPATH)
#print PYTHONPATH

from site_stats.util import parse

parse()
