import nltk
import json
import heapq
from operator import itemgetter
from PatternMining import HypernymMiningPhase2 as hmp


def writeToJsonFile(data, outputFile):
    with open(outputFile, 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False)


def readJsonFile(filename):
    try:
        return json.load(open(filename))
    except:
        print(filename + 'didn\'t work')



class Item:
    def __init__(self, valueList):
        self.valueList = valueList
        self.rank = 0

    def __eq__(self, other):
        # for i, value in enumerate(self.valueList):
        #     if other.valueList[i] != value:
        #         return False
        # return True
        return self.rank == other.rank

    def __lt__(self, other):
        return other.rank < self.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __hash__(self):
        h = 0
        for item in self.valueList:
            h += hash(item)
        return h

    def __str__(self):
        return ' '.join(self.valueList)

    def inToken(self, token):
        start = 0
        for i in range(len(token)):
            if token[i][0] == self.valueList[0]:
                start = i
                break

        if len(token) == 0:
            return False

        for i in range(len(self.valueList)):
            if token[start][0] != self.valueList[i]:
                return False
            start += 1
        return True


class PatternMining2:

    def __init__(self, filename=None):
        self.VALID_POS_TAGS = ['DT', 'JJ', 'NN', 'NNS']
        self.data = None

        if filename is not None:
            self.data = readJsonFile(filename)

    def loadData(self, filename):
        self.data = readJsonFile(filename)

    def readTrainingData(self, trainigFilename, goldFilename):
        map = dict()
        with open(trainigFilename, 'r') as training:
            with open(goldFilename, 'r') as gold:
                for i, line in enumerate(training):
                    value = line.split('\t')[:-1][0].split()
                    itm = Item(value)
                    map[itm] = set()
                    gline = gold.readline()
                    hypernims = gline.replace('\n', '').split('\t')

                    for h in hypernims:
                        map[itm].add(Item(h.split()))
        return map

    def getPatterns(self, concepts, concepts2):

        pats = dict()
        for i, token in enumerate(self.data):
            if self.isNounPhrase(token):
                right = Item([item[0] for item in token])
                if right in concepts:
                    frm, frmToken = self.findNextNounPhrase(i)
                    to = i

                    if frm >= 0 and to <= len(self.data):
                        w = (self.getPattern(frm + 1, to))

                        left = Item([item[0] for item in frmToken])
                        direction = concepts2.getHypernimDirection(str(left), str(right))

                        if w is not None and direction is not None:
                            if w not in pats:
                                pats[w] = {'direction' : direction, 'freq': 0}
                            pats[w]['freq'] += 1
        return pats

    def getPattern(self, lower, upper):
        """
        Returns the pattern between lower and upper in string format
        :param lower:
        :param upper:
        :param lst:
        :return: pattern in string format
        """
        l = list()
        for s in self.data[lower: upper]:
            if s[0].isalnum():
                l.append(s[0])
        return None if len(l) <= 0 else Item(l)

    def findNextNounPhrase(self, i):
        for j in range(i - 1, i - 5, -1):
            item = self.data[j]
            if self.isNounPhrase(item):
                return j, item
        return -1, None

    def itemContains(self, token):
        start = 0
        for i in range(len(token)):
            if token[i][0] == self.valueList[0]:
                start = i
                break

        if len(token) == 0:
            return False

        for i in range(len(self.valueList)):
            if token[start][0] != self.valueList[i]:
                return False
            start += 1
        return True

    def isNounPhrase(self, items):
        if isinstance(items, list):
            for item in items:
                if isinstance(item, list):
                    return True
        return False

    def sortPatterns(self, patterns):
        """
        Sorts patterns based on the frequency
        :param patterns:
        :return:
        """
        lst = list()
        for item, value in patterns.items():
            item.rank = value
            lst.append(item)
        lst.sort()
        return lst


def formatTuples(tuples):
    s = set()
    for t in tuples:
        s.add(tuple(t[1].split()))
    return s


if __name__ == '__main__':

    pm = PatternMining2()

    concepts = pm.readTrainingData('../SemEval2018-Task9/training/data/2A.medical.training.data.txt',
                                   '../SemEval2018-Task9/training/gold/2A.medical.training.gold.txt')

    concepts2 = hmp.HypernymMining()
    concepts2.parse('../SemEval2018-Task9/training/data/2A.medical.training.data.txt',
                                   '../SemEval2018-Task9/training/gold/2A.medical.training.gold.txt')

    pts = dict()
    for i in range(0, 368):

        print(i)

        filename = '../Data/2A_med_pubmed_tokenized/2A_med_pubmed_tokenized_{0}.txt'.format(i)

        pm.loadData(filename)

        patterns = pm.getPatterns(concepts, concepts2)
        for item, value in patterns.items():
            if item not in pts:
                pts[item] = []
            pts[item].append(value)

        # for item, value in patterns.items():
        #     if item not in pts:
        #         pts[item] = 0
        #     pts[item] += value['frequency']

    print(pts)
    # w = pm.sortPatterns(pts)

    # with open('../MinedData/patternUsingTokens.txt', 'w') as f:

    pattern_direction_freq = list()
    for wi in w:
        pattern_direction_freq.append({"pattern" : str(wi), "direction" : "L", "freq":wi.rank})
        print('{0} = {1}'.format(str(wi), wi.rank))

    with open('../MinedData/patternUsingTokens.json', 'w') as df:
        json.dump(pattern_direction_freq, df)