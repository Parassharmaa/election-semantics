import codecs
import glob
import logging
import multiprocessing
import os
import pprint
import re
import nltk
import gensim.models.word2vec as w2v
import sklearn.manifold
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns



election2vec = w2v.Word2Vec.load(os.path.join("trained", "electionTweets.w2v"))

tsne = sklearn.manifold.TSNE(n_components=2, random_state=0)

all_word_vectors_matrix = election2vec.syn0

all_word_vectors_matrix_2d = tsne.fit_transform(all_word_vectors_matrix)

points = pd.DataFrame(
    [
        (word, coords[0], coords[1])
        for word, coords in [
            (word, all_word_vectors_matrix_2d[election2vec.vocab[word].index])
            for word in election2vec.vocab
        ]
    ],
    columns=["word", "x", "y"]
)


print(points.head(10))




sns.set_context("poster")

points.plot.scatter("x", "y", s=10, figsize=(20, 12))
sns.plt.show()


def plot_region(x_bounds, y_bounds):
    slice = points[
        (x_bounds[0] <= points.x) &
        (points.x <= x_bounds[1]) & 
        (y_bounds[0] <= points.y) &
        (points.y <= y_bounds[1])
    ]
    
    ax = slice.plot.scatter("x", "y", s=35, figsize=(10, 8))
    for i, point in slice.iterrows():
        ax.text(point.x + 0.005, point.y + 0.005, point.word, fontsize=11)

    ax.show()


election2vec.most_similar("modi")

election2vec.most_similar("Aap")

election2vec.most_similar("Kejriwal")


def nearest_similarity_cosmul(start1, end1, end2):
    similarities = election2vec.most_similar_cosmul(
        positive=[end2, start1],
        negative=[end1]
    )
    start2 = similarities[0][0]
    print("{start1} is related to {end1}, as {start2} is related to {end2}".format(**locals()))
    return start2

nearest_similarity_cosmul("BJP", "Aap", "Congress")
nearest_similarity_cosmul("Modi", "Kejriwal", "Rahul")
nearest_similarity_cosmul("Sikh", "Akali", "Aap")

