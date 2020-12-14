from wsgiref.simple_server import make_server
from wsgiref import util
from urllib.parse import urlparse
from wsgiref.util import setup_testing_defaults, request_uri
from datetime import datetime, timezone, timedelta
import pytz 
from tzlocal import get_localzone 
import json

def app(environ, start_response):
    setup_testing_defaults(environ)
 
    request_type = environ['REQUEST_METHOD']
    print(request_type)

    url=urlparse(util.request_uri(environ))
    request_param = url.path.split('/',1)[1]
    print(request_param)

    if (request_type=="GET"):
        
        if (request_param==""):
            time = datetime.now(tz=get_localzone())
        elif (request_param in pytz.all_timezones):
            time = datetime.now(tz=pytz.timezone(request_param))
        else:
            start_response(status = '404 NOT FOUND',headers = [('Content-type', 'application/json; charset=utf-8')])
            return json.dumps({
                "status": 404,
                "message": "tz not found",
            }).encode().splitlines()

        start_response(status = '200 OK',headers = [('Content-type', 'text/html; charset=utf-8')])
        ret = time.strftime('%Y-%m-%d %H:%M:%S').encode().splitlines()
        print(ret)
        return(ret)


    elif (request_type=="POST"):
        cont = read_json(environ)
        start_response(status = '200 OK',headers = [('Content-type', 'application/json; charset=utf-8')])
        
        if (request_param == "api/v1/time"):
            time_zone = pytz.timezone(cont['tz'])
            time = datetime.now(tz=time_zone)
            ret={"tz": time.tzinfo.__str__()}
            ret["time"] = time.strftime('%H:%M:%S')
            return(json.dumps(ret).encode().splitlines())
        
        if (request_param == "api/v1/date"):
            time_zone = pytz.timezone(cont['tz'])
            time = datetime.now(tz=time_zone)
            ret={"tz": time.tzinfo.__str__()}
            ret["date"] = time.strftime('%Y-%m-%d')
            return(json.dumps(ret).encode().splitlines())
        
        if (request_param == "api/v1/datediff"):
            dif=""
            try:
                start = datetime.strptime(cont["start"]["date"], '%m.%d.%Y %H:%M:%S')
            except:
                start = datetime.strptime(cont["start"]["date"], '%H:%M%p %Y-%m-%d')
            try:
                end = datetime.strptime(cont["end"]["date"], '%m.%d.%Y %H:%M:%S')
            except:
                end = datetime.strptime(cont["end"]["date"], '%H:%M%p %Y-%m-%d')

            if ("tz" in cont['start']) & ("tz" in cont['end']):
                start_tz = pytz.timezone(cont['start']['tz'])
                end_tz = pytz.timezone(cont['end']['tz'])

            elif ("tz" in cont['start']) & ("tz" not in cont['end']):
                start_tz = pytz.timezone(cont['start']['tz'])
                end_tz = pytz.timezone('GMT')

            elif ("tz" in cont['end']) & ("tz" not in cont['start']):
                start_tz = pytz.timezone('GMT')
                end_tz = pytz.timezone(cont['end']['tz'])

            try:
                end = end_tz.localize(end)
            except:
                end = end
            try:
                start = start_tz.localize(start)
            except:
                start = start

            dif = abs(end - start)
            return json.dumps({
                "dif": dif.__str__()
            }).encode().splitlines() 
        
            
          

def read_json(environ):
    try:
        req_size = int(environ['CONTENT_LENGTH'])
    except:
        req_size = 0
    req = environ['wsgi.input'].read(req_size)
    return json.loads(req)

with make_server('', 8000, app) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()