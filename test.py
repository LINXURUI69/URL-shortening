import re

def is_valid(token):
    if token is None:
        return False
    pattern = r'^[^.]+\.+[^.]+\.+[^.]+$'
    return re.match(pattern, token) is not None

token = 'eyJhbG.sfdsf.dsa'
print(is_valid(token))