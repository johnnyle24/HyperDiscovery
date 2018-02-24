from HypernymMining import HypernymMining
from patternMining import PatternMining


def main():

    # file_name = "../Data/2A_med_pubmed2/2A_med_pubmed_POITagged1.txt"

    # for i in range(10):
    file_name = "../Data/2A_med_pubmed_2/2A_med_pubmed_2_2.txt"

    #file_name = "../Data/2B_music_bioreviews_2_2.txt"

    print("Pattern mining...")
    # pattern_mining = PatternMining()

    print("...")
    # pattern_mining.GetPairs()

    print("Hypernym hashing...")
    hyp = HypernymMining("../SemEval2018-Task9/test/data/2A.medical.test.data.txt")
    print("...")
    hyp.hash_patterns("../MinedData/patterns.txt")

    # hyp.hash_patterns("../MinedData/suggestedPatterns.txt")
    print("...")
    hyp.hash_hypernyms("../SemEval2018-Task9/training/data/2A.medical.training.data.txt")

    print("Hypernym extraction...")
    hyp.extract_hypernyms(file_name)

    hyp.ordered_score("../SemEval2018-Task9/test/gold/2A.medical.test.gold.txt")

    print("Extraction Complete.")


if __name__ == '__main__':
    main()
