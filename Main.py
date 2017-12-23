import gc

from Strategy import *
import sys
from collections import defaultdict, Counter
import numpy as np

MIN_OCCURRENCES = 100
CONTEXT_MIN_OCCURRENCES = 200

TARGET_WORDS = ["car", "bus", "hospital", "hotel", "gun", "bomb", "horse", "fox", "table", "bowl", "guitar", "piano"]


def clean_dictionary(words_dict, context_dict, syntactic_window = False):
    before = 1.*sum([sum(words_dict[c].itervalues()) for c in words_dict])
    print "len before: ", before
    for w, context in words_dict.iteritems():
        cpy = Counter(words_dict[w])
        for c in context:
            if context_dict[c] < CONTEXT_MIN_OCCURRENCES:
                del cpy[c]

            elif syntactic_window: #if it's a syntactic dependency

                word = c.split("*-")[0].strip()

                if lemma_count[word] < CONTEXT_MIN_OCCURRENCES:
                    del cpy[c]

        words_dict[w] = cpy

    after = 1. * sum([sum(words_dict[c].itervalues()) for c in words_dict])
    print "len after: ", after
    print "fraction: ", after/before

    return words_dict

def read_file(file_name):
    with open(file_name, "r") as f:
        lines = f.readlines()

        lines = [line.replace("\r\n", "") for line in lines]
        sentences, sentence = [], []

        for line in lines:
            if len(line) > 0:  # a sentence ends with an empty line.
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
            lemma_count[lemma] += 1

    return lemma_count


def create_dictionary(sentences, strategy, frequent_lemmas):
    word_counts = defaultdict(Counter)
    context_counts = Counter()

    for s in sentences:
        words, context = strategy.get_context(s)

        for (w, c) in zip(words, context):

            if w not in frequent_lemmas: continue  # filter rare words.

            context_counts_for_word = word_counts[w]

            for context_word in c:

                #if context_word not in frequent_lemmas: continue

                context_counts_for_word[context_word] += 1
                context_counts[context_word]+=1

    print "Voc size: ", len(word_counts)
    return word_counts, context_counts


def calculate_PMI(x, y, counts, context_counts, total_num_of_pairs):
    p_x = sum(counts[x].itervalues()) / total_num_of_pairs
    p_y = context_counts[y] / total_num_of_pairs
    p_x_y = (counts[x][y]) / total_num_of_pairs

    # print (x, y), (p_x, p_y), (x in counts, y in counts)
    # print len (counts[x])
    # print len(counts[y])
    # print "===================================================="
    return max(np.log(p_x_y / (p_x * p_y)), 0.)


def get_vector(w, counts, context_counts, frequent_lemmas, word2key, total_num_pairs):
    # v = np.zeros(len(lemma_count))
    v = {}
    for i, w2 in enumerate(counts[w].iterkeys()):

        #if w2 not in frequent_lemmas: continue

        PMI = calculate_PMI(w, w2, counts, context_counts, total_num_pairs)
        if PMI > 1e-7:
            v[w2] = PMI

    return v


def get_matrix(counts,context_counts, frequent_lemmas, word2key):
    l = len(frequent_lemmas)
    m = [None] * l
    total_num_pairs = 1. * sum([sum(counts[c].itervalues()) for c in counts])

    for i, w in enumerate(frequent_lemmas):
        if i % 100 == 0:
            print "{}/{}".format(i, l)
        m[word2key[w]] = get_vector(w, counts,context_counts, frequent_lemmas, word2key, total_num_pairs)

    return m


def get_attributes_words_matrix(word_attribute_mat):
    attribute_words_mat = {}
    for i, attirbutes in enumerate(word_attribute_mat):
        for att in attirbutes:
            if att not in attribute_words_mat:
                attribute_words_mat[att] = list()
            attribute_words_mat[att].append((i, attirbutes[att]))
    return attribute_words_mat


def word_similaraties(key2word, word_attribute_mat, attribute_word_mat, word_index):
    word_attributes = word_attribute_mat[word_index]
    num_of_words = len(key2word)
    similarity_mat = [0] * num_of_words
    for att in word_attributes:
        for v in attribute_word_mat[att]:
            similarity_mat[v[0]] += word_attributes[att] * word_attribute_mat[v[0]][att]

    u_side = 0.0
    for att in word_attributes:
        u_side += word_attributes[att] * word_attributes[att]

    for i in range(num_of_words):
        v_attributes = word_attribute_mat[i]
        v_side = 0.0
        for att in v_attributes:
            v_side += v_attributes[att] * v_attributes[att]
        similarity_mat[i] /= np.sqrt(u_side * v_side)
    return similarity_mat


if __name__ == "__main__":
    sentences = read_file("wikipedia.sample.trees.lemmatized")
    lemma_count = get_word_count(sentences)
    print "test: ", lemma_count["confederate_states_of_america"]
    frequent_lemmas = set(filter(lambda lemma: lemma_count[lemma] > MIN_OCCURRENCES and lemma not in FUNCTION_WORDS,
                                 lemma_count.iterkeys()))
    k = 20

    key2word = np.array([w for w in sorted(frequent_lemmas)])
    word2key = {w: i for i, w in enumerate(sorted(frequent_lemmas))}
    #DependecyContextWord()
    strategies = [DependecyContextWord(), CoContextWord(), WindowContextWord()]
    for strategy in strategies:
        dict, context_dict = create_dictionary(sentences, strategy, frequent_lemmas)
        clean_dictionary(dict, context_dict, isinstance(strategy, DependecyContextWord))
        print "bulding matrix..."
        m = get_matrix(dict, context_dict, frequent_lemmas, word2key)
        mt = get_attributes_words_matrix(m)
        for word in TARGET_WORDS:
            similar_words = np.array(word_similaraties(key2word, m, mt, word2key[word]))
            most_similar = similar_words.argsort()[-1:-k:-1]
            print key2word[most_similar]
            print "======"
        print "==================================="
        del dict
        del m
        del mt
        del similar_words, most_similar
        gc.collect()


    """
    k = 5
    strategy = WindowContextWord()
    dict = create_dictionary(sentences, strategy, frequent_lemmas)
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
    del dict
    gc.collect()
    strategy = CoContextWord()
    dict = create_dictionary(sentences, strategy, frequent_lemmas)
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


    # print calculate_PMI("dog", "cat", dict)
    # print calculate_PMI("england", "france", dict)
    # print calculate_PMI("wine", "grape", dict)
    # print calculate_PMI("computer", "television", dict)
    # print calculate_PMI("england", "television", dict)
    # print calculate_PMI("dog", "john", dict)
    """

    # v  = m[0]
    # for (key, count) in v.iteritems():
    #     print (key2word[key], count)
    # print key2word[0]
