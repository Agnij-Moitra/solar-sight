from flask import Flask, jsonify, Request
from supplementry import get_preds

app = Flask(__name__)

@app.route('/<location>', methods = ['GET'])
def index(location):
    return jsonify({'estimatedElectricity': float(get_preds(location)), 'unit': 'watts'})
  
if __name__ == '__main__':
  
    app.run(debug = True)