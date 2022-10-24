from flask import Flask, jsonify, request, render_template
from supplementry import get_preds, get_time_preds

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index(): return render_template("./index.html")


@app.route('/api/', methods=['GET'])
def api(): return jsonify({'estimatedElectricity': float(
    get_preds(str(request.args.to_dict().get('place')))), 'unit': 'watts'})

@app.route('/api/time-series/', methods=['GET'])
def api_series():
    res = request.args.to_dict(flat=False)
    dayofyear = int(res.get('dayofyear')[0])
    dayofweek = int(res.get('dayofweek')[0])
    quarter = int(res.get('quarter')[0])
    month = int(res.get('month')[0])
    year = int(res.get('year')[0])
    state = res.get('state')[0]
    region = res.get('region')[0]
    return jsonify({'estimatedDemanded': get_time_preds(
        dayofyear, dayofweek, quarter, month, year, state, region
    )})


if __name__ == '__main__':
    app.run(debug=True)
