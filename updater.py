import json
import sqlite3
from time import localtime, strftime

from config import Config
from app.toolbox import reqs


def main(priceLimit, priceMod):
    print("Waking up at {}".format(strftime("%Y-%m-%d %H:%M:%S", localtime())))
    conn = sqlite3.connect(Config.SQLITE3_DATABASE_URI)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    print("Opened database successfully");

    root = json.loads(reqs.stock().text)

    for article in root['article']:
        arg = {i: article[i] for i in article}
        arg["idLanguage"] = article['language']['idLanguage']
        arg["enName"] = article['product']['enName']
        root2 = json.loads(reqs.getprod(int(arg['idProduct'])).text)
        product = root2['product']
        if arg['isFoil'] == "True":
            trendprice = product['priceGuide']['TRENDFOIL']
        else:
            trendprice = product['priceGuide']['TREND']

        oldprice = arg["price"]
        arg["price"] = round(float(trendprice) * float(priceMod), 2)

        delflag = 0
        if arg["price"] >= priceLimit:
            pass
        else:
            delflag = 1
        if delflag == 0:
            reqs.updatecard(arg)
            print("Old price for {0}: {1}, updated to {2}".format(arg["enName"], oldprice, arg["price"]))
        else:
            reqs.delete(arg)
            print("Price for {0} too low ({1}), DELETED.".format(arg["enName"], finprice))
            conn.execute("UPDATE card SET listed = null WHERE card.listed = {}".format(arg["idArticle"]));
            conn.commit()
    conn.close()
    print("Finished at {}.".format(strftime("%Y-%m-%d %H:%M:%S", localtime())))


if __name__ == "__main__":
    priceLimit = 1.5
    priceMod = 1
    main(priceLimit, priceMod)
