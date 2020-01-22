from flask import Flask
from flask_cors import CORS
import json


app = Flask(__name__)

CORS(app)


DATA = [{
    "time": "kaki time",
    "lat": " ", "lan": " ", "img": " ", "video": "kaki video ", "msg": "kaki msg ", "category": "category"
}]


@app.route("/", methods=['GET'])
def hello():
    return json.dumps(DATA)


if __name__ == "__main__":
    app.run()