from flask import request, jsonify, Blueprint

invoice_route_page = Blueprint('invoice_route_page', __name__, template_folder='invoice_templates')
from services.invoice import invoice_service


@invoice_route_page.route("/invoices", methods=["GET"])
def get_invoice():
    todos = invoice_service.fetch_invoice()
    print(todos)
    return jsonify(todos)


@invoice_route_page.route('/invoices', methods=["POST"])
def add_invoice():
    json_data = request.json
    id = json_data["id"]
    customer = json_data["customer"]
    date = json_data["date"]
    total_quantity = json_data["total_quantity"]
    total_amount = json_data["total_amount"]
    todo = invoice_service.add_invoice(id, customer, date, total_quantity, total_amount)
    return todo


@invoice_route_page.route("/invoices/<id>", methods=['GET', 'PUT', 'DELETE'])
def invoice_by_id(id):
    if request.method == 'GET':
        return get_invoice_by_id(id)
    elif request.method == 'DELETE':
        return delete_invoice_by_id(id)
    elif request.method == 'PUT':
        return update_invoice(id)


def get_invoice_by_id(id):
    todos = invoice_service.fetch_invoice_by_id(id)
    return jsonify(todos)


def delete_invoice_by_id(id):
    todos = invoice_service.delete_invoice(id)
    return jsonify(todos)


def update_invoice(id):
    json_data = request.json
    customer = json_data["customer"]
    date = json_data["date"]
    total_quantity = json_data["total_quantity"]
    total_amount = json_data["total_amount"]
    todo = invoice_service.update_invoice(id, customer, date, total_quantity, total_amount)
    return todo
