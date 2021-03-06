from sqlalchemy.exc import IntegrityError

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
    for i in result:
        i['line_total'] = str(i['line_total'])
        i['price'] = str(i['price'])
    return result


def add_transactions(invoice_id, transactions):
    try:
        total_id = db.session.query(Transaction).order_by('id').all()
        id_length = len(total_id)
        new_id = id_length + 1
        print(invoice_id)
        print(transactions)

        for t in transactions:
            new_id = new_id + 1
            add_transaction_in_db(new_id, invoice_id, t)

        return "Transaction has been Saved Successfully!"
    except IntegrityError as err:
        db.session.rollback()
        err_msg = err.args[0]

        if "UNIQUE constraint failed: invoice_id" in err_msg:
            return "Id should be unique for Transaction : (%s)" % id
        elif "FOREIGN KEY constraint failed" in err_msg:
            return "supplier does not exist"
        else:
            return "unknown error adding user"


def update_transactions(invoice_id, transactions):
    try:
        existing_transactions = Transaction.query.filter_by(invoice_id=invoice_id).all()
        total_id = db.session.query(Transaction).order_by('id').all()
        id_length = len(total_id)
        new_id = id_length + 1

        existing_transactions_ids = []
        for t in transactions:
            if hasattr(t, 'id'):
                existing_transactions_ids.insert(t.id)
            else:
                new_id = new_id + 1
                add_transaction_in_db(new_id, invoice_id, t)

        for t in existing_transactions:
            if t.id not in existing_transactions_ids:
                delete_transactions_by_id(t)

        return "Transaction has been Updated Successfully!"
    except IntegrityError as err:
        db.session.rollback()
        err_msg = err.args[0]

        if "UNIQUE constraint failed: invoice_id" in err_msg:
            return "Id should be unique for Transaction : (%s)" % id
        elif "FOREIGN KEY constraint failed" in err_msg:
            return "supplier does not exist"
        else:
            return "unknown error adding user"


def add_transaction_in_db(new_id, invoice_id, t):
    line_total = t['price'] * t['quantity']
    quantity = t['quantity']
    price = t['price']
    create_transaction = Transaction(id=new_id, product='product', invoice_id=invoice_id, quantity=quantity,
                                     price=price, line_total=line_total)
    db.session.add(create_transaction)
    db.session.commit()


def delete_transactions_by_id(transaction):
    db.session.delete(transaction)
    db.session.commit()
    return "Deleted!"


def delete_transactions_by_invoice_id(invoice_id):
    transactions = Transaction.query.filter_by(invoice_id=invoice_id).all()
    for transaction in transactions:
        delete_transactions_by_id(transaction)
    return "Deleted!"

