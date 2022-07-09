from flask import Flask, jsonify, request
# https://www.geeksforgeeks.org/python-build-a-rest-api-using-flask/

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
  
        data = "hello world"
        return jsonify({'data': data})

@app.route('/home/<int:num>', methods = ['GET'])
def disp(num):
  
    return jsonify({'data': num**2})
  
if __name__ == '__main__':
  
    app.run(debug = True)