import gc
import numpy as np
import sys
import pandas as pd
from Main import TARGET_WORDS


def most_similar(word, k):
    global word2key
    global key2word
    word = vecs[word2key[word]]  # get the dog vector
    sims = vecs.dot(word)  # compute similarities
    most_similar_ids = sims.argsort()[-2:-k - 2:-1]
    return key2word[most_similar_ids]


if __name__ == '__main__':
    data = pd.read_csv(sys.argv[1], sep=' ', header=None).get_values()
    key2word = np.array([row[0] for row in data])
    word2key = {w: i for i, w in enumerate(key2word)}

    vecs = [row[1:].astype(np.float32) for row in data]
    del data
    gc.collect()

    vecs_norm = np.linalg.norm(vecs, axis=1)
    vecs_norm.shape = (vecs_norm.shape[0], 1)
    vecs /= vecs_norm
    for word in TARGET_WORDS:
        print most_similar(word, 20)
