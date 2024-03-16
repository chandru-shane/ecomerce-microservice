# from database import Base
from .extensions import db
from sqlalchemy import Column, Integer, String, JSON, DECIMAL

from sqlalchemy.dialects.postgresql import JSON


class Product(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(120))
    price = Column(DECIMAL(2))
    version = Column(Integer, default=0)
    
    def __init__(self, name=None,description=None, price=None):
        self.name = name
        self.description = description
        self.price = price

    def __repr__(self):
        return '<Product %r>' % (self.name)

    def as_dict(self):
        price_str = str(self.price) if self.price is not None else None
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': price_str
        }
    


