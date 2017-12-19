from Strategy import *
import sys
from collections import defaultdict, Counter

def read_file(file_name):

    with open(file_name, "r") as f :
        lines = f.readlines()
        print ("size: ", sys.getsizeof(lines) / 1e6)
        print ("length: ", len(lines))
        print ("last: ", lines[-2])

        lines = [line.replace("\r\n", "") for line in lines]
        sentences, sentence = [], []

        for line in lines:
            #print line
            if len(line) > 0:
                sentence.append(line)
            else:
                sentences.append(sentence)
                sentence = []

        return sentences


if __name__ == "__main__":
    sentences = read_file("wikipedia.sample.trees.lemmatized")
    print ("size of sentences:", sys.getsizeof(sentences)/1e6)
    print (len(sentences))
    s = WindowContextWord()
    words, context = s.get_context(sentences[0])
