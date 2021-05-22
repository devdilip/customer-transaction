from app import app, db
from models.invoice.invoice import Invoice
from models.transaction.transaction import Transaction


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Invoice=Invoice, Transaction=Transaction)
