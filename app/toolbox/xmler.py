from xml.etree.ElementTree import Element, SubElement, Comment, tostring

def main(args, method):
    if method == "delete":
        a = ["idArticle","count"]
    if method == "put":
        a = ["idArticle","idLanguage","comments","count","price","condition","isFoil"]
    if method == "post":
        a = ["idProduct","idLanguage","comments","count","price","condition","isFoil"]
    top = Element("request")
    art = SubElement(top, "article")
    for i in a:
        row = SubElement(art, i)
        if type(args[i]) == int or type(args[i]) == float:
            row.text = str(args[i])
        else:
            row.text = args[i]

    return tostring(top, encoding='utf8')