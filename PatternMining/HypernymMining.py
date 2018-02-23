

class HypernymMining:

    def __init__(self):
        self.hyp_hashes = dict()
        self.pat_hashes = dict()

        self.node_map = dict()

    # Extracts hypernym phrases from a body of text such as PubMed
    def extract_hypernyms(self, file_name):
        if len(self.pat_hashes) == 0:
            print("No patterns have been added.")
        else:
            with open(file_name, 'r') as file:
                for line in file:

                    str_split = line.lower().split(' ')

                    split_len = len(str_split)
                    for word_index in range(0, split_len):
                        one_gram = str_split[word_index]

                        one_gram = one_gram.rstrip()

                        if self.check_patterns(one_gram):

                            self.pos(line)

                            # check left
                            if self.check_hyps(left_phrase):
                                # self.add_hypernym_to_hash(str_split[word_index + 3], 1)
                                self.add_hypernym_to_hash(right_phrase, 1)
                                self.add_hypernym_to_nodes(right_phrase, left_phrase, "")

                            # check right
                            if self.check_hyps(right_phrase):
                                # self.add_hypernym_to_hash(str_split[word_index - 1], 1)
                                self.add_hypernym_to_hash(left_phrase, 1)
                                self.add_hypernym_to_nodes(left_phrase, "", right_phrase)

                        if (word_index+1) < split_len:
                            two_gram = str_split[word_index] + " " + str_split[word_index+1]

                            two_gram = two_gram.rstrip()

                            if self.check_patterns(two_gram):

                                self.pos(line)

                                # check left
                                if self.check_hyps(left_phrase):
                                    #self.add_hypernym_to_hash(str_split[word_index + 3], 1)
                                    self.add_hypernym_to_hash(right_phrase, 1)
                                    self.add_hypernym_to_nodes(right_phrase, left_phrase, "")


                                # check right
                                if self.check_hyps(right_phrase):
                                    #self.add_hypernym_to_hash(str_split[word_index - 1], 1)
                                    self.add_hypernym_to_hash(left_phrase, 1)
                                    self.add_hypernym_to_nodes(left_phrase, "", right_phrase)

                        if (word_index+2) < split_len:
                            three_gram = str_split[word_index] + " " + str_split[word_index + 1] + " " + str_split[word_index + 2]

                            three_gram = three_gram.rstrip()

                            if self.check_patterns(three_gram):

                                self.pos(line)

                                # check left
                                if self.check_hyps(left_phrase):
                                    #self.add_hypernym_to_hash(str_split[word_index + 3], 1)
                                    self.add_hypernym_to_hash(right_phrase, 1)
                                    self.add_hypernym_to_nodes(right_phrase, left_phrase, "")


                                # check right
                                if self.check_hyps(right_phrase):
                                    #self.add_hypernym_to_hash(str_split[word_index - 1], 1)
                                    self.add_hypernym_to_hash(left_phrase, 1)
                                    self.add_hypernym_to_nodes(left_phrase, "", right_phrase)


        # self.rank_nodes
        # evaluations

    def pos(self, phrase):
        print("Not done")


    def check_hyps(self, phrase):
        if phrase in self.hyp_hashes:
            return True
        else:
            return False


    # Checks if the gram matches a pattern
    def check_patterns(self, phrase):
        if phrase in self.pat_hashes:
            return True
        else:
            return False

    # Extracts the patterns STORED in a patterns.txt file paired with its frequency
    def hash_patterns(self, file_name):
        with open(file_name, 'r') as file:
            for line in file:
                str_split = line.lower().split('=')
                phrase = str_split[0].rstrip()
                frequency = int(str_split[1])
                self.add_pattern(phrase, frequency)

    # Add the patterns to the hashmap and adjusts the number of times found if necessary
    # This is done to check if the gram is a pattern in constant time
    def add_pattern(self, phrase, frequency):
        if phrase in self.pat_hashes:
            self.pat_hashes[phrase] += frequency
        else:
            self.pat_hashes[phrase] = frequency

    # Extracts the hypernyms STORED in a hypernyms.txt file tagged with 'concept'
    def hash_hypernyms(self, file_name):
        with open(file_name, 'r') as file:
            for line in file:
                str_split = line.lower().split('concept')
                phrase = str_split[0].rstrip()
                self.add_hypernym_to_hash(phrase, 1)

    # Adds the hypernyms to the hashmap and adjusts number of times found if necessary
    # This is done for checking if the gram is a known hypernym in constant time
    def add_hypernym_to_hash(self, phrase, frequency):
        if phrase in self.hyp_hashes:
            self.hyp_hashes[phrase] += frequency
        else:
            self.hyp_hashes[phrase] = frequency
            self.add_hypernym_to_nodes(phrase, "", "")

    # Creates a hypernym node and adds it to the hashmap/dictionary
    # Used for ranking the hypernyms
    def add_hypernym_to_nodes(self, phrase, parent, child):
        if phrase in self.node_map:
            if child != "":
                self.node_map[phrase].add_child(child)
                self.node_map[phrase].rank += 1
            if parent != "":
                self.node_map[phrase].add_parent(parent)
        else:
            node = HyperNode(phrase)
            if child != "":
                node.add_child(child)
                node.rank += 1
            if parent != "":
                node.add_parent(parent)

            self.node_map[phrase] = node

    def check_for_circular_dep(self, phrase):

        print("Not implemented yet")

        searching = False

        while searching:

            current = self.node_map[phrase]

    def rank_nodes(self):
        print("Not implemented yet")



# Used for ranking hypernyms found in text
class HyperNode:

    def __init__(self, phrase):
        self.rank = 0
        self.phrase = phrase
        self.child_set = set()
        self.parent_set = set()

    def add_child(self, child):
        if child in self.child_set:
            return
        else:
            self.child_set.add(child)

    def add_parent(self, parent):
        if parent in self.parent_set:
            return
        else:
            self.parent_set.add(parent)

