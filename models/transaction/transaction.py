from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from app import db


class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(255))
    invoice_id = Column(Integer, ForeignKey('invoice.id'))
    invoice = relationship("Invoice", backref=backref("invoice", uselist=False))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric)
    line_total = db.Column(db.Numeric)

    def __init__(self, id, product, invoice_id, quantity, price, line_total):
        self.id = id
        self.product = product
        self.invoice_id = invoice_id
        self.quantity = quantity
        self.price = price
        self.line_total = line_total

