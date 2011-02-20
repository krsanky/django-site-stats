from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group

from logger import log

from site_stats.models import VisitorIP

def admin_group(user):
    grp = Group.objects.get(name='admin')
    if grp in user.groups.all():
        return True
    else:
        return False

#@login_required
@user_passes_test(admin_group)
def index(request):
    """
    """
    ips = VisitorIP.objects.all()
    ctx = RequestContext(request,{'ips': ips, 'gmap_key': settings.GMAP_KEY})
    return render_to_response('site_stats/index.html', context_instance=ctx)

def map(request):
    """
    google map with visitor ips marked
    """
    ips = VisitorIP.objects.all()
    ctx = RequestContext(request,{'ips': ips, 'gmap_key': settings.GMAP_KEY})
    return render_to_response('site_stats/map.html', context_instance=ctx)

