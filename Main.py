from Strategy import *
import sys
from collections import defaultdict, Counter
import numpy as np


def read_file(file_name):

    with open(file_name, "r") as f :
        lines = f.readlines()

        lines = [line.replace("\r\n", "") for line in lines]
        sentences, sentence = [], []

        for line in lines:

            if len(line) > 0: #a sentence ends with an empty line.
                sentence.append(line)

            else:
                sentences.append(sentence)
                sentence = []

        return sentences

def get_word_count(sentences):

    lemma_count = Counter()

    for s in sentences:
        for w in s:
            lemma = w.split('\t')[2]
            lemma_count[lemma]+=1

    return lemma_count

def create_dictionary(sentences, strategy):

    counts = defaultdict(Counter)

    for s in sentences:
        words, context = strategy.get_context(s)

        for (w,c) in zip(words, context):

            if lemma_count[w] < 100: continue #filter rare words.

            context_counts_for_word = counts[w]

            for context_word in c:
                 context_counts_for_word[context_word] += 1

    print "Voc size: ", len(counts)
    return counts

def calculate_PMI(x, y, counts):

    total_num_pairs = sum( [sum(counts[c].values()) for c in counts]    )
    p_x = sum(counts[x].values())/(1.*total_num_pairs)
    p_y =  sum(counts[y].values())/(1.*total_num_pairs)
    p_x_y = (counts[x][y])/(1.*total_num_pairs)

    return max(np.log(p_x_y/(p_x*p_y)), 0)

def get_vector(w, counts, lemma_count):
    v = np.zeros(len(lemma_count))

    for i, w2 in enumerate(sorted(lemma_count)):

        PMI = calculate_PMI(w,w2,counts)
        v[i] = PMI

    return v

def get_matrix(counts, lemma_count):

    l = len(lemma_count)
    m = np.zeros(l, l)

    for i, w in enumerate(sorted(lemma_count)):
        m[i] = get_vector(w, counts, lemma_count)

    return m

if __name__ == "__main__":

    sentences = read_file("wikipedia.sample.trees.lemmatized")
    lemma_count = get_word_count(sentences)


    strategy = WindowContextWord()
    dict = create_dictionary(sentences, strategy)
    k = 5
    print dict['dog'].most_common(k)
    print "================="
    print dict['cat'].most_common(k)
    print "================="
    print dict['john'].most_common(k)
    print "================="
    print dict['wine'].most_common(k)
    print "================="
    print dict['phone'].most_common(k)
    print "================="
    print dict['england'].most_common(k)
    print "================="

    print "==================================================="
    strategy = CoContextWord()
    dict = create_dictionary(sentences, strategy)
    print dict['dog'].most_common(k)
    print "================="
    print dict['cat'].most_common(k)
    print "================="
    print dict['john'].most_common(k)
    print "================="
    print dict['wine'].most_common(k)
    print "================="
    print dict['phone'].most_common(k)
    print "================="
    print dict['england'].most_common(k)
    print "================="

    print calculate_PMI("dog", "cat", dict)
    m = get_matrix(dict, lemma_count)
    print m.shape