from collections import defaultdict, Counter

def read_file(file_name):
    input_file = open(file_name, 'r')
    sentences = list()
    sent = []
    lines = input_file.readlines()
    setnences = "".join(lines).split("\r\n\r\n")

    input_file.close()
    return sentences
if __name__ == "__main__":
    k = read_file("wikipedia.sample.trees.lemmatized")
    pass