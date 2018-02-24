from HypernymMining import HypernymMining
from patternMining import PatternMining


def main():

    file_name = ""

    print("Pattern mining...")
    # pattern_mining = PatternMining()

    print("...")
    # pattern_mining.GetPairs()

    print("Hypernym hashing...")
    hyp = HypernymMining()
    print("...")
    hyp.hash_patterns("../MInedData/Patterns.txt")
    print("...")
    hyp.hash_hypernyms("../SemEval2018-Task9/training/2A.medical.training.data.txt")

    print("Hypernym extraction...")
    hyp.extractHypernyms(file_name)

    print("Extraction Complete.")


if __name__ == '__main__':
    main()
