import json
import random
from nltk.stem.porter import *

class score:
    def __init__(self, pred_dict, gold_dict):
        # self.pred_dict = pred_dict
        self.pred_dict = dict()

        stemmer = PorterStemmer()
        for key, val in pred_dict.items():
            self.pred_dict[key] = set()
            for item in val:
                clean = ' '.join([stemmer.stem(t) for t in item.split()])
                self.pred_dict[key].add(clean)

        self.gold_dict = gold_dict

    def recall(self):
        stemmer = PorterStemmer()

        correct = 0
        tot = 0
        visited = set()
        for key_gold, val_gold in self.gold_dict.items():

            if key_gold in self.pred_dict:

                for pred_val in self.pred_dict[key_gold]:

                    for gold_val in self.gold_dict[key_gold]:
                        for t in pred_val.split():

                            if stemmer.stem(t) in gold_val and t not in visited:
                                visited.add(t)
                                correct += 1

                tot += len(val_gold)

        if tot == 0:
            return 0
        return correct/tot

    def precision(self):
        stemmer = PorterStemmer()

        correct = 0
        for key_gold, val_gold in self.gold_dict.items():

            if key_gold in self.pred_dict:

                for pred_val in self.pred_dict[key_gold]:

                    for gold_val in self.gold_dict[key_gold]:
                        for t in pred_val.split():

                            if stemmer.stem(t) in gold_val:
                                correct += 1

        sum_ = sum([len(p) for p in self.pred_dict.values()])
        if sum_ == 0:
            return 0
        return correct/ sum_

    def fscore(self):

        denom = (self.precision() + self.recall())
        if denom == 0:
            return 0
        return 2 * ((self.precision() * self.recall()) / denom)


def readConcepts(fileName):
    result = list()
    with open(fileName, 'r') as file:
        for line in file:
            result.append(line.split('\t')[0])
    return result

def isNounPhrase(items):
    if isinstance(items, list):
        for item in items:
            if isinstance(item, list):
                return True
    return False

def findPrevNounPhrase(data, i):
    for j in range(i - 1, i - 5, -1):
        item = data[j]
        if isNounPhrase(item):
            return j, item
    return -1, None

def matchesPattern(patterns, data, i):

    list_pat = [ ]
    for p in patterns:

        if len(p.split()) != len(list_pat):
            list_pat = []
            for pt in range(i - 1 - len(p.split()), i):
                if not isNounPhrase(data[pt]):
                    list_pat.append(data[pt][0])

        potential_pattern = '' if len(list_pat) < 0 else ' '.join(list_pat)
        if potential_pattern == p:
            return findPrevNounPhrase(data, i)

def loadJson(corpus_filename):
    with open(corpus_filename, 'r') as file:
        return json.load(file)

def readPatterns(corpus_filename):
    tokens = loadJson(corpus_filename)
    return [token['pattern'] for token in tokens]

def readConceptAndHypernyms(conceptsFileName, hypernymFileName):

    hypernymConceptMapping = dict()
    with open(conceptsFileName, 'r') as conceptFile:
        with open(hypernymFileName, 'r') as hypernymFile:
            conceptFile = conceptFile.readlines()
            hypernymFile = hypernymFile.readlines()

            if len(conceptFile) != len(hypernymFile):
                return None

            for current in range(len(conceptFile)):
                concept = conceptFile[current].replace('\n', '').split('\t')[0]
                hypernyms = hypernymFile[current].replace('\n', '').split('\t')
                hypernymConceptMapping[concept] = set([x.lower() for x in hypernyms])

    return hypernymConceptMapping

def containsConceptInToken(concept, token):

    # if isNounPhrase(token):
    for word in token:
        if word[0].lower() == concept.lower():
            return True
    return False

def containsHypernymsInToken(hypernyms, token):

    if isNounPhrase(token):
        for word in token:
            if word[0].lower() in hypernyms:
                return word[0]
    return None


def discoverTokens(concepts, items, patterns):
    concepts = list(filter(lambda x: len(x.split()) == 1, concepts))

    # random.seed(seed)
    # items = [random.randrange(0, 368) for rand in range(5)]
    # results = set()
    results = dict()
    for file_id in items:
        # corpus_filename = "../Data/2A_med_pubmed_tokenized/2A_med_pubmed_tokenized_{0}.txt".format(file_id)
        corpus_filename = file_id
        print(corpus_filename)

        tokens = loadJson(corpus_filename)
        for r in concepts:
            for i, token in enumerate(tokens):

                # TODO: Use function here instead from above
                if isNounPhrase(token):
                    for word in token:
                        if word[0].lower() == r.lower() and len(token) == 1:
                            res = matchesPattern(patterns, tokens, i)
                            if res is not None and res[1] is not None:
                                lst = [item[0] for item in res[1]]

                                if word[0] not in results:
                                    results[word[0]] = set()

                                results[word[0]].add(' '.join(lst))
                                print('{0}->{1}'.format(r, res))
    return results

def getPairs(concept, hypernyms, tokens):
    resultPairs = list()
    for i, token in enumerate(tokens):

        if isNounPhrase(token):
            if containsConceptInToken(concept, token):

                j, provHypernym = findPrevNounPhrase(tokens, i)
                matchHypernym = containsHypernymsInToken(hypernyms, provHypernym)
                if matchHypernym is not None:
                    resultPairs.append(matchHypernym)#' '.join([item[0] for item in provHypernym]))
    return resultPairs

def shouldHaveFound(fileNameList, hypernymsConceptMap):
    pairs = dict()
    for file in fileNameList:
        tokens = loadJson(file)
        for concept_, hypernyms_ in hypernymsConceptMap.items():
            pairResults = getPairs(concept_, hypernyms_, tokens)
            if len(pairResults) > 0:
                if concept_ not in pairs:
                    pairs[concept_] = set()

                for p in pairResults:
                    pairs[concept_].add(p.lower())

                # print('concept: {0} -> {1}'.format(concept_, pairs))
    for key, val in pairs.items():
        pairs[key] = list(val)
    return pairs

def randomFiles(num=10, seed=-1, type='medical'):
    if seed >= 0:
        random.seed(seed)


    fileList = list()
    if type == 'music':
        items = [random.randrange(0, 438) for rand in range(num)]
        for file_id in items:
            fileList.append("../Data/2B_music_bioreviews_tokenized/2B_music_bioreviews_tokenized_{0}.txt".format(file_id))
    else:
        items = [random.randrange(0, 368) for rand in range(num)]
        # items = [55]
        for file_id in items:
            fileList.append("../Data/2A_med_pubmed_tokenized/2A_med_pubmed_tokenized_{0}.txt".format(file_id))
    return fileList

def getPossibilities(consideredFileList, hypernymsConceptMap, possibilitiesFile = 'possibilities.json', loadFile=False):

    if not loadFile:
        possibilities = shouldHaveFound(consideredFileList, hypernymsConceptMap)

        with open(possibilitiesFile, 'w') as df:
            json.dump(possibilities, df)
        return possibilities
    else:
        return loadJson(possibilitiesFile)

def getDiscoveredHypernyms(concepts, consideredFileList, patterns, discoveredHypernymsFile='discoveredHypernyms.json', loadFile=False):

    if not loadFile:
        dict_ = dict()

        dicovered = discoverTokens(concepts, consideredFileList, patterns)
        for key, val in dicovered.items():
            if key not in dict_:
                dict_[key] = list()
            dict_[key].extend(list(val))

        with open(discoveredHypernymsFile, 'w') as df:
            json.dump(dict_, df)

        return dict_
    else:
        return loadJson(discoveredHypernymsFile)

def runScoring(trainingFilename, goldFilename, patternFileName, dataType_):
    '''
    The Results will be written in the Scoring/ScoringData subdirectory

    :param trainingFilename:
    :param goldFilename:
    :param patternFileName:
    :return:
    '''
    concepts = readConcepts(trainingFilename)

    patterns = readPatterns(patternFileName)

    hypernymsConceptMap = readConceptAndHypernyms(trainingFilename,goldFilename)

    loadPossibilities = False
    loadHypernyms = False
    NSamples = 5
    seeds = [random.randrange(0, 368) for rand in range(5)]
    # seeds = [55]

    with open('../Scoring/ScoringData/scoringResults.txt', 'w') as scoringFile:
        for instance, seed in enumerate(seeds):
            consideredFileList = randomFiles(NSamples, seed=seed, type=dataType_)

            possibilities = getPossibilities(consideredFileList, hypernymsConceptMap,
                                             '../Scoring/ScoringData/possibilities{0}.json'.format(instance),
                                             loadFile=loadPossibilities)

            dict_ = getDiscoveredHypernyms(concepts, consideredFileList, patterns,
                                           '../Scoring/ScoringData/discoveredHypernyms{0}.json'.format(instance),
                                           loadFile=loadHypernyms)

            print('Considered Files:')
            for f in consideredFileList:
                scoringFile.write(f + '\n')
                print(f)

            print()
            scoringFile.write('\n'*2)

            scoring = score(dict_, possibilities)
            recall = 'Recall: {0}'.format(scoring.recall())
            precision = 'Precision: {0}'.format(scoring.precision())
            fscore = 'F score: {0}'.format(scoring.fscore())

            print(recall)
            print(precision)
            print(fscore)

            scoringFile.write(recall + '\n')
            scoringFile.write(precision + '\n')
            scoringFile.write(fscore + '\n')
            scoringFile.write('-'*80)
            scoringFile.write('\n'*2)

def runMusic():
    runScoring('../SemEval2018-Task9/training/data/2B.music.training.data.txt',
               '../SemEval2018-Task9/training/gold/2B.music.training.gold.txt',
               '../MinedData/medical_patterns_top20_len2.json', 'music')

def runMedical():
    runScoring('../SemEval2018-Task9/training/data/2A.medical.training.data.txt',
               '../SemEval2018-Task9/training/gold/2A.medical.training.gold.txt',
               '../MinedData/medical_patterns_top20_len2.json', 'medical')


if __name__ == '__main__':
    runMedical()