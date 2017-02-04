import re
import json
import pickle
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.chunk import named_entity

def make_pickle(o, p):
    save = open(p,"wb")
    pickle.dump(o, save)
    save.close()

def load_pickle(p):
	return pickle.load(open(p, "rb"))


def save_file(dl, fp):
    with open(fp, 'w') as of:  
            json.dump(dl, of,indent=None, separators=(',', ': '))
            print("Saved %s" %of.name)

def clean_n_tokenize(s):
	tknzr = TweetTokenizer()
	#stopwords and stemmer
	stop_words = list(set(stopwords.words('english')))
	lemmatizer = nltk.WordNetLemmatizer()

	noise_words = ['&amp;', 'rt', 'RT',"https","http",'\\', '//', '"', "'", ")", "("]
	noise_punc = [ "''", '""', '/', ",", "?", "-", ":", '"', "&", "?", "_"]

	URL_REGEX = r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?<>""'']))"""
	clean_text = re.sub(URL_REGEX, '', s, flags=re.MULTILINE)
	clean_text = ' '.join([i.strip("...").lower() for i in tknzr.tokenize(clean_text) if i not in noise_words])
	tokens = [lemmatizer.lemmatize(i) for i in tknzr.tokenize(clean_text) if i not in noise_punc+stop_words]

	return (clean_text,tokens)

def get_hashs_n_mentions(t):
	return ([i for i in t if i.startswith("#")], [i for i in t if i.startswith("@")])

def get_pos(t):
	return named_entity.pos_tag(t) 

def calculate_word_freq(words):
	r = {}
	for w in words.split():
		if not r.get(w):
			r[w] = words.count(w)
	return r
		

