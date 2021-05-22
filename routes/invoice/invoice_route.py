from flask import request, jsonify, Blueprint

invoice_route_page = Blueprint('invoice_route_page', __name__, template_folder='invoice_templates')
from services.invoice import invoice_service
from services.transaction import transaction_service


@invoice_route_page.route("/invoices", methods=["GET"])
def get_invoice():
    invoices = invoice_service.fetch_invoice()
    return jsonify(invoices)


@invoice_route_page.route('/invoices', methods=["POST"])
def add_invoice():
    json_data = request.json
    invoices = invoice_service.add_invoice(json_data)
    return invoices


@invoice_route_page.route("/invoices/<invoice_id>/transaction", methods=["POST"])
def add_transactions_by_invoice_id(invoice_id):
    json_data = request.json
    invoices = transaction_service.add_transactions(invoice_id, json_data)
    return jsonify(invoices)


@invoice_route_page.route("/invoices/<id>", methods=['GET', 'PUT', 'DELETE'])
def invoice_by_id(id):
    if request.method == 'GET':
        return get_invoice_by_id(id)
    elif request.method == 'DELETE':
        return delete_invoice_by_id(id)
    elif request.method == 'PUT':
        return update_invoice(id)


def get_invoice_by_id(id):
    invoices = invoice_service.fetch_invoice_by_id(id)
    return jsonify(invoices)


def delete_invoice_by_id(id):
    invoices = invoice_service.delete_invoice(id)
    return jsonify(invoices)


def update_invoice(id):
    json_data = request.json
    customer = json_data["customer"]
    date = json_data["date"]
    total_quantity = json_data["total_quantity"]
    total_amount = json_data["total_amount"]
    invoices = invoice_service.update_invoice(id, customer, date, total_quantity, total_amount)
    return invoices
