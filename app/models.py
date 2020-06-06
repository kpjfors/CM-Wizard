from datetime import datetime
from app import db

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idProduct = db.Column(db.Integer, unique=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    idLanguage = db.Column(db.Integer, unique=False, nullable=False)
    condition = db.Column(db.String(2), unique=False, nullable=False)
    count = db.Column(db.Integer, unique=False, nullable=False)
    isFoil = db.Column(db.String) #Boolean but should take "true/false" as string instead
   # isSigned = db.Column(db.String)
   # isAltered = db.Column(db.String)
   # isPlayset = db.Column(db.String)
    idArticle = db.Column(db.String)
    comments = db.Column(db.String(200), unique=False)
    img = db.Column(db.String(200), unique=False)
    __table_args__ = (db.UniqueConstraint('idProduct','name','idLanguage','condition','isFoil', name='_card_nondup_uc'),)

    def __repr__(self):
        return '<Name %r>' % self.name

class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idProduct = db.Column(db.Integer, db.ForeignKey('card.idProduct'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    price = db.Column(db.Float, nullable=False)


    def __repr__(self):
        return '<Name %r>' % self.name