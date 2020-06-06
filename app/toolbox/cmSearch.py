import json

from app.toolbox import reqs


class Card:
    def __init__(self, img, name, idProduct):
        self.img = img
        self.name = name
        self.idProduct = idProduct


def searcher(search):
    cards = []
    resp = reqs.getid(search)
    resp = json.loads(resp.text)
    for product in resp['product']:
        catname = product["categoryName"]
        if catname != "Magic Single":
            pass
        else:
            img = product["image"]
            name = product["enName"]
            idProduct = product["idProduct"]
            cards.append(Card(img, name, idProduct))
    return cards
