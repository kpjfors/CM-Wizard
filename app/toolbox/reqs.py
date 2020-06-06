import hmac
import random
import time
import urllib
from base64 import b64encode
from hashlib import sha1
from config import Config

import requests

from app.toolbox import xmler


# signature

def generate_nonce(length=13):
    return ''.join([str(random.randint(0, 9)) for i in range(length)])


def raw_url_encode(params, req, realm):
    retstr = ""
    for k in sorted(params):
        retstr += k + "=" + str(params[k]) + "&"
    retstr = urllib.parse.quote(req, safe='') + "&" + urllib.parse.quote(realm, safe='') + "&" + urllib.parse.quote(
        retstr[:len(retstr) - 1], safe='')
    return retstr


def generate_signature(key, url_string):
    key_bytes = bytes(key, 'latin-1')
    message_bytes = bytes(url_string, 'latin-1')
    hashed = hmac.new(key_bytes, message_bytes, sha1)
    return b64encode(hashed.digest())


def header_to_string(params):
    retstr = "OAuth "
    for k in sorted(params):
        retstr = retstr + urllib.parse.quote(k, safe='') + '="' + urllib.parse.quote(params[k], safe='') + '",'
    return retstr[0:len(retstr) - 1]


def get_tokens():
    ret_dict = {}
    f = open(Config.AUTH_FILE, 'r')
    for i in range(4):
        key, val = f.readline().strip().split(":")
        ret_dict[key] = val
    return ret_dict


# methods

def stock():
    url = Config.BASE_URL + "stock"
    realm = Config.BASE_URL + "stock"
    request = "GET"

    return main(url, realm, request)


def getprod(idProduct):
    url = Config.BASE_URL + "products/{}".format(idProduct)
    realm = Config.BASE_URL + "products/{}".format(idProduct)
    request = "GET"

    return main(url, realm, request)


def getid(card):
    url = Config.BASE_URL + "products/find?search={}&exact=false".format(urllib.parse.quote(card))
    realm = Config.BASE_URL + "products/find"
    request = "GET"

    args = {
        "exact": "false",
        "search": urllib.parse.quote(card)}

    return main(url, realm, request, args)


def post(args):
    url = Config.BASE_URL + "stock"
    realm = Config.BASE_URL + "stock"
    request = "POST"
    body = xmler.main(args, "post")

    return main(url, realm, request, data=body)


def updatecard(args):
    url = Config.BASE_URL + "stock"
    realm = Config.BASE_URL + "stock"
    request = "PUT"

    body = xmler.main(args, "put")

    return main(url, realm, request, data=body)


def delete(args):
    url = Config.BASE_URL + "stock"
    realm = Config.BASE_URL + "stock"
    request = "DELETE"

    body = xmler.main(args, "delete")

    return main(url, realm, method=request, data=body)


def main(url, realm, method, args={}, data=None):
    tokens = get_tokens()
    appToken = tokens['appToken']
    appSecret = tokens['appSecret']
    accessToken = tokens['accessToken']
    accessSecret = tokens['accessSecret']
    nonce = generate_nonce()
    timeNow = str(time.time())
    signingKey = urllib.parse.quote(appSecret, safe='') + "&" + urllib.parse.quote(accessSecret, safe='')

    signing_dict = {
        "oauth_consumer_key": appToken,
        "oauth_nonce": nonce,
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": timeNow,
        "oauth_token": accessToken,
        "oauth_version": "1.0"}
    signing_dict.update(args)

    raw_url = raw_url_encode(signing_dict, method, realm)
    signature = generate_signature(signingKey, raw_url)

    auth_header = {
        "realm": realm,
        "oauth_consumer_key": appToken,
        "oauth_token": accessToken,
        "oauth_nonce": nonce,
        "oauth_timestamp": timeNow,
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_version": "1.0",
        "oauth_signature": signature,
    }

    if method == "GET":
        resp = requests.get(url, headers={"Authorization": header_to_string(auth_header)})
        return resp
    if method == "POST":
        resp = requests.post(url, headers={"Authorization": header_to_string(auth_header)}, data=data)
        return resp
    if method == "PUT":
        resp = requests.put(url, headers={"Authorization": header_to_string(auth_header)}, data=data)
        return resp
    if method == "DELETE":
        resp = requests.delete(url, headers={"Authorization": header_to_string(auth_header)}, data=data)
        return resp
