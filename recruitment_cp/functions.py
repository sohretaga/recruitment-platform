from datetime import datetime

def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def datetime_to_string(o):
    if isinstance(o, datetime):
        return o.strftime('%Y-%m-%d')
    raise TypeError("Type not serializable")