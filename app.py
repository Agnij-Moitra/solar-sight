from flask import Flask, jsonify, request, render_template
from supplementry import get_preds

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def index(): return render_template("./index.html")

@app.route('/api/', methods = ['GET'])
def api(): return jsonify({'estimatedElectricity': float(get_preds(str(request.args.to_dict().get('place')))), 'unit': 'watts'})
  
if __name__ == '__main__':
    app.run(debug = True)
