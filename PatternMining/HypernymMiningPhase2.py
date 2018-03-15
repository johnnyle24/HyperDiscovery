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

                    for i in range(0, length_hyp-1):
                        self.training_hypernyms.add(hypernyms[i+1])

                        if hypernyms[i+1] not in self.nodes:
                            node = HyperNode(hypernyms[i+1], hypernyms[i])
                            self.nodes[hypernyms[i+1]] = node
                        else:
                            if self.nodes[hypernyms[i+1]].parent == hypernyms[i]:
                                continue
                                # do nothing
                            else:
                                previous = hypernyms[i+1]
                                current = self.nodes[hypernyms[i+1]].parent
                                while current == hypernyms[i] and len(current) != 0:
                                    previous = current
                                    current = self.nodes[current].parent
                                if len(current) == 0:
                                    node = HyperNode(hypernyms[i + 1], "")
                                    self.nodes[hypernyms[i + 1]] = node
                                    self.nodes[previous].parent = hypernyms[i+1]


                            # needs to do a check to see if node already exists
                            # percolate up logic

                    self.train[concepts[count]] = hypernyms[len(hypernyms)-1]

    def parse_patterns(self, pattern_filename, frequency):

        frequency = 0

        pattern_filename = "../MinedData/patternUsingTokens.json"

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

        if noun_phrase_left == "tuberculosis" and noun_phrase_right == "an immunocompetent host":
            print("D")

        if direction == "L":
            if noun_phrase_left not in self.domain_nps:
                self.gen_nps[noun_phrase_left].parent = self.gen_nps[noun_phrase_right].parent
                self.gen_nps[noun_phrase_right].parent = noun_phrase_left
                self.gen_nps[noun_phrase_left].has_children = True
            else:
                # check for parent above child
                not_found = True

                present_set = set()

                current = self.gen_nps[noun_phrase_right].parent
                present_set.add(current)
                last = noun_phrase_right


                while not_found:
                    if current == "":
                        break

                    if current == noun_phrase_left:
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
                    current = self.gen_nps[noun_phrase_left].parent
                    while not_found:

                        if current in checked:
                            print(current)
                            hidden_set.append(current)
                        else:
                            checked.add(current)

                        if current == "":
                            temp_node_last = self.gen_nps[last]
                            order_last = self.get_order(last)
                            temp_node_left = self.gen_nps[noun_phrase_left]
                            order_right = self.get_order(noun_phrase_right)
                            order_left = self.get_order(noun_phrase_left)
                            break

                        if current == noun_phrase_right or current in present_set:
                            not_found = False
                        else:
                            current = self.gen_nps[current].parent

                    # if not found, take current path and connect it
                    if not_found:
                        if noun_phrase_left == "disseminated cryptococcal infection":
                            print("Check")
                        self.gen_nps[last].parent = noun_phrase_left
                        self.gen_nps[noun_phrase_left].has_children = True
        else:
            if noun_phrase_right not in self.domain_nps:
                self.gen_nps[noun_phrase_right].parent = self.gen_nps[noun_phrase_left].parent
                self.gen_nps[noun_phrase_left].parent = noun_phrase_right
                self.gen_nps[noun_phrase_right].has_children = True
            else:
                # check for parent above child
                not_found = True
                current = self.gen_nps[noun_phrase_left].parent
                last = noun_phrase_left
                while not_found:
                    if current == "":
                        break

                    if current == noun_phrase_right:
                        not_found = False
                    else:
                        last = current
                        current = self.gen_nps[current].parent

                # check if child is above parent
                if not_found:
                    current = self.gen_nps[noun_phrase_right].parent
                    while not_found:
                        if current == "":
                            break

                        if current == noun_phrase_left:
                            not_found = False
                        else:
                            current = self.gen_nps[current].parent

                    # if not found, take current path and connect it
                    if not_found:
                        self.gen_nps[last].parent = noun_phrase_right
                        self.gen_nps[noun_phrase_right].has_children = True

        if noun_phrase_left not in self.domain_nps:
            self.domain_nps[noun_phrase_left] = self.gen_nps[noun_phrase_left]

        if noun_phrase_right not in self.domain_nps:
            self.domain_nps[noun_phrase_right] = self.gen_nps[noun_phrase_right]

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

                        if len(first_np) > 3 and len(second_np) > 3 and pattern in self.patterns and first_np != second_np:

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

            print("Now must order everything")

    def get_concepts(self):
        pass

    def sort_orders(self):
        pass

    def get_order(self, noun_phrase):

        order = list()

        current = noun_phrase

        while current != "":
            order.append(self.gen_nps[current].phrase)
            current = self.gen_nps[current].parent

        return order


def main():

    frequency = 0

    pattern_filename = "../MinedData/patternUsingTokens.json"

    hyp = HypernymMining()

    hyp.parse_patterns(frequency, pattern_filename)

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

    # Takes in a child node and will append its phrase to the current's children
    # Additionally, will add the current's phrase to the child's parents
    def add_child(self, child):
        if child.phrase in self.child_set:
            return
        else:
            self.child_set.add(child.phrase)
            child.add_parent(self)
            self.rank += 1

    def add_parent(self, parent):
        if parent.phrase in self.parent_set:
            return
        else:
            self.parent_set.add(parent.phrase)

if __name__ == '__main__':
    main()