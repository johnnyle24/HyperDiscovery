import sys
import nltk
from nltk.chunk import conlltags2tree, tree2conlltags

class PatternMining:

    def __init__(self, tokensFilename, corpusFilename):
        self.tokensFilename = tokensFilename
        self.corpusFilename = corpusFilename
        self.corpusTokenized = list()
        pass

    # def getTokenizedCorpus(self):
    #     if len(self.corpusTokenized) == 0:
    #         corpus = ''
    #         with open(self.corpusFilename, 'r') as file:
    #             for line in file:
    #                 # corpus += line.lower()
    #                 # self.corpusTokenized.extend()
    #                 tokens_list = nltk.word_tokenize(line.lower())
    #
    #                 self.extractPattern()
    #     return self.corpusTokenized

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
        pattern = ''
        for t in range(len(tokens_list)):
            if tokens_list[t] == token:
                for p in range(t-n, t):
                    print('{0} '.format(tokens_list[p]), end='')
                    pattern += '{0} '.format(tokens_list[p])
                print(token)
                resList.add(pattern)
                pattern = ''
        return resList

if __name__ == '__main__':
    tokens = 'endodontics'#sys.argv[0]
    corpus = '../SemEval2018-Task9/2A_med_pubmed_tokenized.txt'#sys.argv[1]
    # corpus = 'testCorpus.txt'#sys.argv[1]

    pm = PatternMining(tokens, corpus)
    patterns = pm.extractPatternOnFly(tokens, extract=False)

