from flask import Flask, jsonify, Request, render_template
from supplementry import get_preds
from geopy.geocoders import Nominatim

app = Flask(__name__)
geolocator = Nominatim(user_agent="geoapiExercises")

@app.route("/", methods = ['GET'])
def index():
    return render_template("./index.html")

@app.route('/latlot', methods = ['GET'])
def api():
    location = geolocator.reverse(Request.argsto_dict().get("place")).raw['address'].get('state', '')
    return jsonify({'estimatedElectricity': float(get_preds(str(location))), 'unit': 'watts'})

@app.route('/api/<location>', methods = ['GET'])
def api(location):
    return jsonify({'estimatedElectricity': float(get_preds(str(location))), 'unit': 'watts'})
  
if __name__ == '__main__':
  
    app.run(debug = True)
