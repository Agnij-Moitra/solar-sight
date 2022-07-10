from flask import Flask, jsonify, Request
from supplementry import get_preds

app = Flask(__name__)


@app.route("/", methods = ['GET'])
def index():
    return "https://github.com/Agnij-Moitra/solar-sight"


@app.route('/api/<location>', methods = ['GET'])
def api(location):
    print(get_preds(location))
    return jsonify({'estimatedElectricity': float(get_preds(str(location))), 'unit': 'watts'})
  
if __name__ == '__main__':
  
    app.run(debug = True)