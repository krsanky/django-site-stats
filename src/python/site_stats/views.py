from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from logger import log

#@login_required
@user_passes_test(util.urban_terror_group)


#@login_required
## @user_passes_test(util.urban_terror_group)
## def urban_terror_group(user):
##     """
##     """
##     ut_grp = Group.objects.get(name=settings.UT_GROUP)
##     if ut_grp in user.groups.all():
##         return True
##     else:
##         return False



def index(request):
    """
    """
    ctx = RequestContext(request,{})
    return render_to_response('site_stats/index.html', context_instance=ctx)

