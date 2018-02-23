

class HypernymMining:

    def __init__(self):
        self.hyp_hashes = dict()
        self.pat_hashes = dict()

    def parse(self):
        print("Not implemented yet")

    def hash_hypernyms(self, file_name):
        with open(file_name, 'r') as file:
            for line in file:
                str_split = line.lower().split('concept')
                phrase = str_split[0].rstrip()
                self.add_hypernym(phrase, 1)

    def add_hypernym(self, phrase, frequency):
        if phrase in self.hyp_hashes:
            self.hyp_hashes[phrase] += frequency
        else:
            self.hyp_hashes[phrase] = frequency

    def hash_patterns(self, file_name):
        with open(file_name, 'r') as file:
            for line in file:
                str_split = line.lower().split('=')
                phrase = str_split[0].rstrip()
                frequency = int(str_split[1])
                self.add_pattern(phrase, frequency)

    def add_pattern(self, phrase, frequency):
        if phrase in self.pat_hashes:
            self.pat_hashes[phrase] += frequency
        else:
            self.pat_hashes[phrase] = frequency
