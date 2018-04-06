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

    for p in patterns:
        list_pat = [ ]
        for pt in range(i - 1 - len(p.split()), i):
            # if isNounPhrase(data[pt]):
            #
            #     pos = 0
            #     while pt + pos + 1 <= i:
            #         if pos < len(data[pt]):
            #             list_pat.append(data[pt][pos][0])
            #
            #             potential_pattern = '' if len(list_pat) < 0 else ' '.join(list_pat)
            #             if potential_pattern == p:
            #                 return findPrevNounPhrase(data, pt)
            #         pos += 1
            #     pt += pos
            # else:
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

def discoverTokens(concepts):
    concepts = list(filter(lambda x: len(x.split()) == 1, concepts))

    patterns = readPatterns('../MinedData/medical_patterns_top20_len2.json')[:5]#['such as', 'associated with', 'diagnosed with', 'and in']
    # patterns = ['such as', 'associated with', 'diagnosed with', 'and in']

    random_ = random.seed(2)
    items = [random.randrange(0, 368) for rand in range(5)]
    for file_id in items:#range(70, 75):
        corpus_filename = "../Data/2A_med_pubmed_tokenized/2A_med_pubmed_tokenized_{0}.txt".format(file_id)
        print(corpus_filename)

        tokens = loadJson(corpus_filename)
        for r in concepts:

            # with open(corpus_filename, 'r') as file:
            # tokens = json.load(file)

            for i, token in enumerate(tokens):

                if isNounPhrase(token):
                    for word in token:
                        #if isinstance(word, list):
                        # if isNounPhrase(word):
                        if word[0].lower() == r.lower():
                            res = matchesPattern(patterns, tokens, i)
                            if res is not None:
                                print('{0}->{1}'.format(r, res))
                # else:
                #     # for word in token:
                #     if token[0].lower() == r:
                #         res = matchesPattern(['such as'], tokens, i)
                #         if res is not None:
                #             print('{0}->{1}'.format(token, res))

if __name__ == '__main__':

    concepts = readConcepts('../SemEval2018-Task9/training/data/2A.medical.training.data.txt')

    discoverTokens(concepts)

    # This is just to check if inflammation and malady exist together
    # corpus_filename = "../Data/2A_med_pubmed_tokenized/2A_med_pubmed_tokenized_{0}.txt".format(i)
    # tokens = getTokens(corpus_filename)

    # for token in tokens:


