import nltk
import json
from nltk.corpus import stopwords
import heapq

class HypernymMining:

    def __init__(self):
        # self.patterns = dict() # maps to pattern
        self.patterns = set()

        self.concepts = dict() # maps to a set of hypernyms

        self.hypernyms = dict() # maps to a set of concepts

        self.test_hypernyms = dict()

        self.true_patterns = dict()

    # Loads the test concepts and mined patterns
    def load(self, concept_filename, pattern_filename):

        with open(concept_filename, 'r') as concept_file:
            for concept_line in concept_file:
                concept = concept_line.split("\t")

                self.concepts[concept[0]] = set()

        self.parse_patterns(pattern_filename, 10)

    # Loads the test concepts and mined patterns
    def load_test(self, concept_filename, test_hypernyms):

        concepts = list()

        with open(test_hypernyms, 'r') as gold_file:
            with open(concept_filename, 'r') as concept_file:
                for concept_line in concept_file:
                    concept = concept_line.split("\t")

                    concepts.append(concept[0])
            for i, hypernym_line in enumerate(gold_file):
                hypernyms = hypernym_line.split("\t")

                self.test_hypernyms[concepts[i]] = set()

                for hyp in hypernyms:
                    self.test_hypernyms[concepts[i]].add(hyp)

    def load_everything(self, concept_filename, gold_filename, pattern_filename):
        concepts = list()

        with open(concept_filename, 'r') as concept_file:
            with open(gold_filename, "r") as gold_file:
                for concept_line in concept_file:
                    concept = concept_line.split("\t")

                    concepts.append(concept[0])

                for count, gold_line in enumerate(gold_file):
                    hypernyms = gold_line.split("\t")

                    length_hyp = len(hypernyms)

                    self.concepts[concepts[count]] = set()

                    for i in range(1, length_hyp):
                        if hypernyms[i] in self.hypernyms:
                            self.hypernyms[hypernyms[i]].add(concepts[count])
                        else:
                            self.hypernyms[hypernyms[i]] = set()
                            self.hypernyms[hypernyms[i]].add(concepts[count])

                        self.concepts[concepts[count]].add(hypernyms[i])

        self.parse_patterns(pattern_filename)

    def parse_patterns(self, pattern_filename, frequency):

        with open(pattern_filename, 'r') as token_file:
            patterns = json.load(token_file)

        # for pat in patterns:
        #     if pat["freq"] < frequency:
        #         continue
        #     else:
        #         self.patterns[pat["pattern"]] = pat["direction"]

        for pat in patterns:
            self.patterns.add(pat["pattern"])

    def discover(self, corpus_filename, greediness):
        # iterate through tokens until a pattern is found. Then check if there is a concept to left or right of it.
        # add the other value if found

        if len(self.patterns) == 0:
            print("No patterns have been added.")
        else:
            with open(corpus_filename, 'r') as file:
                tokens = json.load(file)

                tokens_iter = iter(tokens)

                nps = list()

                for i in range(0, greediness):
                    nps.append("")

                first_np = ""
                # pattern = ""

                pattern = set()

                for token in tokens_iter:
                    if type(token[0]) is str:
                        # old
                        # pattern += token[0].lower().rstrip() + " "
                        pattern.add((token[0].lower()).rstrip())
                        continue
                    else:
                        # check for a concept
                        second_np = ""
                        for l in token:
                            second_np += l[0] + " "

                        second_np = second_np.rstrip()

                        nps[len(nps)-1] = second_np

                        # old
                        # pattern = pattern.rstrip()

                        for i in range(1, len(nps)):
                            self.collect(nps[i-1], nps[i], pattern)

                        # first_np = second_np

                        # shift elements

                        for i in range(1, len(nps)):
                            nps[i-1] = nps[i]

                        # pattern = "" # old
                        pattern = set()


    def collect(self, first_np, second_np, pattern):

        # Using all data

        # if (first_np in self.concepts and second_np in self.test_hypernyms[first_np]) or (
        #         second_np in self.concepts and first_np in self.test_hypernyms[second_np]):
        #     if first_np in self.concepts:
        #         self.concepts[first_np].add(second_np)
        #     if second_np in self.concepts:
        #         self.concepts[second_np].add(first_np)

        # if pattern in self.true_patterns:
        #         self.true_patterns[pattern] += 1
        #     else:
        #         self.true_patterns[pattern] = 1
        #     print("Found")




        # old
        # if (len(first_np)>0 and len(second_np) > 0 and pattern in self.patterns and first_np != second_np and
        #         (first_np in self.concepts or second_np in self.concepts)):
        valid = False

        for pt in self.patterns:
            if pt in pattern:
                valid = True

        if (len(first_np) > 0 and len(second_np) > 0 and valid and first_np != second_np and
                (first_np in self.concepts or second_np in self.concepts)):
            if first_np in self.concepts and second_np not in self.hypernyms:
                self.concepts[first_np].add(second_np)
                if second_np in self.hypernyms:
                    self.hypernyms[second_np].add(first_np)
                else:
                    self.hypernyms[second_np] = set()
                    self.hypernyms[second_np].add(first_np)
            else:
                if second_np in self.concepts and first_np not in self.hypernyms:
                    self.concepts[second_np].add(first_np)
                    if first_np in self.hypernyms:
                        self.hypernyms[first_np].add(second_np)
                    else:
                        self.hypernyms[first_np] = set()
                        self.hypernyms[first_np].add(second_np)
                else:
                    pass
        else:
            if ((first_np in self.hypernyms and second_np not in self.hypernyms) or
                    (first_np not in self.hypernyms and second_np in self.hypernyms)):
                if (len(first_np) > 0 and len(second_np) > 0):
                    # check which one is the more general hypernym

                    if first_np not in self.hypernyms:
                        self.hypernyms[first_np] = set()

                        for s in self.hypernyms[second_np]:
                            self.hypernyms[first_np].add(s)
                            self.concepts[s].add(first_np)

                    if second_np not in self.hypernyms:
                        self.hypernyms[second_np] = set()

                        for s in self.hypernyms[first_np]:
                            self.hypernyms[second_np].add(s)
                            self.concepts[s].add(second_np)

    def write_percentages(self, concept_file, results_file):
        concepts = list()

        with open(concept_file, 'r') as cfile:
            for concept_line in cfile:
                concept = concept_line.split("\t")

                concepts.append(concept[0])

        with open(results_file, 'w') as f:
            for c in concepts:
                found = 0
                for t_hyp in self.test_hypernyms[c]:
                    if t_hyp in self.concepts[c]:
                        found += 1

                f.write(str(float(found)/float(len(self.test_hypernyms[c]))) + '\n')

    def write_true_patterns(self, frequency):
        with open("../MinedData/patterns_output", 'w') as file:
            for pat in self.true_patterns:
                if self.true_patterns[pat] > frequency:
                    file.write(pat + ' ::: frequency :::' + str(self.true_patterns[pat]) + '\n')

    def write_model(self):

        dir = '../Data/Model'
        # with open(dir + '/concepts.json', 'w') as conFile:
        #     json.dump(self.get_concepts(), conFile)
        #
        # with open(dir + '/hypernyms.json', 'w') as conFile:
        #     json.dump(self.domain_nps, conFile)

        concepts = list()

        for con in self.concepts:
            concepts.append(con)

        with open(dir + '/concepts.txt', 'w') as f:
            for con in concepts:
                f.write('{0}\tConcept\n'.format(con))

        with open(dir + '/hypernyms.txt', 'w') as f:
            for con in concepts:
                orderList = self.get_hypernyms(con)
                if len(orderList) > 0:
                    print('writing {0}'.format(con))
                    f.write('\t'.join(orderList))
                    f.write('\n')


    def test(self):
        dir = '../Data/Model'
        concepts = []
        with open('../SemEval2018-Task9/test/data/2B.music.test.data.txt') as f:

            for line in f:
                concepts.append(line.split('\t')[0])

        with open(dir + '/hypernyms.txt', 'w') as f:
            for con in concepts:
                orderList = self.get_hypernyms(con)
                if len(orderList) > 0:
                    print('writing {0}'.format(con))
                    hypermym = '\t'.join(orderList)
                    f.write(hypermym.replace('\n', ''))
                    hypermym = ''
                f.write('\n')

    def write_hypernyms(self, concept_file, results_file):

        concepts = list()

        with open(concept_file, 'r') as cfile:
            for concept_line in cfile:
                concept = concept_line.split("\t")

                concepts.append(concept[0])

        with open(results_file, 'w') as f:

            for c in concepts:
                hypernyms = ""
                for hyp in self.concepts[c]:
                    hypernyms += hyp + "\t"

                hypernyms.rstrip()

                f.write(hypernyms + '\n')


    def write_results(self, test_concepts, write_file):

        concepts = list()

        for con in self.concepts:
            concepts.append(con)

        predictions = []
        for t_concept in test_concepts:

            if t_concept in concepts:
                predictions.append(self.get_hypernyms(t_concept))
            else:
                predictions.append(None)

        with open(write_file, 'w') as f:

            for prediction in predictions:
                if prediction is not None:
                    f.write('\t'.join(prediction))
                    f.write('\n')

    def get_concepts(self, hypernym):

        concepts = list()
        concepts.append("None Found")

        if hypernym in self.hypernyms:
            concepts = list()

            for con in self.hypernyms[hypernym]:
                concepts.append(con)

        return concepts

    def get_hypernyms(self, concept):

        hypernyms = list()
        hypernyms.append("None Found")

        if concept in self.concepts:
            hypernyms = list()

            for hyp in self.concepts[concept]:
                hypernyms.append(hyp)

        return hypernyms

    # def getHypernimDirection(self, left, right):
    #     if left in self.training_hypernyms and right in self.training_hypernyms:
    #
    #         if self.getHypernimRec(left, right):
    #             return 'R'
    #
    #         if self.getHypernimRec(right, left):
    #             return 'L'
    #     return None
    #
    # def getHypernimRec(self, potHypo, potHyper):
    #
    #     if self.nodes[potHypo].parent == '':
    #         return False
    #
    #     if self.nodes[potHypo].parent == potHyper:
    #         return True
    #
    #     return self.getHypernimRec(self.nodes[potHypo].parent, potHyper)

    def removeStopWords(self, phrase):
        phrase = phrase.split()
        words = ''
        for word in phrase:
            if word not in stopwords.words('english'):
                words += word + ' '

        return words.rstrip()

def run(pattern_filename, concept_filename, corpus_subname, test_hypernyms, results_file, percents_file, greediness, frange = (0, 369)):
    frequency = 0

    hyp = HypernymMining()

    hyp.load(concept_filename, pattern_filename)

    hyp.load_test(concept_filename, test_hypernyms)

    for i in range(frange[0], frange[1]):
        corpus_filename = "{0}_{1}.txt".format(corpus_subname, i)

        hyp.discover(corpus_filename, greediness)
        print("Now serving file number: {0}".format(i))

    # hyp.write_true_patterns(1)

    hyp.write_hypernyms(concept_filename, results_file)

    hyp.write_percentages(concept_filename, percents_file)

    # # hyp.test()
    # hyp.write_model()

    pass

def music(r=369):
    pattern_filename = "../MinedData/music_patterns.json"

    concept_filename = "../SemEval2018-Task9/training/data/2B.music.training.data.txt"
    test_hypernyms = "../SemEval2018-Task9/test/gold/2B.music.test.gold.txt"
    gold_filename = "../SemEval2018-Task9/training/gold/2B.music.training.gold.txt"
    corputSubName = "../Data/2B_music_bioreviews_tokenized/2B_music_bioreviews_tokenized"

    results_file = "../MinedData/musical_hypernym_results.txt"

    percents_file = "../MinedData/musical_hypernym_percents.txt"

    greediness = 5

    run(pattern_filename, concept_filename, corputSubName, test_hypernyms, results_file, percents_file, greediness, frange=(0, r))

def medical(r=369):
    # pattern_filename = "../MinedData/medical_patterns_top20_len3.json"
    pattern_filename = "../MinedData/medical_patterns_revised.json"

    # concept_filename = "../SemEval2018-Task9/training/data/2A.medical.training.data.txt"
    concept_filename = "../SemEval2018-Task9/test/data/2A.medical.test.data.txt"
    test_hypernyms = "../SemEval2018-Task9/test/gold/2A.medical.test.gold.txt"
    gold_filename = "../SemEval2018-Task9/training/gold/2A.medical.training.gold.txt"
    corputSubName = "../Data/2A_med_pubmed_tokenized/2A_med_pubmed_tokenized"

    percents_file = "../MinedData/medical_hypernym_percents.txt"

    results_file = "../MinedData/medical_hypernym_results.txt"

    greediness = 5

    run(pattern_filename, concept_filename, corputSubName, test_hypernyms, results_file, percents_file, greediness, frange=(0, r))

# Used for ranking hypernyms found in text
class HyperNode:

    def __init__(self, phrase, parent):
        self.freq = 1
        self.phrase = phrase
        self.parent = parent
        self.has_children = False
        self.visited_rank = False

if __name__ == '__main__':
    # music(5)
    medical()
    # main()

    # pattern_filename = "../MinedData/medical_patterns.json"
    #
    # concept_filename = "../SemEval2018-Task9/training/data/2A.medical.training.data.txt"
    # gold_filename = "../SemEval2018-Task9/training/gold/2A.medical.training.gold.txt"
    # corputSubName = "../Data/2A_med_pubmed_tokenized/2A_med_pubmed_tokenized"
    #
    # run(pattern_filename, concept_filename, gold_filename, corputSubName)