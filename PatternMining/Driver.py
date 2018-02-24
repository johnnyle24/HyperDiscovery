from HypernymMining import HypernymMining
from patternMining import PatternMining


def main():

    file_name = "../Data/2A_med_pubmed_POITagged1.txt"

    print("Pattern mining...")
    # pattern_mining = PatternMining()

    print("...")
    # pattern_mining.GetPairs()

    print("Hypernym hashing...")
    hyp = HypernymMining()
    print("...")
    hyp.hash_patterns("../MinedData/Patterns.txt")
    print("...")
    hyp.hash_hypernyms("../SemEval2018-Task9/training/data/2A.medical.training.data.txt")

    print("Hypernym extraction...")
    hyp.extract_hypernyms(file_name)

    print("Extraction Complete.")


if __name__ == '__main__':
    main()
