def measure():
    pass

def to_string(val, default=''):
    if val == None:
        return default

    try:
        return str(val)
    except:
        return default

def to_int(val, default=0):
    if val == None:
        return default

    try:
        return int(val)
    except ValueError:
        return default
