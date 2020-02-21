import urllib
import requests
import time
import random
from base64 import b64encode
import hmac
from hashlib import sha1
import json
import xmler

#signature

def generate_nonce(length=13):
    """Generate pseudorandom number."""
    return ''.join([str(random.randint(0, 9)) for i in range(length)])

def generateSign(authlist,req,realm):
    retstr = ""
    for k in sorted(authlist):
        retstr= retstr +k+"="+str(authlist[k])+"&"
    return urllib.parse.quote(req,safe='')+"&"+urllib.parse.quote(realm,safe='')+"&"+urllib.parse.quote(retstr[0:len(retstr)-1],safe='')

def genSign(key, message):
    key_bytes = bytes(key, 'latin-1')
    message_bytes = bytes(message, 'latin-1')
    hashed = hmac.new(key_bytes, message_bytes, sha1)
    return b64encode(hashed.digest())

def makeNice(dic):
    retstr = "OAuth "
    for k in sorted(dic):
        retstr = retstr + urllib.parse.quote(k,safe='')+'="'+urllib.parse.quote(dic[k],safe='')+'",'
    return retstr[0:len(retstr)-1]

def auths():
    retlist = [0, 1, 2, 3]
    f = open("auth", "r")
    for i in range(len(retlist)):
        retlist[i] = f.readline().strip().split(":")[1]
    return retlist
 
#methods
 
def stock():
	url = "https://api.cardmarket.com/ws/v2.0/stock"
	realm = "https://api.cardmarket.com/ws/v2.0/stock"
	request = "GET"
	
	return main(url, realm, request)
    
def getprod(idProduct):
    url = "https://api.cardmarket.com/ws/v2.0/products/{}".format(idProduct)
    realm = "https://api.cardmarket.com/ws/v2.0/products/{}".format(idProduct)
    request = "GET"

    return main(url, realm, request)
    
def getid(card):
    url = "https://api.cardmarket.com/ws/v2.0/products/find?search={}&exact=false".format(urllib.parse.quote(card))
    realm = "https://api.cardmarket.com/ws/v2.0/products/find"
    request = "GET"

    args = {
    "exact" : "false",
    "search" : urllib.parse.quote(card)}
	
    return main(url, realm, request, args)
    
def post(args):
    url = "https://api.cardmarket.com/ws/v2.0/stock"
    realm = "https://api.cardmarket.com/ws/v2.0/stock"
    request = "POST"
    body = xmler.main(args,"post")

    return main(url, realm, request, data = body)
    
def updatecard(args):
	url = "https://api.cardmarket.com/ws/v2.0/stock"
	realm = "https://api.cardmarket.com/ws/v2.0/stock"
	request = "PUT"

	body = xmler.main(args,"put")

	return main(url, realm, request, data = body)
    
def delete(args):
	url = "https://api.cardmarket.com/ws/v2.0/stock"
	realm = "https://api.cardmarket.com/ws/v2.0/stock"
	request = "DELETE"
	
	body = xmler.main(args,"delete")

	return main(url, realm, method = request,data = body)
    

def main(url, realm, method, args = {}, data = None):
    tokens = auths()
    appToken = tokens[0]
    appSecret = tokens[1]
    accessToken = tokens[2]
    accessSecret = tokens[3]
    nonce = generate_nonce()
    timeNow = str(time.time())
    signingKey = urllib.parse.quote(appSecret, safe='')+"&"+urllib.parse.quote(accessSecret, safe='')

    auth2 = {
    "oauth_consumer_key":appToken,
    "oauth_nonce" : nonce,
    "oauth_signature_method" : "HMAC-SHA1",
    "oauth_timestamp" : timeNow,
    "oauth_token" : accessToken,
    "oauth_version":"1.0"}
    auth2.update(args)

    rawsign = generateSign(auth2, method, realm)
    #print(rawsign)
    
    finsign = genSign(signingKey,rawsign)
    #print(finsign)
            
    auth = {
    "realm" : realm,
    "oauth_consumer_key":appToken,
    "oauth_token" : accessToken,
    "oauth_nonce" : nonce,
    "oauth_timestamp" : timeNow,
    "oauth_signature_method" : "HMAC-SHA1",
    "oauth_version":"1.0",
    "oauth_signature": finsign,
    }

    #print(makeNice(auth))
    
    if method == "GET":
        resp = requests.get(url, headers={"Authorization": makeNice(auth)})
        return(resp)
    if method == "POST":
        resp = requests.post(url, headers={"Authorization": makeNice(auth)}, data = data)
        return(resp)
    if method == "PUT":
        resp = requests.put(url, headers={"Authorization": makeNice(auth)}, data = data)
        return(resp)
    if method == "DELETE":
        resp = requests.delete(url, headers={"Authorization": makeNice(auth)}, data = data)
        return(resp)