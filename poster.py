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
    cur.execute("SELECT * FROM card where card.idArticle is null")

    rows = cur.fetchall()
    i = 0
    j = 0
    for row in rows:
        arg = {i: row[i] for i in row.keys()}
        product = json.loads(reqs.getprod(arg['idProduct']).text)['product']
        if arg['isFoil'] == "true":
            trendprice = product['priceGuide']['TRENDFOIL']
        else:
            trendprice = product['priceGuide']['TREND']

        finprice = round(float(trendprice) * priceMod, 2)
        arg.update({"price": finprice})
        try:
            if finprice > priceLimit:
                resp = json.loads(reqs.post(arg).text)  # get article object extract idArticle.
                article = resp['inserted'][0]
                if article['success']:
                    idArticle = article['idArticle']['idArticle']
                    query = "UPDATE card SET idArticle = {0} WHERE card.id = {1}".format(idArticle, arg['id'])
                    conn.execute(query)
                    conn.commit()
                    print("Posted {0} {1} for {2} €.".format(arg["count"], arg["name"], finprice))
                    i += 1
                else:
                    print('Failed in posting {}'.format(article['product']['enName']))
            else:
                # print("Price too low for {0}. ({1} €).".format(arg["name"],finprice))
                j += 1
        except:
            print("Error posting listing.")
            raise
    conn.close()
    print("Finished at {3}. {0} cards scanned. {1} posted, {2} not posted".format(i + j, i, j,
                                                                                  strftime("%Y-%m-%d %H:%M:%S",
                                                                                           localtime())))


if __name__ == "__main__":
    priceLimit = 1.5
    priceMod = 1
    main(priceLimit, priceMod)
