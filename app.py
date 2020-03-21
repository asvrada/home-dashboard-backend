from flask import Flask, request, jsonify
from flask_cors import CORS

from server import database_table as dt

app = Flask(__name__)
CORS(app)

GET = 'GET'
POST = 'POST'


@app.route('/')
def index():
    return "you shouldn't be here"


@app.route("/summary/")
def summary():
    return {
        # sum of all income this month
        "total": 7000,
        "remainingTotal": 1200,
        "remainingToday": 200
    }


@app.route("/bill/", methods=[GET, POST])
def bill():
    dict_handler = {
        GET: handle_bill_get,
        POST: handle_bill_post
    }

    response_data = dict_handler[request.method](request)

    return jsonify(response_data)


def handle_bill_get(req):
    query_set = dt.Transaction.select()
    return [each.serialize for each in query_set]


def handle_bill_post(req):
    """
    Always assume input is valid
    """
    dict_transaction = req.json

    print(type(dict_transaction), dict_transaction)

    dt.Transaction.create(**dict_transaction)

    return {
        "message": "doesn't matter"
    }


if __name__ == '__main__':
    dt.db.connect()
    # only run once to populate database
    # dt.db_create_table()

    app.run(port=4444)

    print("Server shut down")
    dt.db.close()
