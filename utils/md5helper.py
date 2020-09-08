import hashlib

def ecnrypt(s):
    result = hashlib.md5(s.encode())
    return str(result.hexdigest())

def validateS(sHash,sToValidate):
    return sHash == str(ecnrypt(sToValidate))
