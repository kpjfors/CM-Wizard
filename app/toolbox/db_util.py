from app import db
from app.models import Card


def add_card(data):
    for key in ['csrf_token', 'submit', 'id']:
        data.pop(key)
    q = Card(**data)
    db.session.add(q)
    db.session.commit()


def query_card(search=None):
    if not search:
        cards = Card.query.all()
    else:
        cards = Card.query.filter(Card.name.like('%{}%'.format(search))).all()
    return cards


def update_card(data):
    for key in ['csrf_token', 'submit']:
        data.pop(key)
    card_row = Card.query.get(data['id'])
    for key, value in data.items():
        setattr(card_row, key, value)
    db.session.commit()


def delete_card(data):
    for key in ['csrf_token', 'submit']:
        data.pop(key)
    card_row = Card.query.get(data['id'])
    db.session.delete(card_row)
    db.session.commit()
