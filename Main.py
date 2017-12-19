from Strategy import *
import sys
from collections import defaultdict, Counter



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

def create_dictionary(sentences, strategy):

    counts = defaultdict(Counter)

    for s in sentences:
        words, context = strategy.get_context(s)

        for (w,c) in zip(words, context):

            context_counts_for_word = counts[w]

            for context_word in c:
                 context_counts_for_word[context_word] += 1

    return counts

if __name__ == "__main__":
    sentences = read_file("wikipedia.sample.trees.lemmatized")
    strategy = WindowContextWord()
    dict = create_dictionary(sentences, strategy)
    print dict['dog'].most_common(10)
    print "================="
    print dict['cat'].most_common(10)
    print "================="
    print dict['john'].most_common(10)
    print "================="
    print dict['see'].most_common(10)
    print "================="
    print dict['walk'].most_common(10)

    print "==================================================="
    strategy = CoContextWord()
    dict = create_dictionary(sentences, strategy)
    print dict['dog'].most_common(10)
    print "================="
    print dict['cat'].most_common(10)
    print "================="
    print dict['john'].most_common(10)
    print "================="
    print dict['see'].most_common(10)
    print "================="
    print dict['walk'].most_common(10)