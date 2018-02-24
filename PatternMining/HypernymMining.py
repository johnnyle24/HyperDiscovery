import nltk


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

                            pos_list = self.pos(line)

                            for index in range(0, len(pos_list)):
                                if isinstance(pos_list[index], tuple):
                                    if pos_list[index][0] == one_gram:
                                        left_phrase = self.find_phrase_left(pos_list, index)
                                        right_phrase = self.find_phrase_right(pos_list, index)

                                        # check left
                                        if self.check_hyps(left_phrase):
                                            self.add_hypernym_to_hash(right_phrase, 1)
                                            self.add_hypernym_to_nodes(right_phrase, left_phrase, "")

                                        # check right
                                        if self.check_hyps(right_phrase):
                                            self.add_hypernym_to_hash(left_phrase, 1)
                                            self.add_hypernym_to_nodes(left_phrase, "", right_phrase)

                                        break

                        if (word_index+1) < split_len:
                            two_gram = str_split[word_index] + " " + str_split[word_index+1]

                            two_gram = two_gram.rstrip()

                            if self.check_patterns(two_gram):

                                pos_list = self.pos(line)

                                for index in range(0, len(pos_list)):
                                    if isinstance(pos_list[index], tuple):
                                        if (pos_list[index][0]+" "+pos_list[index+1][0]) == two_gram:
                                            left_phrase = self.find_phrase_left(pos_list, index)
                                            right_phrase = self.find_phrase_right(pos_list, index)

                                            # check left
                                            if self.check_hyps(left_phrase):
                                                self.add_hypernym_to_hash(right_phrase, 1)
                                                self.add_hypernym_to_nodes(right_phrase, left_phrase, "")


                                            # check right
                                            if self.check_hyps(right_phrase):
                                                self.add_hypernym_to_hash(left_phrase, 1)
                                                self.add_hypernym_to_nodes(left_phrase, "", right_phrase)

                                            break

                        if (word_index+2) < split_len:
                            three_gram = str_split[word_index] + " " + str_split[word_index + 1] + " " + str_split[word_index + 2]

                            three_gram = three_gram.rstrip()

                            if self.check_patterns(three_gram):

                                pos_list = self.pos(line)

                                for index in range(0, len(pos_list)):
                                    if isinstance(pos_list[index], tuple):
                                        if (pos_list[index][0]+" "+pos_list[index+1][0]+" "+pos_list[index+2][0]) == three_gram:
                                            left_phrase = self.find_phrase_left(pos_list, index)
                                            right_phrase = self.find_phrase_right(pos_list, index)

                                            # check left
                                            if self.check_hyps(left_phrase):
                                                self.add_hypernym_to_hash(right_phrase, 1)
                                                self.add_hypernym_to_nodes(right_phrase, left_phrase, "")


                                            # check right
                                            if self.check_hyps(right_phrase):
                                                self.add_hypernym_to_hash(left_phrase, 1)
                                                self.add_hypernym_to_nodes(left_phrase, "", right_phrase)

                                            break

            self.rank_nodes()
        # evaluations

    def find_phrase_left(self, pos_list, index):
        for i in range(1, index+1):
            if not isinstance(pos_list[index - i], tuple):
                np = ''
                for j in range(0, pos_list[index - i].__len__):
                    np += (pos_list[index-i][j][0] + ' ')
                np = np.rstrip()

                return np

    def find_phrase_right(self, pos_list, index):
        for i in range(index, len(pos_list)):
            if not isinstance(pos_list[i], tuple):
                np = ''
                for j in range(0, pos_list[i].__len__):
                    np += (pos_list[i][j][0] + ' ')
                np = np.rstrip()

                return np

    def pos(self, sentence):
        tokenized = nltk.word_tokenize(sentence)
        return nltk.pos_tag(tokenized)


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

        parent_set = set()

        child_stack = []

        parent_set.add(phrase.phrase)

        for parent in self.node_map[phrase].parent_set:
            parent_set.add(parent.phrase)

        for child in self.node_map[phrase].child_set:
            if child.phrase in parent_set:
                return True
            else:
                child_stack.append(child)

        while len(child_stack) != 0:

            current_child = child_stack.pop()

            for child in self.node_map[current_child].child_set:
                if child.phrase in parent_set:
                    return True
                else:
                    parent_set.add(child.phrase)
                    child_stack.append(child)

        return False


    def rank_nodes(self):
        # Finds all nodes with 0 rank and adds to stack
        node_stack = []

        for node in self.node_map:
            if node.rank == 0:
                node_stack.append(node)

        while len(node_stack) != 0:

            current_node = node_stack.pop()

            for parent in current_node.parent_set():

                if current_node.rank == 0:
                    parent.rank += 1
                else:
                    parent.rank += current_node.rank

                node_stack.append(parent)


# Used for ranking hypernyms found in text
class HyperNode:

    def __init__(self, phrase):
        self.rank = 0
        self.phrase = phrase
        self.child_set = set() # A set of phrases
        self.parent_set = set() # A set of phrases

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

