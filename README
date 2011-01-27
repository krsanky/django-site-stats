# django-site-stats

This app parses a webserver access-log file, and adds
the basic visitor data to some models.

Visit Visitor RequestMethod StatusCode and BrowserString.

My initial need is so I can do a google map of site visitors
by their ip address.

This code is initially specific to my sites' architecture, which
uses lighttpd, and logs all access to /var/log/lighttpd/access.log.

The log parse method is pretty brittle and specific to lighttpd's
default log formay.

But ... the code is also pretty obvious, and altering to taste
should be easy enough.


