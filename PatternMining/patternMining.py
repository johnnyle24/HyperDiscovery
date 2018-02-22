import sys
import nltk
from nltk.chunk import conlltags2tree, tree2conlltags

class PatternMining:

    def __init__(self, tokensFilename, corpusFilename):
        self.tokensFilename = tokensFilename
        self.corpusFilename = corpusFilename
        self.corpusTokenized = list()

    def extractPatternOnFly(self, token, extract=True):

        tokens = set()
        if extract:
            with open(self.corpusFilename, 'r') as file:
                for line in file:
                    # tokens_list = nltk.word_tokenize(line.lower())
                    pattern = self.extractPattern(token, line.lower().split(' '))
                    if pattern != '' and pattern not in tokens:
                        tokens.update(pattern)
        else:
            with open('patterns.txt', 'r') as file:
                for line in file:
                    tokens.add(line.replace('\n', ''))
        return tokens


    def extractPattern(self, token, tokens_list, n=3):
        resList = set()
        pattern = list()
        for t in range(len(tokens_list)):
            if tokens_list[t] == token:

                for p in range(t+1, t+n+1):
                    if p < len(tokens_list):
                        pattern.append('{0}'.format(tokens_list[p].strip()))
                    else:
                        pattern.append('omega')

                print(pattern)
                resList.add(tuple(pattern))
                pattern = list()
        return resList

if __name__ == '__main__':
    tokens = 'endodontics'#sys.argv[0]
    corpus = '../SemEval2018-Task9/2A_med_pubmed_tokenized.txt'#sys.argv[1]
    # corpus = 'testCorpus.txt'#sys.argv[1]

    pm = PatternMining(tokens, corpus)
    patterns = pm.extractPatternOnFly(tokens, extract=True)

    with open('patterns.txt', 'w') as file:
        for pattern in patterns:
            file.write('{0}\n'.format(pattern))

    print('*'*50)

    # To check if other hypernyms exist with same patterns fournd for endodontics
    # n = 3
    # tokens = list()
    # with open(corpus, 'r') as file:
    #     for line in file:
    #         tokens_list = line.split(' ')
    #
    #         threeGrams = nltk.ngrams(line.split(), n)
    #
    #         for gram in threeGrams:
    #
    #             if gram in patterns:
    #                 print(gram)