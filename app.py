import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.invoice.invoice_route import invoice_route_page
# from routes.transaction.transaction_route import transaction_route_page

app = Flask(__name__)
db = SQLAlchemy()
app.register_blueprint(invoice_route_page)
# app.register_blueprint(transaction_route_page)


def setup(app, **kwargs):
    db_name = 'customer-transaction.sqlite'
    app.secret_key = "5223"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app


@app.route('/')
def health():
    return 'Fine!'


if __name__ == '__main__':
    application = setup(app, **os.environ)
    application.run(debug=True)
