import nltk
import json
import heapq

class PatternMining:

    def getPairs(self, tokenFile, corpusFile, outputFile='patterns.json'):
        f = open(tokenFile, 'rU')

        lines = f.readlines()

        mx = 0
        hashes = set()
        for line in lines:
            entry = nltk.word_tokenize(line)[:-1]
            mx = max(len(entry), mx)
            hashes.add(tuple(entry))

        corpusLines = open(corpusFile, 'rU')

        patterns = dict()
        for line in corpusLines:
            self.getSentencePattern(line, hashes, patterns, mx)


        q = []
        for k, v in patterns.items():
            heapq.heappush(q, (v, k))

        ordered = list()
        while q:
            ordered.insert(0, heapq.heappop(q))


        with open(outputFile, 'w') as outfile:
            json.dump(ordered, outfile, ensure_ascii=False)

        # for key, val in patterns.items():
        #     print('Pattern: {0}'.format(key))
        #     print('values: {0}'.format(val))
        #     print()


    def getSentencePattern(self, line, hashes, patterns, n=3):
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
                            if wc-i - last[1] < 4: # Must be close to the previous token found 3 away in this case
                                pattern = self.getPattern(last[1], wc-i + 1, line)
                                self.addPattern(pattern, patterns)
                            last = None
                        last = (tup, wc + i + 1)

    def getPattern(self, lower, upper, lst):
        return ' '.join([s.lower() for s in lst[lower : upper]])

    def addPattern(self, pattern, patterns):
        if pattern not in patterns:
            patterns[pattern] = 0
        patterns[pattern] += 1

    def cleanJsonData(self, data):
        result = dict()
        for k, v in data.items():
            result[k] = list(v)
        return result

    def jsonToOurFormat(self, filename, outputFile):
        data = json.load(open(filename))
        with open(outputFile, 'w') as file:
            for l in data:
                file.write('{0} = {1}\n'.format(l[1], l[0]))




if __name__ == '__main__':

    tokenFile = '../SemEval2018-Task9/training/data/2A.medical.training.data.txt'
    corpusFile = '../Data/2A_med_pubmed_tokenized.txt'
    # corpusFile = 'testCorpus.txt'

    pm = PatternMining()

    # pm.getPairs(tokenFile, corpusFile, 'test.json')

    pm.jsonToOurFormat('patterns.json', 'patterns.txt')