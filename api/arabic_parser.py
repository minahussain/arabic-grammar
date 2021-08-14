import json
# import camel tools
from camel_tools.utils.dediac import dediac_ar
from camel_tools.utils.normalize import normalize_alef_maksura_ar
from camel_tools.utils.normalize import normalize_alef_ar
from camel_tools.utils.normalize import normalize_teh_marbuta_ar
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer

class ParseError(Exception):
    def __init__(self, pos, msg, *args):
        self.pos = pos
        self.msg = msg
        self.args = args

    def __str__(self):
        return '%s at position %s' % (self.msg % self.args, self.pos)

# Grammar
# Start -> Sentence
# Sentence -> N | V (nominal or verbal)
# N -> Subject + Pred
# V -> Verb + Subject + Object
# Subject -> Noun'
# Pred -> Noun' | Sentence | Phrase
# Phrase -> (Adv | Prep) + Noun'
# Prep -> e
# Noun' -> NA | Noun
# NA -> Noun + Adj
# Noun -> e
# Adj -> e
class POSParser:
    nouns = [
        'NOUN',
        'NOUN_NUM',
        'NOUN_PROP',
        'NOUN_QUANT',
        'PRON',
        'PRON_DEM',
        'PRON_INTERROG',
        'PRON_EXCLAM',
        'PRON_REL'
    ]
    adjs = [
        'ADJ',
        'ADJ_NUM',
        'ADJ_COMP',
    ]
    adv = [
        'ADV',
        'ADV_INTERROG',
        'ADV_REL'
    ]
    verbs = [
        'VERB',
        'VERB_PSEUDO',
        'VERB_NOM',
    ]
    parts = [
        'PART',
        'PART_DET',
        'PART_NEG',
        'PART_FUT',
        'PART_PROG',
        'PART_VERB',
        'PART_VOC',
        'PART_INTERROG',
        'PART_RESTRICT',
        'PART_FOCUS',
        'PART_EMPHATIC',
        'PART_RC',
        'PART_CONNECT'
    ]
    prep = [
        'PREP'
    ]
    other = [
        'CONJ',
        'CONJ_SUB',
        'DIGIT',
        'ABBREV',
        'INTERJ',
        'PUNC',
    ]
    db = MorphologyDB.builtin_db()
    analyzer = Analyzer(db)

    def __init__(self):
        self.cache = {}

    def parse(self, text):
        self.text = text
        self.pos = -1
        self.len = len(text.split()) - 1
        rv = self.start()
        self.assert_end()
        rv_json = json.dumps(rv, indent=2)
        print(rv_json)
        return rv_json

    def assert_end(self):
        if self.pos < self.len:
            raise ParseError(
                self.pos + 1,
                'Expected end of string but got %s',
                self.text[self.pos + 1]
            )
    
    def match(self, *rules):
        last_error_rules = [] 
        last_error_pos = -1
        last_exception = None
        last_error_rules = []

        for rule in rules:
            initial_pos = self.pos
            try:
                rv = getattr(self, rule)()
                return rv
            except ParseError as e:
                # this word wasn't processed
                # return position back to where it was
                self.pos = initial_pos

                # keep track of multiple error messages
                # from trying multiple rules
                if e.pos > self.len:
                    last_exception = e
                    last_error_pos = e.pos-1
                    last_error_rules.clear()
                    last_error_rules.append(rule)
                elif e.pos > last_error_pos:
                    last_exception = e
                    last_error_pos = e.pos
                    last_error_rules.clear()
                    last_error_rules.append(rule)
                elif e.pos == last_error_pos:
                    last_error_rules.append(rule)

        # now raise error(s)
        if len(last_error_rules) == 1:
            raise last_exception
        else:
            raise ParseError(
                last_error_pos,
                'Expected %s but got %s',
                ','.join(str(last_error_rules)),
                self.text[last_error_pos]
            )

    def keyword(self, expected_pos: list):
        if self.pos >= self.len:
            raise ParseError(
                self.pos + 1,
                'Expected %s but got end of text',
                ','.join(str(expected_pos))
            )

        word = self.text[self.pos + 1]
        analyses = POSParser.analyzer.analyze(word)

        # take top results if matches the expected part of speech
        # todo sophisticate matching with maybe checks?
        for analysis in analyses:
            print(word)
            print(analysis['pos'])
            if analysis['pos'] and str(analysis['pos']).upper() in expected_pos:
                partOfSpeech = str(analysis['pos'])
                self.pos += 1
                return dict(partOfSpeech=partOfSpeech, word=word, children=[])

        raise ParseError(
            self.pos + 1,
            'Expected a different keyword for: %s',
            self.text[self.pos + 1],
        )
    
    def maybe_match(self, *rules):
        try:
            return self.match(*rules)
        except ParseError:
            return None

    def maybe_keyword(self, *keywords):
        try:
            return self.keyword(*keywords)
        except ParseError:
            return None

class ArabicParser(POSParser):
    # clean text with dediacritization
    def dediac(self, text):
        return dediac_ar(self.text)

    # ortho-normalize
    def ortho_normalize(self, text):
        text = normalize_alef_maksura_ar(text)
        text = normalize_alef_ar(text)
        text = normalize_teh_marbuta_ar(text)
        return text

    def start(self):
        self.text = self.dediac(self.text)
        self.text = self.ortho_normalize(self.text)
        self.text = self.text.split(' ')
        return self.match('sentence')

    def sentence(self):
        return self.match('nominal')

    def nominal(self):
        return dict(
                    partOfSpeech='nominal sentence', 
                    children=[self.match('subject'), self.match('predicate')]
        )

    # not processing verbal sentences yet
    def verbal(self):
        raise ParseError(
            self.pos+1, 
            'Cannot process verbal sentences yet %s',
            self.text[self.pos+1]
        )

    # a subject could be a noun+noun (i.e. morning flight) or
    # noun+adjective (i.e. new book, in arabic the adj is after the noun)
    # or any combo
    def subject(self):
        return dict(
                    partOfSpeech='subject',
                    children=[self.match('noun')]
        )  
    
    # pred can be (1) Singular Noun (2) Phrase (3) Sentence
    def predicate(self):
        return dict(
                    partOfSpeech='predicate',
                    children=[self.match('phrase', 'sentence', 'noun')]
        )

    def phrase(self):
        return self.match('PP', 'AP')
    
    # AP is adverbial phrase
    def AP(self):
        return dict(
                    partOfSpeech='adverbial phrase', 
                    children=[self.match('adverb'), self.match('noun')]
        )

    # PP is prepositional phrase
    def PP(self):
        return dict(
                    partOfSpeech='prepositional phrase', 
                    children=[self.match('preposition'), self.match('noun')]
        )
    
    # combining nouns and adjectives since they will be read similarly
    def noun(self):
        return self.keyword(self.nouns + self.adjs)

    def preposition(self):
        return self.keyword(self.prep)

    def adverb(self):
        return self.keyword(self.adv)