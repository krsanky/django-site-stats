from datetime import datetime

from site_stats.models import Visitor, BrowserString, RequestMethod, StatusCode, Visit #ParseEvent

log_file = "/var/log/lighttpd/access.log"
line1 = '127.0.0.1 abc.oldcode.org - [26/Jan/2011:12:23:28 -0500] "GET /favicon.ico HTTP/1.1" 404 345 "-" "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100723 Firefox/3.6.8"'

def parse_log_line(line):
    """
127.0.0.1 abc.oldcode.org - [26/Jan/2011:12:23:28 -0500] "GET /favicon.ico HTTP/1.1" 404 345 "-" "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100723 Firefox/3.6.8"

127.0.0.1 abc.oldcode.org -
[26/Jan/2011:12:23:28 -0500]
"GET /favicon.ico HTTP/1.1"
404 345 "-"
"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100723 Firefox/3.6.8"

split out the logging for the seperate vhosts ??????????????????????
... /var/www/vhost/oldcode.org/oldcode//var/www/vhost/oldcode.org/oldcode/log/lighttpd_access.log

for now we can just parse it all.
    """

    # SITE and VISITOR
    [vis_n_site, rest] = line.split('-',1)
    #print "[%s]" % (vis_n_site,)
    vis, site = vis_n_site.strip().split(' ',1)
    #print "vis[%s] site[%s]" % (vis, site)

    #print rest
    #[26/Jan/2011:12:23:28 -0500] "GET /favicon.ico HTTP/1.1" 404 345 "-" "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100723 Firefox/3.6.8"

    # DATETIME ignores the -0500
    dt = rest[rest.find('['):rest.find(']')]
    #datetime.strptime('[1/Jun/2005:21:33:12', '[%d/%b/%Y %H:%M:%S')
    dt = dt.split(' ',1)[0]
    #'[26/Jan/2011:12:23:28'
    dt = datetime.strptime(dt, '[%d/%b/%Y:%H:%M:%S')

    # METHOD PATH and CODE
    rest = rest[rest.find('"',1)+1:]
    mpc = rest.split(' ')
    #['GET', '/favicon.ico', 'HTTP/1.1"', '404', '345',
    method = mpc[0]
    path = mpc[1]
    code = mpc[3]

    #BROWSER STRING
    rest = rest.rstrip('" \n')
    #print rest
    #print "----- %s" % (rest.rfind('"'),)
    br_str = rest[rest.rfind('"')+1:]

    return {'site': site,
            'datetime': dt,
            'path': path,
            'visitor': vis,
            'method': method,
            'code': code,
            'browser_string': br_str,
            }


def main():
    """
    this is the 'main'
    """

    with open(log_file, 'r') as f:
        for line in f:
            #print line[:20]
            data = parse_log_line(line)
            #print data
            visit = Visit()

            for f in ('datetime', 'path', 'site'):
                setattr(visit, f, data[f])

            visit.visitor, _ = Visitor.objects.get_or_create(pk=data['visitor'])
            #visit.visitor.save()
            visit.method, _ = RequestMethod.objects.get_or_create(pk=data['method'])
            visit.code, _ = StatusCode.objects.get_or_create(pk=data['code'])
            visit.browser_string, _ = BrowserString.objects.get_or_create(pk=data['browser_string'])

            visit.save()



#file.seek(offset)
#file.tell()

