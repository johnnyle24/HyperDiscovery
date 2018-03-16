import nltk
import os
import json

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

def corpusDirectoryExist(head, dirname):
    fullPath = os.path.join(head, dirname)
    if not os.path.isdir(fullPath):
        os.mkdir(os.path.join(head, dirname))

    return fullPath

def writeToJsonFile(data, outputFile):
    with open(outputFile, 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False)


if __name__ == '__main__':
    # corpus = '../Data/2B_music_bioreviews_tokenized.txt'
    # corpus = '../Data/2A_med_pubmed_tokenized.txt'
    # corpus = '../Data/musc/2B_music_bioreviews_2.txt'
    # corpus = '../Data/2A_med_pubmed_tokenized.txt'#sys.argv[1]

    corpuses = ['../Data/2B_music_bioreviews_tokenized.txt', '../Data/2A_med_pubmed_tokenized.txt']
    corpuses = ['../Data/2A_med_pubmed_tokenized.txt']
    corpuses = ['../Data/Data/2B_music_bioreviews_tokenized.txt']

    for corpus in corpuses:

        head, tail = os.path.split(corpus)
        f = ''
        try:
            f=open(corpus,'rU')
        except:
            continue

        filename, ext = os.path.splitext(tail)
        head = corpusDirectoryExist(head, filename)


        for i, chunk in enumerate(read_in_chunks(f, 1000000)):
            if i == i:
                newFilename = os.path.join(head, '{0}_{1}.txt'.format(filename, i))
                # pm.writeToJsonFile(pos(chunk), 'posChunk.json')
                # write(pos(chunk), filename=newFilename)
                print('Processing {0}'.format(newFilename))
                writeToJsonFile(pos(chunk), newFilename)
                print('Finished Processing {0}'.format(newFilename))
