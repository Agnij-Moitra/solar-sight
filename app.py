from flask import Flask, jsonify, Request, render_template
from supplementry import get_preds

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def index():
    return render_template("./index.html")

@app.route('/api/<location>', methods = ['GET'])
def api(location):
    return jsonify({'estimatedElectricity': float(get_preds(str(location))), 'unit': 'watts'})
  
if __name__ == '__main__':
    app.run(debug = True)
