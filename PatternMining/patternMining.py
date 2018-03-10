import nltk
import json
import heapq
from operator import itemgetter


def writeToJsonFile(data, outputFile):
    with open(outputFile, 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False)


def readJsonFile(filename):
    return json.load(open(filename))

class Item:
    def __init__(self, pattern):
        self.pattern = list()
        self.pattern = pattern

class PatternMining:

    def __init__(self, filename):
        self.VALID_POS_TAGS = ['DT', 'JJ', 'NN', 'NNS']
        self.data = None
        self.data = readJsonFile(filename)

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

        self.writeToJsonFile(orderedPatterns, outputFile)

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
                            if wc - i - last[
                                1] <= closeness:  # Must be close to the previous token found 3 away in this case
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
        return ordered

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

    def pos(self, sent):
        tokenized = nltk.word_tokenize(sent)
        taggedSent = nltk.pos_tag(tokenized)
        grammar = 'NP: {<DT>?<JJ>*<NNS>*<NN>*(<NNS>|<NN>)+}'
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(taggedSent)
        return result

    def isList(self, items):
        if isinstance(items, list):
            for item in items:
                if isinstance(item, list):
                    return True
        return False

    def isNounPhrase(self, items):
        return self.isList(items)

    def hypeIsValid(self, hypernymToken):
        if hypernymToken[0].isalpha():
            for validToken in self.VALID_POS_TAGS:
                if hypernymToken[1] != validToken:
                    return False
        return True

    def getHypernim(self, i, data):
        for j in range(i, 0, -1):
            item = data[j]
            if self.isList(item):
                return item
        return None

    def getHyponim(self, i, data):
        for j in range(i, len(data)):
            item = data[j]

            if self.isList(item):
                return item
        return None

    def getNNS(self, item):
        str = ''
        for i in item:
            if i[1] == 'NN' or i[1] == 'NNS':
                str += i[0] + ' '
        return str

    def isPatternMatch(self, items, patterns):

        for pattern in patterns:
            l = len(pattern)

            #asd += [item for item in items]
            # lst = ' '.join(map(str, items))
            # 2 3
            t = tuple(items[:l])

            if pattern == t:
                return True
            # for i in range(len(items)):
            #     if len(items) != len(patterns):
            #         continue
            #
            #     if items[i].lower() == patterns[i].lower():
            #         return True
        return False


    def getHyperHypo(self, patterns):
        maxLen = 0
        for p in patterns:
            maxLen = max(maxLen, len(p))

        data = self.data

        tups = set()
        for i, item in enumerate(self.data[:-maxLen]):

            items = [ self.data[j][0] for j in range(i, i+maxLen)]

            if not self.isNounPhrase(items):
                if self.isPatternMatch(items, patterns):
                    item = self.getHypernim(i - 1, self.data)
                    item4 = self.getHyponim(i + maxLen, self.data)
                    print('{0} -> {1} '.format(item, item4))

                    nn1 = self.getNNS(item)
                    nn2 = self.getNNS(item4)

                    print('{0} -> {1}'.format(nn1, nn2))
                    print()

                    tups.add((nn1.strip(), nn2.strip()))
        return tups

    def getHypernimOfConcept(self, concept, patterns):
        maxLen = 0
        for p in patterns:
            maxLen = max(maxLen, len(p))

        data = self.data

        tups = set()
        for i, item in enumerate(self.data[:-maxLen]):

            items = [ self.data[j][0] for j in range(i, i+maxLen)]

            if not self.isNounPhrase(items):
                if self.isPatternMatch(items, patterns):
                    item = self.getHypernim(i - 1, self.data)
                    hyponim = self.getHyponim(i + maxLen, self.data)
                    # print('{0} -> {1} '.format(item, hyponim))

                    nn1 = self.getNNS(item)
                    nn2 = self.getNNS(hyponim)

                    if concept in hyponim:
                        print('Hypernim: {0}'.format(item))

                    # print('{0} -> {1}'.format(nn1, nn2))
                    # print()

                    tups.add((nn1.strip(), nn2.strip()))
        return tups



    def extractPattern(self, i):

        pattern = []
        count = 0
        for j in range(i, len(self.data)):

            if count >= 4:
                return -1, None

            p = self.data[j][0]
            if self.isList([p]):
                pattern.append(p)
                return self.data[j], pattern

            pattern.append(self.data[j])
            count += 1
        return -1, None

    def createTupleValue(self, item):
        one = ''
        for i in item:
            one += i[0] + ' '
        return one.strip()

    def tupleContains(self, item, tuples):
        for tup in tuples:
            if tup[0] == item:
                return tup
        return None

    def getPatterns(self, tups):

        patterns = dict()
        for it in range(len(self.data)):
            item = self.data[it]
            if self.isNounPhrase([item[0]]):
                tup = self.tupleContains(self.createTupleValue(item), tups)
                if tup is not None:
                    next, pattern = self.extractPattern(it + 1)
                    if pattern is not None and self.tupleContains(self.createTupleValue(next), tups) is not None:
                        prt = ''
                        for p in pattern:
                            if p[1].isalpha():
                                prt += p[0] + ' '
                        print(tup[0] + ',' + tup[1] + '->' + prt)
                        if prt.lower() not in patterns:
                            patterns[prt.lower()] = 0
                        patterns[prt.lower()] += 1
        return patterns


def formatTuples(tuples):
    s = set()
    for t in tuples:
        newTup = tuple
        s.add(tuple(t[1].split()))
        # for sa in strArr:
        #     newTup += sa
        # s.add(newTup)
    return s

if __name__ == '__main__':
    # tokenFile = '../SemEval2018-Task9/training/data/2B.music.training.data.txt'
    # corpusFile = '../Data/2A_med_pubmed_tokenized.txt'
    # # corpusFile = 'testCorpus.txt'
    #
    pm = PatternMining('../Misc/posChunk.json')
    #
    # # pm.getPairs(tokenFile, corpusFile, 'musc_patterns.json')
    # pm.jsonToOurFormat('../MinedData/musc_patterns.json', '../MinedData/musc_patterns.txt')

    tups = pm.getHyperHypo({('such', 'as'), ('especially',)})

    pts = pm.getPatterns(tups)

    pts = pm.sortPatterns(pts)
    newTups = formatTuples(pts)

    tups = pm.getHyperHypo(newTups)

    print(tups)

    print('Hypernim of endodontics')
    # tups = pm.getHypernimOfConcept('cancer', {('such', 'as'), ('especially',)})

    # Find endodontics

