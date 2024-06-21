from datetime import datetime, date

def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

def datetime_to_string(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d')
    raise TypeError("Type not serializable")

def date_to_string(obj):
    if isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')