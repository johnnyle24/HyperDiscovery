import nltk

def read_in_chunks(file_object, chunk_size=1024):
    """
    Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k.
    """
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def pos(sentence):
    tokenized = nltk.word_tokenize(sentence)

    taggedSent = nltk.pos_tag(tokenized)
    grammar = 'NP: {<DT>?<JJ>*<NNS>*<NN>*(<NNS>|<NN>)+}'
    cp = nltk.RegexpParser(grammar)
    result = cp.parse(taggedSent)
    return result

def write(sentence, filename = 'testfile.txt'):
    with open(filename, 'w') as file:
        file.write(str(sentence))

if __name__ == '__main__':
    corpus = '../Data/2B_music_bioreviews_tokenized.txt'
    # corpus = '../Data/2A_med_pubmed_tokenized.txt'
    # corpus = '../Data/musc/2B_music_bioreviews_2.txt'
    # corpus = '../Data/2A_med_pubmed_tokenized.txt'#sys.argv[1]

    f=open(corpus,'rU')

    for chunk in read_in_chunks(f, 1000000):
        write(pos(chunk))