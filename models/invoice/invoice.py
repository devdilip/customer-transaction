from app import db


class Invoice(db.Model):
    __tablename__ = 'invoice'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(255))
    date = db.Column(db.String(255))
    total_quantity = db.Column(db.Integer)
    total_amount = db.Column(db.Numeric)

    def __init__(self, id, customer, date, total_quantity, total_amount):
        self.id = id
        self.customer = customer
        self.date = date
        self.is_active = total_quantity
        self.total_amount = total_amount


