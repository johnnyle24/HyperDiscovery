import nltk
import json
import heapq


class PatternMining:
    def getPairs(self, tokenFile, corpusFile, outputFile='patterns.json'):
        """
        Get patterns of every matched pair from tokenFile in the corpusFile
        :param tokenFile: Name of the tokens file
        :param corpusFile: Name of the corpus file
        :param outputFile: Name of the output file to write the result to
        :return:
        """

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

        orderedPatterns = self.sortPatterns(patterns)

        with open(outputFile, 'w') as outfile:
            json.dump(orderedPatterns, outfile, ensure_ascii=False)

    def getSentencePattern(self, sent, hashes, patterns, maxn=3, closeness=3):
        """
        Extracts patterns out of the sentence

        :param sent: Corpus line
        :param hashes: The hashes of the data entries
        :param patterns: Dictionary container to store the found patterns
        :param maxn: Max number of tokens in a data entry
        :param closeness: How close two tokens need to be to be considered
        :return:
        """
        line = sent.split()

        last = None
        for wc, word in enumerate(line):
            nGram = list()
            for i in range(maxn):
                if wc + i < len(line):
                    nGram.append((line[wc + i]).lower())
                    tup = tuple(nGram)
                    if tup in hashes:
                        if last is not None:
                            if wc - i - last[1] <= 3:  # Must be close to the previous token found 3 away in this case
                                pattern = self.getPattern(last[1], wc - i + 1, line)
                                self.addPattern(pattern, patterns)
                            last = None
                        last = (tup, wc + i + 1)

    def getPattern(self, lower, upper, lst):
        """
        Returns the pattern between lower and upper in string format
        :param lower:
        :param upper:
        :param lst:
        :return: pattern in string format
        """
        return ' '.join([s.lower() for s in lst[lower: upper]])

    def addPattern(self, pattern, patterns):
        """
        Helper method to add the pattern to the patterns container
        :param pattern:
        :param patterns:
        :return:
        """
        if pattern not in patterns:
            patterns[pattern] = 0
        patterns[pattern] += 1

    def sortPatterns(self, patterns):
        """
        Sorts patterns based on the frequency
        :param patterns:
        :return:
        """
        q = []
        for k, v in patterns.items():
            heapq.heappush(q, (v, k))

        ordered = list()
        while q:
            ordered.insert(0, heapq.heappop(q))

    def jsonToOurFormat(self, filename, outputFile):
        """
        Transforms json format: <pattern> = <frequency>
        :param filename:
        :param outputFile:
        :return:
        """
        data = json.load(open(filename))
        with open(outputFile, 'w') as file:
            for l in data:
                file.write('{0} = {1}\n'.format(l[1], l[0]))


if __name__ == '__main__':
    tokenFile = '../SemEval2018-Task9/training/data/2A.medical.training.data.txt'
    corpusFile = '../Data/2A_med_pubmed_tokenized.txt'
    # corpusFile = 'testCorpus.txt'

    pm = PatternMining()

    pm.getPairs(tokenFile, corpusFile, 'test.json')
    pm.jsonToOurFormat('patterns.json', 'patterns.txt')
