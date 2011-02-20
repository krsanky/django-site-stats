from datetime import datetime

from django.conf import settings

from logger import log

from site_stats.models import VisitorIP, BrowserString, RequestMethod, StatusCode, Visit
from site_stats.models import ParseEvent

#log_file = settings.SITE_STATS_LOG_FILE
log_file = '/var/www/vhost/abc.oldcode.org/oldcode/tmp/all.log'

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


def parse(filename):
    'Return tuple of dictionaries containing file data.'
    def make_entry(x):
        return {
            'server_ip':x.group('ip'),
            'uri':x.group('uri'),
            'time':x.group('time'),
            'status_code':x.group('status_code'),
            'referral':x.group('referral'),
            'agent':x.group('agent'),
            }
    log_re = '(?P<ip>[.\d]+) - - \[(?P<time>.*?)\] "GET (?P<uri>.*?) HTTP/1.\d" (?P<status_code>\d+) \d+ "(?P<referral>.*?)" "(?P<agent>.*?)"'
    search = re.compile(log_re).search
    matches = (search(line) for line in file(filename))
    return (make_entry(x) for x in matches if x)



    """
    #log.debug(line)

    # SITE and VISITOR (VISITOR means ip-address)
    [vis_n_site, rest] = line.split('-',1)
    log.debug("v_n_s:[%s]" % vis_n_site,)
    try:
        vis, site = vis_n_site.strip().split(' ',1)
    except ValueError as e:
        log.debug("%s" % e,)
        site = ''
        vis = vis_n_site.strip()
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
            'ip': vis,
            'method': method,
            'code': code,
            'browser_string': br_str,
            }


def parse():
    """
    """
    try:
        last_pe = ParseEvent.objects.latest()
    except Exception as e:
        last_pe = ParseEvent()
        #pe.last_position = 0
        last_pe.first_line = 'first_linefirst_linefirst_linefirst_linefirst_linefirst_linefirst_linefirst_line'
        #pe.save()



    file_tell = 0
    f = open(log_file, 'r')
    first_line = f.readline()[:256]
    if first_line == last_pe.first_line:
        log.debug("MATCH skip ahead ... %s" % last_pe.last_position,)
        f.seek(last_pe.last_position)
    else:
        f.seek(0)

    file_tell = f.tell() #???
    for line in f:
        file_tell = f.tell()

        #print "tell:%s" % file_tell,
        data = parse_log_line(line)
        #print data
        visit = Visit()

        #for fld in ('datetime', 'path', 'site'):
        #    setattr(visit, fld, data[fld])
        visit.datetime = data['datetime']
        visit.path = data['path'][:256]
        visit.site = data['site'][:256]

        visit.ip, _ = VisitorIP.objects.get_or_create(pk=data['ip'])
        visit.method, _ = RequestMethod.objects.get_or_create(pk=data['method'])
        visit.code, _ = StatusCode.objects.get_or_create(pk=data['code'])
        visit.browser_string, _ = BrowserString.objects.get_or_create(string=data['browser_string'][:256])

        visit.save()

    f.close()

    pe = ParseEvent()
    pe.last_position = file_tell
    pe.first_line = first_line[:256]
    pe.save()


