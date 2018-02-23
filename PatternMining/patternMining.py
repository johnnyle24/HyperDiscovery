import nltk
import json

class PatternMining:

    def getPairs(self, tokenFile, corpusFile):
        f = open(tokenFile, 'rU')

        lines = f.readlines()

        mx = 0
        hashes = dict()
        for line in lines:
            entry = nltk.word_tokenize(line)[:-1]
            mx = max(len(entry), mx)
            hashes[tuple(entry)] = 0

        corpusLines = open(corpusFile, 'rU')

        patterns = dict()
        for line in corpusLines:
            self.getNgrams(line, hashes, patterns, mx)

        patterns = self.cleanJsonData(patterns)

        with open('patterns.txt', 'w') as outfile:
            json.dump(patterns, outfile, ensure_ascii=False)

        for key, val in patterns.items():
            print('Pattern: {0}'.format(key))
            print('values: {0}'.format(val))
            print()


    def getNgrams(self, line, hashes, patterns, n=3):
        line = line.split()

        last = None
        for wc, word in enumerate(line):
            nGram = list()
            for i in range(n):
                if wc + i < len(line):
                    nGram.append((line[wc + i]).lower())
                    tup = tuple(nGram)
                    if tup in hashes:
                        if last is not None:
                            if wc-i - last[1] < 4: # Must be close to the previous token found
                                pattern = ' '.join(line[last[1]: wc-i + 1])#[s.lower() for s in line[last[1]: wc-i + 1]]
                                if pattern not in patterns:
                                    patterns[pattern] = set()
                                patterns[pattern].add((last[0], tup))
                            last = None
                        last = (tup, wc + i + 1)
                        hashes[tuple(nGram)] += 1

    def cleanJsonData(self, data):
        result = dict()
        for k, v in data.items():
            result[k] = list(v)
        return result

if __name__ == '__main__':

    tokenFile = '../SemEval2018-Task9/training/data/2A.medical.training.data.txt'
    # corpusFile = '../Data/2A_med_pubmed_tokenized.txt'
    corpusFile = 'testCorpus.txt'

    PatternMining().getPairs(tokenFile, corpusFile)