from xml.etree.ElementTree import Element, SubElement, Comment, tostring

def main(args, method):
    if method == "delete":
        a = ["idArticle","count"]
    if method == "put": #putcard
        a = ["idArticle","idLanguage","comments","count","price","condition","isFoil","isSigned","isAltered","isPlayset"]
    if method == "post": #testreq
        a = ["idProduct","idLanguage","comments","count","price","condition","isFoil","isSigned","isAltered","isPlayset"]
    top = Element("request")
    art = SubElement(top, "article")
    for i in a:
        row = SubElement(art, i)
        row.text = args[i]


    return tostring(top, encoding='utf8')