from django.db import models
from django.contrib.sites.models import Site

from django.contrib.gis.utils import GeoIP

"""
127.0.0.1 abc.oldcode.org -
[26/Jan/2011:12:23:28 -0500]
"GET /favicon.ico HTTP/1.1"
404 345 "-"
"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100723 Firefox/3.6.8"
"""

class VisitorIP(models.Model):
    """
    """
    ip = models.IPAddressField(null=True, primary_key=True)
    desc = models.CharField(max_length=256, blank=True)
    lon = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return "%s" % (self.ip,)

    def lat_lon(self):
        """
        this method returns lat, lon if avail.
        OR it sets lat and lon from GeoIP
        and then returns them
        """
        if self.lat and self.lon:
            return self.lat, self.lon
        else:
            g = GeoIP()
            ret = g.lat_lon(self.ip)
            if ret:
                lat, lon = ret
                self.lat = lat
                self.lon = lon
                self.save()
                return self.lat, self.lon
            else:
                return None

    def lat_lon_str(self):
        """
        wrapper of self.lat_lon(), that returns a single comma seperated string
        to play nice with html templates
        """
        lat, lon = self.lat_lon()
        return "%s, %s" % (lat, lon)

class BrowserString(models.Model):
    """
    "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100723 Firefox/3.6.8"
    """
    string = models.CharField(max_length=256, unique=True)
    def __unicode__(self):
        return "%s" % (self.string,)

class RequestMethod(models.Model):
    """
    GET POST ...
    """
    method = models.CharField(max_length=10, primary_key=True)
    desc = models.CharField(max_length=256, blank=True)
    def __unicode__(self):
        return "%s" % (self.method,)

class StatusCode(models.Model):
    """
    200 404 ...
    """
    code = models.CharField(max_length=3, primary_key=True)
    desc = models.CharField(max_length=256, blank=True)
    def __unicode__(self):
        return "%s" % (self.code,)

class Visit(models.Model):
    """
    """
    #site = models.ForeignKey(Site, null=True)
    site = models.CharField(max_length=256, blank=True)
    datetime = models.DateTimeField()
    path = models.CharField(max_length=256)
    ip = models.ForeignKey(VisitorIP) #add if needed
    method = models.ForeignKey(RequestMethod) #add if needed
    code = models.ForeignKey(StatusCode) #add if needed
    browser_string = models.ForeignKey(BrowserString) #add if needed

    def __unicode__(self):
        return "%s : %s" % (self.ip, self.path)


class ParseEvent(models.Model):
    """
    last_position along with first_line will let us only read new log entries on every parse
    """
    datetime = models.DateTimeField(auto_now_add=True)
    first_line = models.CharField(max_length=256)
    last_position = models.IntegerField() #from <file>.tell()

    class Meta:
        get_latest_by = "datetime"

    def __unicode__(self):
        return "%s: %s" % (self.datetime, self.last_position)
