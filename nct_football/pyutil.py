import requests,json,os

def _getpath():
    return os.path.dirname(os.path.abspath(__file__))

def _get_json(filejson):

    # Opening JSON file 
    f = open(filejson) 
    
    # returns JSON object as  
    # a dictionary 
    data = json.load(f) 
   
    # Closing file 
    f.close()
    return data


def _linux2time(str):
    from datetime import datetime
    import tzlocal  # $ pip install tzlocal

    unix_timestamp = float(str)
    local_timezone = tzlocal.get_localzone() # get pytz timezone
    local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)
    date = local_time.strftime('%Y-%m-%d')
    time = local_time.strftime('%H:%M:%S')

    return {'date':date, 'time':time}

def _extract_values_json(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results
