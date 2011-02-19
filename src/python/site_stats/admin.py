from django.contrib import admin

#from urt_server.models import Server
#class ServerAdmin(admin.ModelAdmin):
#    """
#    list_filter = ('is_region', 'map_display', 'future')
#    """
#    list_display = ('ip', 'port', 'name', 'enabled')
#    list_display_links = ('ip', 'name')
#    list_editable = ('enabled',)
#admin.site.register(Server, ServerAdmin)

from site_stats.models import Visitor
from site_stats.models import BrowserString
from site_stats.models import RequestMethod
from site_stats.models import Visit
from site_stats.models import ParseEvent

admin.site.register(Visitor)
admin.site.register(BrowserString)
admin.site.register(RequestMethod)
admin.site.register(Visit)
admin.site.register(ParseEvent)
