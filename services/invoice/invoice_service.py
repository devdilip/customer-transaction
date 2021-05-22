from sqlalchemy.exc import IntegrityError
from models.invoice.invoice import Invoice
from app import db, app
from services.transaction import transaction_service

from flask_marshmallow import Marshmallow

ma = Marshmallow(app)


class InvoiceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'customer', 'date', 'total_quantity', 'total_amount')


@app.before_first_request
def create_tables():
    db.create_all()


def add_invoice(id, customer, date, total_quantity, total_amount):
    try:
        create_todo = Invoice(id=id, customer=customer, date=date, total_quantity=total_quantity, total_amount=total_amount)
        db.session.add(create_todo)
        db.session.commit()
        return "Invoice has been Saved Successfully!"
    except IntegrityError as err:
        db.session.rollback()
        err_msg = err.args[0]

        if "UNIQUE constraint failed: todo.id" in err_msg:
            return "Id should be unique : (%s)" % id
        elif "FOREIGN KEY constraint failed" in err_msg:
            return "supplier does not exist"
        else:
            return "unknown error adding user"


def fetch_invoice():
    invoices = Invoice.query.all()
    invoice_schema = InvoiceSchema(many=True)
    result = invoice_schema.dump(invoices)
    for r in result:
        transaction = transaction_service.fetch_status_by_invoice_id(r['id'])
        r['transaction'] = transaction
    return result


def fetch_invoice_by_id(id):
    invoice = Invoice.query.filter_by(id=id).first()
    todo_schema = InvoiceSchema()
    result = todo_schema.dump(invoice)
    if bool(invoice) is True:
        transaction = transaction_service.fetch_status_by_invoice_id(invoice.id)
        result['transaction'] = transaction
    return result


def update_invoice(id, customer, date, total_quantity, total_amount):
    try:
        invoice = Invoice.query.filter_by(id=id).first()
        if bool(invoice) is True:
            invoice.customer = customer
            invoice.date = date
            invoice.total_quantity = total_quantity
            invoice.total_amount = total_amount
            db.session.commit()
            return "Invoice has been Updated Successfully!"
        else:
            return "Invoice has not found from given id!"
    except IntegrityError as err:
        db.session.rollback()
        err_msg = err.args[0]
        return err_msg


def delete_invoice(id):
    try:
        todos = Invoice.query.filter_by(id=id).first()
        if bool(todos) is True:
            db.session.delete(todos)
            db.session.commit()
            return "Todo has been Deleted Successfully!"
        else:
            return "Todo has not found from given id!"
    except IntegrityError as err:
        db.session.rollback()
        err_msg = err.args[0]
        return err_msg
