from flask import Flask, jsonify, request
from mongo import get_mongo

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
  return jsonify({
    "message": "API立ち上がってまーす！"})

@app.route('/test')
def mongo_test():
  conf = get_mongo()
  col = conf['test']['test_col']
  data = col.find_one()
  return jsonify(data)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
