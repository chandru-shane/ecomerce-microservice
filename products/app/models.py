# from database import Base
from .extensions import db
from sqlalchemy import Column, Integer, String, DECIMAL



class Product(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(120))
    price = Column(DECIMAL(2))
    version = Column(Integer, default=0)
    user_id = Column(Integer)
    
    def __init__(self, name,description, price, user_id, version=0):
        self.name = name
        self.description = description
        self.price = price
        self.version = version
        self.user_id = user_id

    def __repr__(self):
        return '<Product %r>' % (self.name)

    def as_dict(self):
        price_str = str(self.price) if self.price is not None else None
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': price_str,
            'version':self.version,
            'user_id':self.user_id
        }
    


