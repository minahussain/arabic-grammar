from flask import Flask, request
from flask_cors import CORS, cross_origin
import os
import arabic_parser

app = Flask(__name__, static_folder='../build', static_url_path='/')
CORS(app, support_credentials=True)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')

@cross_origin(origin="*")
@app.route('/api/pos', methods = ['POST'])
def get_pos():
    # call parser to handle text
    # todo add check string is arabic
    text = request.json
    pr = arabic_parser.ArabicParser()

    try:
        return pr.parse(text)
    except arabic_parser.ParseError as e:
        print('Error: ' + str(e))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 80))

