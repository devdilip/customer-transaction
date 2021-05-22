from models.transaction.transaction import Transaction
from app import db, app

from flask_marshmallow import Marshmallow

ma = Marshmallow(app)


class TransactionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'product', 'invoice_id', 'quantity', 'price', 'line_total')


@app.before_first_request
def create_tables():
    db.create_all()


def fetch_status_by_invoice_id(invoice_id):
    transactions = Transaction.query.filter_by(invoice_id=invoice_id).all()
    print(transactions)
    transactions_schema = TransactionSchema(many=True)
    result = transactions_schema.dump(transactions)
    return result

