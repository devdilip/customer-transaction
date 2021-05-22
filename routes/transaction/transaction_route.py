from flask import request, jsonify, Blueprint

transaction_route_page = Blueprint('transaction_route_page', __name__, template_folder='transaction_templates')
from services.transaction import transaction_service


@transaction_route_page.route("/invoices/<invoice_id>/transaction", methods=["POST"])
def add_transactions_by_invoice_id(invoice_id):
    json_data = request.json
    todos = transaction_service.add_transactions(invoice_id, json_data)
    print(todos)
    return jsonify(todos)


@transaction_route_page.route("/invoices/transaction/<id>", methods=['GET', 'DELETE'])
def transactions_by_id(id):
    if request.method == 'GET':
        return get_transactions_by_id(id)
    elif request.method == 'DELETE':
        return delete_transactions_by_id(id)


def get_transactions_by_id(id):
    invoice = transaction_service.fetch_status_by_invoice_id(id)
    return jsonify(invoice)


def delete_transactions_by_id(id):
    invoice = transaction_service.fetch_status_by_invoice_id(id)
    return jsonify(invoice)
