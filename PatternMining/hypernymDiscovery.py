import json
import random

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
        corpus_filename = "../Data/2A_med_pubmed_tokenized/2A_med_pubmed_tokenized_{0}.txt".format(file_id)
        print(corpus_filename)

        tokens = loadJson(corpus_filename)
        for r in concepts:
            for i, token in enumerate(tokens):

                # TODO: Use function here instead from above
                if isNounPhrase(token):
                    for word in token:
                        if word[0].lower() == r.lower() and len(token) == 1:
                            res = matchesPattern(patterns, tokens, i)
                            if res is not None:
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
                    pairs[concept_].add(p)

                # print('concept: {0} -> {1}'.format(concept_, pairs))
    for key, val in pairs.items():
        pairs[key] = list(val)
    return pairs

def recall(pred_dict, gold_dict):

    correct = 0
    tot = 0
    for key_gold, val_gold in gold_dict.items():
        # for key_pred, val_pred in pred_dict:

        if key_gold in pred_dict:

            # pred_val =
            # gold_val =
            for pred_val in pred_dict[key_gold]:

                # if pred_val in gold_dict[key_gold]:
                #     correct += 1
                for gold_val in gold_dict[key_gold]:
                    for t in pred_val.split():

                        if t in gold_val:
                            correct += 1

            tot += len(val_gold)

    return correct/tot

def randomFiles(num=10, seed=1, type='medical'):
    random.seed(seed)
    items = [random.randrange(0, 368) for rand in range(num)]
    fileList = list()
    if type == 'music':
        for file_id in items:
            fileList.append("../Data/2B_music_bioreviews_tokenized/2B_music_bioreviews_tokenized_{0}.txt".format(file_id))
    else:
        for file_id in items:
            fileList.append("../Data/2A_med_pubmed_tokenized/2A_med_pubmed_tokenized_{0}.txt".format(file_id))
    return fileList

if __name__ == '__main__':

    concepts = readConcepts('../SemEval2018-Task9/training/data/2A.medical.training.data.txt')

    patterns = readPatterns('../MinedData/medical_patterns_top20_len2.json')#['and']

    hypernymsConceptMap = readConceptAndHypernyms('../SemEval2018-Task9/training/data/2A.medical.training.data.txt',
        '../SemEval2018-Task9/training/gold/2A.medical.training.gold.txt')

    consideredFileList = randomFiles(5, 10)
    # possibilities = shouldHaveFound(consideredFileList, hypernymsConceptMap)
    #
    # with open('possibilities.json', 'w') as df:
    #     json.dump(possibilities, df)

    dict_ = dict()
    # for seed in range(10):
    dicovered = discoverTokens(concepts, consideredFileList, patterns)
    for key, val in dicovered.items():
        if key not in dict_:
            dict_[key] = list()
        dict_[key].extend(list(val))

    print(recall(dict_, hypernymsConceptMap))

    with open('justatesthere.json', 'w') as df:
        json.dump(dict_, df)


