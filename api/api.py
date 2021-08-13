from flask import Flask, request
from flask_cors import CORS, cross_origin
# import camel tools
from camel_tools.utils.dediac import dediac_ar
from camel_tools.utils.normalize import normalize_alef_maksura_ar
from camel_tools.utils.normalize import normalize_alef_ar
from camel_tools.utils.normalize import normalize_teh_marbuta_ar
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
# import arabic parser
import arabic_parser

app = Flask(__name__, static_folder='../build')
CORS(app, support_credentials=True)
app.config['JSON_AS_ASCII'] = False

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

