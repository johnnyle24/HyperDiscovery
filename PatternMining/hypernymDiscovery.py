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

        try:
            potential_pattern = '' if len(list_pat) < 0 else ' '.join(list_pat)
            if potential_pattern == p:
                return findPrevNounPhrase(data, i)
        except:
            pass

def loadJson(corpus_filename):
    with open(corpus_filename, 'r') as file:
        return json.load(file)

def readPatterns(corpus_filename):
    tokens = loadJson(corpus_filename)
    return [token['pattern'] for token in tokens]

def discoverTokens(concepts, seed, patterns):
    concepts = list(filter(lambda x: len(x.split()) == 1, concepts))

    random.seed(seed)
    items = [random.randrange(0, 368) for rand in range(5)]
    results = set()
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
                        if word[0].lower() == r.lower() and len(token) == 1:
                            res = matchesPattern(patterns, tokens, i)
                            if res is not None:
                                lst = [item[0] for item in res[1]]
                                results.add(' '.join(lst))
                                print('{0}->{1}'.format(r, res))
                # else:
                #     # for word in token:
                #     if token[0].lower() == r:
                #         res = matchesPattern(['such as'], tokens, i)
                #         if res is not None:
                #             print('{0}->{1}'.format(token, res))
    return results

if __name__ == '__main__':

    concepts = ['obesity']#readConcepts('../SemEval2018-Task9/training/data/2A.medical.training.data.txt')

    # patterns = readPatterns('../MinedData/medical_patterns_top20_len2.json')[:5]#['such as', 'associated with', 'diagnosed with', 'and in']
    patterns = ['and']

    set_ = set()
    for seed in range(10):
        dicovered = discoverTokens(concepts, seed, patterns)
        for disc in dicovered:
            set_.add(disc)


    # print(set_)

    with open('justatesthere.json', 'w') as df:
        json.dump(list(set_), df)


    # This is just to check if inflammation and malady exist together
    # corpus_filename = "../Data/2A_med_pubmed_tokenized/2A_med_pubmed_tokenized_{0}.txt".format(i)
    # tokens = getTokens(corpus_filename)

    # for token in tokens:


