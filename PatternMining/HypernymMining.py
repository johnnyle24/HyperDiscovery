import nltk
import re


class HypernymMining:

    def __init__(self, file_name):
        self.hyp_hashes = dict()
        self.pat_hashes = dict()

        self.test_hashes = set()

        with open(file_name, 'r') as file:
            for line in file:
                str_split = line.lower().split('concept')
                phrase = str_split[0].rstrip()
                self.test_hashes.add(phrase)

        self.ordered_hashes = []

        self.ordered_found_hashes = []

        self.ordered_found_strings = []

        self.node_map = dict()

        self.found_hypernyms = set()

    # Extracts hypernym phrases from a body of text such as PubMed
    def extract_hypernyms(self, file_name):

        if len(self.pat_hashes) == 0:
            print("No patterns have been added.")
        else:
            with open(file_name, 'r') as file:
                for count, line in enumerate(file):

                    print(count)

                    # if count == 100:
                    #     break

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

                                        if left_phrase == "" or right_phrase == "":
                                            continue

                                        # check left
                                        if self.check_hyps(left_phrase):
                                            self.add_hypernym_to_hash(right_phrase, 1)
                                            self.add_hypernym_to_nodes(right_phrase, left_phrase, "")

                                            self.found_hypernyms.add(right_phrase)

                                        # check right
                                        if self.check_hyps(right_phrase):
                                            self.add_hypernym_to_hash(left_phrase, 1)
                                            self.add_hypernym_to_nodes(left_phrase, "", right_phrase)

                                            self.found_hypernyms.add(left_phrase)

                                        break

                        if (word_index+1) < split_len:
                            two_gram = str_split[word_index] + " " + str_split[word_index+1]

                            two_gram = two_gram.rstrip()

                            if self.check_patterns(two_gram):

                                pos_list = self.pos(line)

                                for index in range(0, len(pos_list)-1):
                                    if isinstance(pos_list[index], tuple) and isinstance(pos_list[index+1], tuple):
                                        try:
                                            if (pos_list[index][0]+" "+pos_list[index+1][0]) == two_gram:
                                                left_phrase = self.find_phrase_left(pos_list, index)
                                                right_phrase = self.find_phrase_right(pos_list, index)

                                                if left_phrase == "" or right_phrase == "":
                                                    continue

                                                # check left
                                                if self.check_hyps(left_phrase):
                                                    self.add_hypernym_to_hash(right_phrase, 1)
                                                    self.add_hypernym_to_nodes(right_phrase, left_phrase, "")

                                                    self.found_hypernyms.add(right_phrase)


                                                # check right
                                                if self.check_hyps(right_phrase):
                                                    self.add_hypernym_to_hash(left_phrase, 1)
                                                    self.add_hypernym_to_nodes(left_phrase, "", right_phrase)

                                                    self.found_hypernyms.add(left_phrase)

                                                break
                                        except:
                                            pass

                        if (word_index+2) < split_len:
                            three_gram = str_split[word_index] + " " + str_split[word_index + 1] + " " + str_split[word_index + 2]

                            three_gram = three_gram.rstrip()

                            if self.check_patterns(three_gram):

                                pos_list = self.pos(line)

                                for index in range(0, len(pos_list)-2):
                                    if isinstance(pos_list[index], tuple) and isinstance(pos_list[index+1], tuple) and isinstance(pos_list[index+2], tuple):
                                        if (pos_list[index][0]+" "+pos_list[index+1][0]+" "+pos_list[index+2][0]) == three_gram:
                                            left_phrase = self.find_phrase_left(pos_list, index)
                                            right_phrase = self.find_phrase_right(pos_list, index)

                                            if left_phrase == "" or right_phrase == "":
                                                continue

                                            # check left
                                            if self.check_hyps(left_phrase):
                                                self.add_hypernym_to_hash(right_phrase, 1)
                                                self.add_hypernym_to_nodes(right_phrase, left_phrase, "")

                                                self.found_hypernyms.add(right_phrase)


                                            # check right
                                            if self.check_hyps(right_phrase):
                                                self.add_hypernym_to_hash(left_phrase, 1)
                                                self.add_hypernym_to_nodes(left_phrase, "", right_phrase)

                                                self.found_hypernyms.add(left_phrase)

                                            break

            self.rank_nodes()
            self.print_found_hypernyms()
            self.print_ordered_hypernyms()
            self.unordered_score()
        # evaluations

    def unordered_score(self):
        found_score = 0

        overall_score = 0

        total_hypernyms = len(self.test_hashes)

        for key in self.test_hashes:
            if key in self.found_hypernyms:
                found_score += 1

            if key in self.hyp_hashes:
                overall_score += 1

        print("Unordered Found Score: " + str(float(found_score)/float(total_hypernyms)))

        print("Unordered Overall Score: " + str(float(overall_score) / float(total_hypernyms)))

    def ordered_score(self, file_name):

        scores = []

        with open(file_name, 'r') as file:
            for line in file:
                line = line.rstrip()
                str_split = re.split(r'\t+', line)
                while len(self.ordered_hashes) < len(str_split):
                    hash = set()
                    self.ordered_hashes.append(hash)
                for index, token in enumerate(str_split):
                    self.ordered_hashes[index].add(token)

        for line in self.ordered_found_strings:
            str_split = re.split(r'\t+', line)
            while len(self.ordered_found_hashes) < len(str_split):
                hash = set()
                self.ordered_found_hashes.append(hash)
            for index, token in enumerate(str_split):
                self.ordered_found_hashes[index].add(token)

        for index, hash_s in enumerate(self.ordered_hashes):
            scores.append(float(0))
            if index >= len(self.ordered_found_hashes):
                break
            for token in hash_s:
                if token in self.ordered_found_hashes[index]:
                    scores[index] += float(1)
            scores[index] = scores[index]/float(len(hash_s))

        average_score = float(0)

        for index, score in enumerate(scores):
            print("Rank: " + str(index) + ", Score: " + str(score))
            average_score += score

        average_score = average_score/float(len(scores))

        print("Average Score: " + str(average_score))

    def print_found_hypernyms(self):
        print("\n\n\n")
        for hyp in self.found_hypernyms:
            print(hyp)

    def print_ordered_hypernyms(self):
        unsorted_nodes = []

        for key in self.node_map:
            self.node_map[key].visited_rank = False
            unsorted_nodes.append(self.node_map[key])

        sorted_nodes = sorted(unsorted_nodes, key=lambda node: node.rank, reverse=True)

        # for node in sorted_nodes:
        #     print(node.phrase)
        #     print(node.rank)
        #     print("Phrase: " + node.phrase + ", Rank: ", + node.rank)

        print("\n\n\n-------------------------------------------------\n\n\n")

        for node in sorted_nodes:
            hypernym_string = ""

            self.print_hypernym_recursively(node, hypernym_string)

    def print_hypernym_recursively(self, current_node, string):

        if len(current_node.child_set) == 0 or current_node.visited_rank:
            string = string.rstrip()
            if len(string) != 0:
                print(string)
                self.ordered_found_strings.append(string)
            return

        string += (current_node.phrase + "\t")

        current_node.visited_rank = True

        for child in current_node.child_set:
            self.print_hypernym_recursively(self.node_map[child], string)

    def find_phrase_left(self, pos_list, index):
        for i in range(1, index+1):
            if not isinstance(pos_list[index - i], tuple):
                np = ''
                for j in range(0, len(pos_list[index - i])):
                    np += (pos_list[index-i][j][0] + ' ')
                np = np.rstrip()

                return np

        return ""

    def find_phrase_right(self, pos_list, index):
        for i in range(index, len(pos_list)):
            if not isinstance(pos_list[i], tuple):
                np = ''
                for j in range(0, len(pos_list[i])):
                    np += (pos_list[i][j][0] + ' ')
                np = np.rstrip()

                return np

        return ""

    def pos(self, sentence):
        tokenized = nltk.word_tokenize(sentence)

        taggedSent = nltk.pos_tag(tokenized)
        grammar = 'NP: {<DT>?<JJ>*<NNS>*<NN>*(<NNS>|<NN>)+}'
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(taggedSent)
        return result


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
                if len(str_split) == 2:
                    phrase = str_split[0].rstrip()
                    frequency = int(str_split[1].rstrip('\n'))
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
                self.node_map[phrase].add_child(self.node_map[child])
                self.node_map[phrase].rank += 1
            if parent != "":
                self.node_map[phrase].add_parent(self.node_map[parent])
        else:
            node = HyperNode(phrase)
            if child != "":
                node.add_child(self.node_map[child])
                node.rank += 1
            if parent != "":
                node.add_parent(self.node_map[parent])

            self.node_map[phrase] = node

    def check_for_circular_dep(self, node):

        parent_set = set()

        child_stack = []

        parent_set.add(node.phrase)

        for parent in self.node_map[node].parent_set:
            parent_set.add(parent.phrase)

        for child in self.node_map[node].child_set:
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

        for phrase in self.node_map:
            if self.node_map[phrase].rank == 0:
                node_stack.append(self.node_map[phrase])

        while len(node_stack) != 0:

            current_node = node_stack.pop()

            for parent in current_node.parent_set:

                if current_node.rank == 0:
                    self.node_map[parent].rank += 1
                else:
                    self.node_map[parent].rank += current_node.rank

                current_node.visited_rank = True

                if not self.node_map[parent].visited_rank:
                    node_stack.insert(0, self.node_map[parent])


# Used for ranking hypernyms found in text
class HyperNode:

    def __init__(self, phrase):
        self.rank = 0
        self.phrase = phrase
        self.child_set = set() # A set of phrases
        self.parent_set = set() # A set of phrases
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

