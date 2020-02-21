import reqs

import time
from time import localtime, strftime
import sqlite3
import xml.etree.ElementTree as ET

priceLimit = 1.5

#while 1:
print("Waking up at {}".format(strftime("%Y-%m-%d %H:%M:%S", localtime())))
conn = sqlite3.connect('../magic.db')
cur = conn.cursor()
print("Opened database successfully");

root = ET.fromstring(reqs.stock().text) 
for article in root.findall('article'):
    arg = {i.tag: i.text for i in article.findall('*')}
    arg.update({"idLanguage":article.find('language').find('idLanguage').text})
    arg.update({"enName":article.find('product').find('enName').text})
    #arg.update({"idLanguage":arg["language"].find('idLanguage')})
    root2 = ET.fromstring(reqs.getprod(int(arg['idProduct'])).text)
    product = root2.find('product')
    if arg['isFoil'] == "true":
        trendprice = product.find('priceGuide').find("TRENDFOIL").text
    else:
        trendprice = product.find('priceGuide').find("TREND").text
    arg.update({"trendprice":trendprice})
    cur.execute("SELECT pricemod FROM cards WHERE cards.listed = {}".format(arg["idArticle"]))
    
    for i in cur.fetchall():
        priceMod = i[0]
    arg.update({"finprice":round(float(trendprice)*float(priceMod),2)})
    
    

    delflag = 0
    finprice = round(float(trendprice)*float(priceMod),2)
    if finprice > priceLimit:
        pass
    else:
        delflag = 1
    if delflag == 0:
        asd = reqs.updatecard(arg) #skicka ett dict ist
        print("Old price for {0}: {1}, updated to {2}".format(arg["enName"], arg["price"], finprice))
    else:
        reqs.delete(arg)
        print("Price for {0} too low ({1}), DELETED.".format(arg["enName"], finprice))
        conn.execute("UPDATE cards SET listed = null WHERE cards.listed = {}".format(arg["idArticle"]));
        conn.commit()
conn.close()
print("Finished at {}.".format(strftime("%Y-%m-%d %H:%M:%S", localtime())))
    #print("Sleeping for 3h. Good night")
    #time.sleep(10800)
