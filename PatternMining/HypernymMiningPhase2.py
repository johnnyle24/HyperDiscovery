import nltk
import json


class HypernymMining:

    def __init__(self):
        self.patterns = dict()

        self.train = dict()
        self.training_hypernyms = set()

        self.nodes = dict()

        self.gen_nps = dict()  # maps from a noun_phrase to node

        self.domain_nps = dict()  # maps from a noun_phrase that got matched to the domain to the gen_nps node

        self.domain_set = set()


    def load(self, concept_filename, gold_filename):
        concepts = list()

        with open(concept_filename, 'r') as concept_file:
            with open(gold_filename, "r") as gold_file:
                for concept_line in concept_file:
                    concept = concept_line.split("\t")

                    concepts.append(concept[0])

                    self.training_hypernyms.add(concept[0])

                for count, gold_line in enumerate(gold_file):
                    hypernyms = gold_line.split("\t")

                    length_hyp = len(hypernyms)

                    node = HyperNode(hypernyms[0], "")
                    self.gen_nps[hypernyms[0]] = node
                    self.training_hypernyms.add(hypernyms[0])

                    for i in range(1, length_hyp):
                        self.training_hypernyms.add(hypernyms[i])

                        node = HyperNode(hypernyms[i], hypernyms[i-1])
                        self.gen_nps[hypernyms[i]] = node

                    node = HyperNode(concepts[count], hypernyms[length_hyp-1])
                    self.gen_nps[concepts[count]] = node

    def parse(self, concept_filename, gold_filename):

        concepts = list()

        with open(concept_filename, 'r') as concept_file:
            with open(gold_filename, "r") as gold_file:
                for concept_line in concept_file:
                    concept = concept_line.split("\t")

                    concepts.append(concept[0])

                    self.training_hypernyms.add(concept[0])

                for count, gold_line in enumerate(gold_file):
                    hypernyms = gold_line.split("\t")

                    length_hyp = len(hypernyms)

                    node = HyperNode(hypernyms[0], "")
                    self.nodes[hypernyms[0]] = node
                    self.training_hypernyms.add(hypernyms[0])

                    for i in range(1, length_hyp):
                        self.training_hypernyms.add(hypernyms[i])

                        node = HyperNode(hypernyms[i], hypernyms[i-1])
                        self.nodes[hypernyms[i]] = node

                    node = HyperNode(concepts[count], hypernyms[length_hyp-1])
                    self.nodes[concepts[count]] = node



        for c in concepts:
            checked = set()
            checked_list = list()

            previous = c
            current = c
            checked.add(c)

            while current != "":
                previous = current
                current = self.nodes[current].parent



                if current in checked:
                    print("Lame")

                else:
                    checked.add(current)
                    checked_list.append(current)

    def parse_patterns(self, pattern_filename, frequency):

        with open(pattern_filename, 'r') as token_file:
            patterns = json.load(token_file)

        for pat in patterns:
            if pat["freq"] < frequency:
                continue
            else:
                self.patterns[pat["pattern"]] = pat["direction"]

    def add_gen_np(self, noun_phrase):
        if noun_phrase not in self.gen_nps:
            node = HyperNode(noun_phrase, "")
            self.gen_nps[noun_phrase] = node
        else:
            self.gen_nps[noun_phrase].freq += 1

    def add_domain_np(self, noun_phrase_left, noun_phrase_right, direction):

        if direction == "L":
            parent = noun_phrase_left
            child = noun_phrase_right
        else:
            parent = noun_phrase_right
            child = noun_phrase_left

        if parent not in self.domain_nps:
            self.gen_nps[parent].parent = self.gen_nps[child].parent
            self.gen_nps[child].parent = parent
            self.gen_nps[parent].has_children = True
        else:
            # check for parent above child
            not_found = True

            present_set = set()

            current = self.gen_nps[child].parent
            present_set.add(current)
            last = child


            while not_found:
                if current == "":
                    break

                if current == parent:
                    not_found = False
                else:
                    last = current
                    current = self.gen_nps[current].parent
                    if current != "":
                        present_set.add(current)

            # check if child is above parent
            if not_found:

                hidden_set = []
                checked = set()
                current = self.gen_nps[parent].parent
                while not_found:

                    if current in checked:
                        print(current)
                        hidden_set.append(current)
                    else:
                        checked.add(current)

                    if current == "":
                        # temp_node_last = self.gen_nps[last]
                        # order_last = self.get_order(last)
                        # temp_node_left = self.gen_nps[parent]
                        # order_right = self.get_order(child)
                        # order_left = self.get_order(parent)
                        break

                    if current == child:
                        not_found = False
                    elif current in present_set:
                        not_found = False
                        # change last
                        last = self.gen_nps[child].phrase

                        while self.gen_nps[last].parent != current:
                            last = self.gen_nps[last].parent

                        self.gen_nps[last].parent = parent
                        self.gen_nps[parent].has_children = True
                    else:
                        current = self.gen_nps[current].parent

                # if not found, take current path and connect it
                if not_found:
                    self.gen_nps[last].parent = parent
                    self.gen_nps[parent].has_children = True

        if parent not in self.domain_nps:
            self.domain_nps[parent] = self.gen_nps[parent]
            self.domain_set.add(parent)

        if child not in self.domain_nps:
            self.domain_nps[child] = self.gen_nps[child]
            self.domain_set.add(child)


    def discover(self, corpus_filename):

        if len(self.patterns) == 0:
            print("No patterns have been added.")
        else:
            with open(corpus_filename, 'r') as file:
                tokens = json.load(file)

                tokens_iter = iter(tokens)

                first_np = ""
                pattern = ""

                count = 0

                for token in tokens_iter:
                    if type(token[0]) is str:
                        pattern += token[0] + " "
                        continue
                    else:
                        second_np = ""
                        for l in token:
                            second_np += l[0] + " "

                        second_np = second_np.rstrip()

                        self.add_gen_np(second_np)

                        pattern = pattern.rstrip()

                        # check if first_np or second_np is in training

                        if (len(first_np) > 3 and len(second_np) > 3 and pattern in self.patterns
                            and first_np != second_np and (first_np in self.training_hypernyms
                            or second_np in self.training_hypernyms or first_np in self.domain_set)):

                            self.add_domain_np(first_np, second_np, self.patterns[pattern])

                            current = first_np

                            check = set()

                            while current != "":
                                current = self.gen_nps[current].parent
                                if current not in check:
                                    check.add(current)
                                else:
                                    print("Found you")


                            current = second_np

                            check = set()

                            while current != "":
                                current = self.gen_nps[current].parent
                                if current not in check:
                                    check.add(current)
                                else:
                                    print("Found you")

                        pattern = ""

                        first_np = second_np

                    count += 1
                    print(count)
                    if(count == 2223):
                        print (count)

    def write_results(self, write_file):

            conc = self.get_concepts()

            for con in conc:
                print(self.get_order(con))


    def get_concepts(self):
        concepts = []

        all = []

        not_domain = []

        for key in self.domain_nps:
            if not self.domain_nps[key].has_children:
                concepts.append(key)
            all.append(key)

        for key in self.gen_nps:
            not_domain.append(key)

        return concepts

    def get_order(self, noun_phrase):

        order = list()

        new_order = list()

        if noun_phrase in self.gen_nps:

            current = noun_phrase

            while current != "":
                order.append(self.gen_nps[current].phrase)
                current = self.gen_nps[current].parent

            indices_collected = set()

            for i in range(0, len(order)):
                max = ""
                max_freq = 0
                max_index = 0
                for index, o in enumerate(order):
                    if self.gen_nps[o].freq > max_freq and index not in indices_collected:
                        max = o
                        max_freq = self.gen_nps[o].freq
                        max_index = index
                indices_collected.add(max_index)
                new_order.append(max)

            return new_order

        else:
            return new_order

    def getHypernimDirection(self, left, right):
        if left in self.training_hypernyms and right in self.training_hypernyms:

            if self.getHypernimRec(left, right):
                return 'R'

            if self.getHypernimRec(right, left):
                return 'L'
        return None

    def getHypernimRec(self, potHypo, potHyper):

        if self.nodes[potHypo].parent == '':
            return False

        if self.nodes[potHypo].parent == potHyper:
            return True

        return self.getHypernimRec(self.nodes[potHypo].parent, potHyper)

    def removeStopWords(self, phrase):
        phrase = phrase.split()
        words = ''
        for word in phrase:
            if word not in stopwords.words('english'):
                words += word + ' '

        return words.rstrip()

def main():

    frequency = 0

    pattern_filename = "../MinedData/patternUsingTokens.json"

    concept_filename = "../SemEval2018-Task9/training/data/2A.medical.training.data.txt"
    gold_filename = "../SemEval2018-Task9/training/gold/2A.medical.training.gold.txt"

    hyp = HypernymMining()

    hyp.parse(concept_filename, gold_filename)

    hyp.parse_patterns(pattern_filename, frequency)

    corpus_filename = "../Data/2A_med_pubmed_tokenized/2A_med_pubmed_tokenized_0.txt"

    hyp.discover(corpus_filename)

# Used for ranking hypernyms found in text
class HyperNode:

    def __init__(self, phrase, parent):
        self.freq = 1
        self.phrase = phrase
        self.parent = parent
        self.has_children = False
        self.visited_rank = False

# if __name__ == '__main__':
    # main()
