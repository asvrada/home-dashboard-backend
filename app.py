from flask import Flask, request, jsonify
from flask_cors import CORS

import json

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
    return [
        {
            "id": 1,
            "amount": -16.00,
            "category": "食物",
            "company": "DoorDash",
            "note": "中饭",
            "timestamp": "2020-2-28"
        },
        {
            "id": 2,
            "amount": 7000.00,
            "category": "工资",
            "company": "amazon",
            "note": "房租",
            "timestamp": "2020-2-28"
        }
    ]


def handle_bill_post(req):
    print(req.json)
    return {
        "message": "doesn't matter"
    }


if __name__ == '__main__':
    app.run(port=4444)
