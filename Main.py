from Strategy import *
import sys
from collections import defaultdict, Counter
import numpy as np

MIN_OCCURRENCES = 100

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

def create_dictionary(sentences, strategy, frequent_lemmas):

    counts = defaultdict(Counter)

    for s in sentences:
        words, context = strategy.get_context(s)

        for (w,c) in zip(words, context):

            if w not in frequent_lemmas: continue #filter rare words.

            context_counts_for_word = counts[w]

            for context_word in c:

                 if context_word not in frequent_lemmas: continue

                 context_counts_for_word[context_word] += 1

    print "Voc size: ", len(counts)
    return counts

def calculate_PMI(x, y, counts, total_num_of_pairs):
    p_x = sum(counts[x].itervalues())/total_num_of_pairs
    p_y =  sum(counts[y].itervalues())/total_num_of_pairs
    p_x_y = (counts[x][y])/total_num_of_pairs

    # print (x, y), (p_x, p_y), (x in counts, y in counts)
    # print len (counts[x])
    # print len(counts[y])
    # print "===================================================="
    return max(np.log(p_x_y/(p_x*p_y)), 0.)

def get_vector(w, counts, frequent_lemmas, word2key, total_num_pairs):
    #v = np.zeros(len(lemma_count))
    v = []
    for i, w2 in enumerate(counts[w].iterkeys()):

        if w2 not in frequent_lemmas: continue

        PMI = calculate_PMI(w,w2,counts, total_num_pairs)
        if PMI>1e-7:
            v.append((word2key[w2], PMI) )

    return v

def get_matrix(counts, frequent_lemmas, word2key):

    l = len(frequent_lemmas)
    m = [None]*l
    total_num_pairs = 1.*sum( [sum(counts[c].itervalues()) for c in counts]    )

    for i, w in enumerate(frequent_lemmas):
        if i%100 == 0:
            print "{}/{}".format(i,l)
        m[word2key[w]] = get_vector(w, counts, frequent_lemmas, word2key, total_num_pairs)

    return m

if __name__ == "__main__":

    sentences = read_file("wikipedia.sample.trees.lemmatized")
    lemma_count = get_word_count(sentences)

    frequent_lemmas = set(filter(lambda lemma: lemma_count[lemma]>MIN_OCCURRENCES and lemma not in FUNCTION_WORDS, lemma_count.iterkeys() ))

    key2word = {i:w for i,w in enumerate(sorted(frequent_lemmas))   }
    word2key = {w:i for i,w in enumerate(sorted(frequent_lemmas))   }

    strategy = WindowContextWord()
    dict = create_dictionary(sentences, strategy, frequent_lemmas)
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
    print "bulding matrix..."
    m = get_matrix(dict, frequent_lemmas, word2key)
    # v  = m[0]
    # for (key, count) in v.iteritems():
    #     print (key2word[key], count)
    # print key2word[0]
