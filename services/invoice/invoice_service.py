from sqlalchemy.exc import IntegrityError
from models.invoice.invoice import Invoice
from app import db, app
from datetime import date
from services.transaction import transaction_service
from utils import utils

from flask_marshmallow import Marshmallow

ma = Marshmallow(app)


class InvoiceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'customer', 'date', 'total_quantity', 'total_amount')


@app.before_first_request
def create_tables():
    db.create_all()


def add_invoice(invoice_data):
    try:
        total_id = db.session.query(Invoice).order_by('id').all()
        id_length = len(total_id)
        customer = invoice_data["customer"]
        total_amount = 0
        total_quantity = 0
        today_date = date.today()
        transactions = invoice_data["transactions"]
        for t in transactions:
            total_amount = total_amount + (t['price'] * t['quantity'])
            total_quantity = total_quantity + t['quantity']

        new_id = id_length + 1
        create_invoice = Invoice(id=new_id, customer=customer, date=today_date, total_quantity=total_quantity,
                                 total_amount=total_amount)
        db.session.add(create_invoice)
        db.session.commit()
        transaction_service.add_transactions(new_id, transactions)

        return "Invoice has been Saved Successfully!"
    except IntegrityError as err:
        db.session.rollback()
        err_msg = err.args[0]

        if "UNIQUE constraint failed: invoice.id" in err_msg:
            return "Id should be unique : (%s)" % id
        elif "FOREIGN KEY constraint failed" in err_msg:
            return "supplier does not exist"
        else:
            return "unknown error adding user"


def fetch_invoice():
    invoices = Invoice.query.all()
    print(invoices)
    invoice_schema = InvoiceSchema(many=True)

    result = invoice_schema.dump(invoices)
    for r in result:
        transaction = transaction_service.fetch_status_by_invoice_id(r['id'])
        r['transaction'] = transaction

    for i in result:
        i['total_amount'] = utils.convert_decimal(i['total_amount'])

    return result


def fetch_invoice_by_id(id):
    invoice = Invoice.query.filter_by(id=id).first()
    invoice_schema = InvoiceSchema()
    result = invoice_schema.dump(invoice)
    if bool(invoice) is True:
        result['total_amount'] = utils.convert_decimal(result['total_amount'])
        transaction = transaction_service.fetch_status_by_invoice_id(invoice.id)
        result['transaction'] = transaction
    return result


def update_invoice(id, invoice_data):
    try:
        invoice = Invoice.query.filter_by(id=id).first()
        if bool(invoice) is True:
            total_amount = 0
            total_quantity = 0
            transactions = invoice_data["transactions"]
            for t in transactions:
                total_amount = total_amount + (t['price'] * t['quantity'])
                total_quantity = total_quantity + t['quantity']

            customer = invoice_data["customer"]
            invoice.customer = customer
            invoice.date = date.today()
            invoice.total_amount = total_amount
            invoice.total_quantity = total_quantity
            db.session.commit()
            transaction_service.update_transactions(id, transactions)

            return "Invoice has been Updated Successfully!"
        else:
            add_invoice(invoice_data)
    except IntegrityError as err:
        db.session.rollback()
        err_msg = err.args[0]
        return err_msg


def delete_invoice(id):
    try:
        invoice = Invoice.query.filter_by(id=id).first()
        if bool(invoice) is True:
            db.session.delete(invoice)
            db.session.commit()
            transaction_service.delete_transactions_by_invoice_id(id)

            return "Invoice has been Deleted Successfully!"
        else:
            return "Invoice has not found from given id!"
    except IntegrityError as err:
        db.session.rollback()
        err_msg = err.args[0]
        return err_msg
