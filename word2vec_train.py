import codecs
import glob
import logging
import multiprocessing
import os
import pprint
import re
import nltk
import gensim.models.word2vec as w2v

nltk.download("punkt")
nltk.download("stopwords")

from nltk.corpus import stopwords

data_files = sorted(glob.glob("data/*.txt"))

print("Found Files:", data_files)

corpus_raw = u""

for data_file in data_files:
    print("Reading '{0}'...".format(data_file))
    with codecs.open(data_file, "r", "utf-8") as d_file:
        corpus_raw += d_file.read()
    print("Corpus is now {0} characters long".format(len(corpus_raw)))

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
raw_sentences = tokenizer.tokenize(corpus_raw)


def sentence_to_wordlist(raw):
	noise_words = ["RT", "rt", "amp"]
	stop_words = list(set(stopwords.words('english')))
	URL_REGEX = r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?<>""'']))"""
	raw = re.sub(URL_REGEX, '', raw, flags=re.MULTILINE)
	for n in noise_words:
		clean = raw.replace(n, " ")
	clean = re.sub("[^a-zA-Z]"," ", raw)
	words = clean.split()
	stop_words = list(set(stopwords.words('english')))
	words = [w for w in words if w not in stop_words]
	return words

sentences = []

for raw_sentence in raw_sentences:
    if len(raw_sentence) > 0:
        sentences.append(sentence_to_wordlist(raw_sentence))


# print(raw_sentences[:5])
# print(sentence_to_wordlist(raw_sentences[5]))


token_count = sum([len(sentence) for sentence in sentences])
print("The book corpus contains {0:,} tokens".format(token_count))




#model

# Dimensionality of the resulting word vectors.
#more dimensions mean more traiig them, but more generalized
num_features = 300
# Minimum word count threshold.
min_word_count = 3
# Number of threads to run in parallel.
num_workers = multiprocessing.cpu_count()
# Context window length.
context_size = 7
# Downsample setting for frequent words.
#rate 0 and 1e-5 
#how often to use
downsampling = 1e-3
# Seed for the RNG, to make the results reproducible.
seed = 1



tweets_vec = w2v.Word2Vec(
    sg=1,
    seed=seed,
    workers=num_workers,
    size=num_features,
    min_count=min_word_count,
    window=context_size,
    sample=downsampling,
    train_count = 5
)

tweets_vec.build_vocab(sentences)

print("Word2Vec vocabulary length:", len(tweets_vec.vocab))

tweets_vec.train(sentences)

if not os.path.exists("trained"):
    os.makedirs("trained")


tweets_vec.save(os.path.join("trained", "electionTweets.w2v"))