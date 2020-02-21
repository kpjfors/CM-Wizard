import reqs

import time
from time import localtime, strftime
import sqlite3
import xml.etree.ElementTree as ET

priceLimit = 1.5

#while 1:
print("Waking up at {}".format(strftime("%Y-%m-%d %H:%M:%S", localtime())))
conn = sqlite3.connect("magic.db")
cur = conn.cursor()
print("Opened database successfully");
cur.execute("SELECT * FROM cards where cards.listed is null")
 
rows = cur.fetchall()
i = 0
j = 0
for row in rows:
    arg = {"idProduct" : row[0],
            "name" : row[1],
            "count" : row[2],
            "idLanguage" : row[3],
            "condition" : row[4],
            "isfoil" : row[5],
            "issigned" : row[6],
            "isaltered" : row[7],
            "isplayset" : row[8],
            "comments" : row[9],
            "listed" : row[10],
            "priceMod" : row[11],
            "imgurl" : row[12],
            "index" : row[13]
           }        
    
    root2 = ET.fromstring(reqs.getprod(int(arg['idProduct'])).text)
    product = root2.find('product')
    if arg['isfoil'] == "true":
        trendprice = product.find('priceGuide').find("TRENDFOIL").text
    else:
        trendprice = product.find('priceGuide').find("TREND").text

    arg.update({"trendprice":trendprice})
    finprice = round(float(trendprice)*arg["priceMod"],2)
    arg.update({"finprice":finprice})
    try:
        if finprice > priceLimit:
            resp = reqs.post(arg) #get article object extract idArticle.
            a = ET.fromstring(resp.text)
            article = a.find('inserted').find('idArticle').find('idArticle').text
            query = "UPDATE cards SET listed = {0} WHERE cards.idx = {1}".format(article, arg["index"])
            conn.execute(query)
            conn.commit()
            print("Posted {0} {1} for {2} €.".format(arg["count"], arg["name"], finprice))
            i += 1
        else:
            #print("Price too low for {0}. ({1} €).".format(arg["name"],finprice))
            j += 1
    except:
        print("Error posting listing.")
        raise
conn.close()
print("Finished at {3}. {0} cards scanned. {1} posted, {2} not posted".format(i+j,i,j,strftime("%Y-%m-%d %H:%M:%S", localtime())))