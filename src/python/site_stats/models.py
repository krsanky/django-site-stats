from django.db import models
from django.contrib.sites.models import Site

"""
127.0.0.1 abc.oldcode.org -
[26/Jan/2011:12:23:28 -0500]
"GET /favicon.ico HTTP/1.1"
404 345 "-"
"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100723 Firefox/3.6.8"
"""
class Visitor(models.Model):
    """
    """
    ip = models.IPAddressField(null=True, primary_key=True)
    desc = models.CharField(max_length=256, blank=True)

class BrowserString(models.Model):
    """
    "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100723 Firefox/3.6.8"
    """
    string = models.CharField(max_length=256, primary_key=True)

class RequestMethod(models.Model):
    """
    GET POST ...
    """
    method = models.CharField(max_length=10, primary_key=True)
    desc = models.CharField(max_length=256, blank=True)

class StatusCode(models.Model):
    """
    200 404 ...
    """
    code = models.CharField(max_length=3, primary_key=True)
    desc = models.CharField(max_length=256, blank=True)

class Visit(models.Model):
    """
    """
    #site = models.ForeignKey(Site, null=True)
    site = models.CharField(max_length=256)
    datetime = models.DateTimeField()
    path = models.CharField(max_length=256)
    visitor = models.ForeignKey(Visitor) #add if needed
    method = models.ForeignKey(RequestMethod) #add if needed
    code = models.ForeignKey(StatusCode) #add if needed
    browser_string = models.ForeignKey(BrowserString) #add if needed

class ParseEvent(models.Model):
    """
    that with first_line will let us only read new log entries on every parse
    """
    datetime = models.DateTimeField(auto_now_add=True)

    #1st line of file, to use as a file-id
    first_line = models.CharField(max_length=256)

    #the number of bytes parsed from the beginning ... from file.tell()
    last_position = models.IntegerField()
