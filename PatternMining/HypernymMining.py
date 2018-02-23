

class HypernymMining:

    def __init__(self):
        self.hyp_hashes = dict()
        self.pat_hashes = dict()
        
        self.hyp_nodes = dict()

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

                        if self.check_patterns(one_gram):

                            self.add_hypernym(str_split[word_index-1], 1)
                            self.add_hypernym(str_split[word_index+1], 1)

                        if (word_index+1) < split_len:
                            two_gram = str_split[word_index] + " " + str_split[word_index+1]

                            if self.check_patterns(two_gram):
                                self.add_hypernym(str_split[word_index - 1], 1)
                                self.add_hypernym(str_split[word_index + 2], 1)

                        if (word_index+2) < split_len:
                            three_gram = str_split[word_index] + " " + str_split[word_index + 1] + " " + str_split[word_index + 2]

                            if self.check_patterns(three_gram):
                                self.add_hypernym(str_split[word_index - 1], 1)
                                self.add_hypernym(str_split[word_index + 3], 1)


    def check_patterns(self, phrase):
        if phrase in self.pat_hashes:
            return True
        else:
            return False


    # Extracts the hypernyms STORED in a hypernyms.txt file tagged with concept
    def hash_hypernyms(self, file_name):
        with open(file_name, 'r') as file:
            for line in file:
                str_split = line.lower().split('concept')
                phrase = str_split[0].rstrip()
                self.add_hypernym(phrase, 1)

    # Adds the hypernyms to the hashmap and adjusts number of times found if necessary
    def add_hypernym(self, phrase, frequency):
        if phrase in self.hyp_hashes:
            self.hyp_hashes[phrase] += frequency
        else:
            self.hyp_hashes[phrase] = frequency

    # Extracts the patterns STORED in a patterns.txt file paired with its frequency
    def hash_patterns(self, file_name):
        with open(file_name, 'r') as file:
            for line in file:
                str_split = line.lower().split('=')
                phrase = str_split[0].rstrip()
                frequency = int(str_split[1])
                self.add_pattern(phrase, frequency)

    # Add the patterns to the hashmap and adjusts the number of times found if necessary
    def add_pattern(self, phrase, frequency):
        if phrase in self.pat_hashes:
            self.pat_hashes[phrase] += frequency
        else:
            self.pat_hashes[phrase] = frequency


# Used for ranking hypernyms found in text
class HyperNodes:

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

