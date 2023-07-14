import urllib.parse
import hmac
import hashlib


def sign(data, secret):
    message = urllib.parse.urlencode(data).encode()
    byte_key = bytes(secret, 'UTF-8')
    mac = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
    return mac