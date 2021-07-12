import time
from flask import Flask, request, jsonify
from flask_cors import CORS
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

# camel-tools comes w/ morphological database
# and outputs a complete analysis of the possible forms 
# and meanings of the word, including the lemma, part of speech, 
# English translation if available, etc
# ths function uses the morph db to get the parts of speech for each word in `text`
def get_pos_from_morph_analysis(text):
    db = MorphologyDB.builtin_db()
    analyzer = Analyzer(db)
    dict = {}

    # get parts of speech per word
    for word in text:
        analyses = analyzer.analyze(word)
        # take top result
        if analyses:
            pos = analyses[0]['pos']
            dict[word] = pos
            # double checking
            for i in range(0,1):
                print(analyses[i], '\n')
    return dict

# POS = Parts of Speech i.e. ADJ, NOUN, VERB, ...
# @app.route('/api/pos', methods = ['POST'])
# def get_pos():
#     # can we check the string is arabic?
#     result = request.json
#     # apply dediacritization to remove grammar markings
#     result = dediac_ar(result)
#     result = ortho_normalize(result)
#     result = simple_word_tokenize(result)
#     result_dict = get_pos_from_morph_analysis(result)
#     return result_dict

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

