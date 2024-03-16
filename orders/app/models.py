from datetime import datetime
from app import db
# from database import Base
from sqlalchemy import Column, Integer, String, JSON, DECIMAL, DateTime, Enum

from sqlalchemy.dialects.postgresql import JSON


class Order(db.Model):

    class StatusEnum(str, Enum):
        pending = 'pending'
        on_the_way = 'on_the_way'
        delivered = 'delivered'



    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    user_id = Column(Integer)
    price = Column(DECIMAL(2))
    quanity = Column(Integer)
    status = Column(String, default=StatusEnum.pending)
    expected_delivery_time = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, product_id=None, user_id=None, quantity=None, status=None,
                 price=None, expected_delivery_time=None, *args, **kwargs):
        self.product_id = product_id
        self.user_id = user_id
        self.quantity = quantity
        self.status = status
        self.price = price
        self.expected_delivery_time = expected_delivery_time


    def __repr__(self):
        return f"<Order {self.id}>"