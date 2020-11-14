from paste.httpserver import serve
import json
from pytz import timezone
from datetime import datetime
from tzlocal import get_localzone
from pytz import UnknownTimeZoneError

#словарь переменных окружения (environ)
#обработчик запроса (start_response)

def application(environ, start_response):
    status = '200 OK'   #arguments for start_responce
    response_headers = [('Content-type', 'text/plain')]
    if environ['REQUEST_METHOD'] == 'GET':
        get_tz = environ['PATH_INFO'][1:]
        if not get_tz:
            get_tz = None   #временная зона сервера
            text = 'Time is '
        else:
            try:
                get_tz = timezone(get_tz)   #время в запрошенной зоне
                text = 'Time in %s is ' % get_tz
            except UnknownTimeZoneError:
                start_response(status, response_headers)
                return [bytes('Unknown timezone',  encoding = 'utf-8')]
        start_response(status, response_headers)
        return [bytes(text + datetime.now(tz = get_tz).strftime('%H:%M:%S'), encoding = 'utf-8')]

    if environ['REQUEST_METHOD'] == 'POST':
        request_body_bytes = environ['wsgi.input'].read()
        request_body_str = request_body_bytes.decode("utf-8")
        request_body_str = json.loads(request_body_str)
        m_type = request_body_str['type']
        try:
            start = request_body_str['tz_start']
        except KeyError:
            start = None
        if start is None:
            start = get_localzone()
        else:
            start = timezone(start)
        str_start = str(start)
        try:
            end = request_body_str['tz_end']
        except KeyError:
            end = None
        if end is None:
            end = get_localzone()
        else:
            end = timezone(end)
        str_end = str(end)
        if m_type == 'date':
            start_response(status, response_headers)
            return [bytes(json.dumps({'date': datetime.now(tz = start).strftime('%d/%m/%Y'), 'tz': str_start})
                          , encoding='utf-8')]
        elif m_type == 'time':
            start_response(status, response_headers)
            return [bytes(json.dumps({'time': datetime.now(tz = start).strftime('%H:%M:%S'), 'tz': str_start})
                          , encoding='utf-8')]
        elif m_type == 'datediff':
            date_start = datetime.now(tz = start).tzinfo.localize(datetime.now())
            date_end = datetime.now(tz = end).tzinfo.localize(datetime.now())
            if date_start <= date_end:
                delta = str(date_end - date_start)
            else:
                delta = '-' + str(date_start - date_end)
        start_response(status, response_headers)
        return [bytes(json.dumps({'diff': delta, 'tz_start': str_start, 'tz_end': str_end}), encoding = 'utf-8')]

serve(application)
