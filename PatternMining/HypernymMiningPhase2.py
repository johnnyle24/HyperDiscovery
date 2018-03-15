import nltk


class HypernymMining:

    def __init__(self):
        self.hyp_hashes = dict()
        self.pat_hashes = dict()

        self.train = dict()
        self.training_hypernyms = set()

        self.nodes = dict()

        self.found_hypernyms = set()

        self.gen_nps = dict()  # maps from a noun_phrase to node

        self.domain_nps = dict()  # maps from a noun_phrase that got matched to the domain to the gen_nps node

    def parse(self, concept_filename, gold_filename):

        concepts = list()

        with open(concept_filename, 'r') as concept_file:
            with open(gold_filename, "r") as gold_file:
                for concept_line in concept_file:
                    concepts.append(concept_line.split("\t")[0])
                for count, gold_line in enumerate(gold_file):
                    hypernyms = gold_line.split("\t")

                    length_hyp = len(hypernyms)

                    node = HyperNode(hypernyms[0], "")
                    self.nodes[hypernyms[0]] = node

                    for i in range(0, length_hyp-1):
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

