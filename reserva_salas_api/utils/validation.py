import re

def validar_email(email):
    patron = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(patron, email):
        return True
    else:
        return False