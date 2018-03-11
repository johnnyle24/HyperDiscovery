# from HypernymMining import HypernymMining
from patternMining import PatternMining
import sys

def main():

    # file_name = "../Data/2A_med_pubmed2/2A_med_pubmed_POITagged1.txt"

    for i in range(40):
        file_name = "../Data/2A_med_pubmed_2/2A_med_pubmed_2_{0}.txt".format(i)

        print("Pattern mining...")
        # pattern_mining = PatternMining()

        print("...")
        # pattern_mining.GetPairs()

        print("Hypernym hashing...")
        hyp = HypernymMining()
        print("...")
        hyp.hash_patterns("../MinedData/suggestedPatterns.txt")
        print("...")
        hyp.hash_hypernyms("../SemEval2018-Task9/training/data/2A.medical.training.data.txt")

        print("Hypernym extraction...")
        hyp.extract_hypernyms(file_name)

        print("Extraction Complete.")

def customRun(corpusFilename, conceptFile, patternsFile):

    file_name = corpusFilename

    print("Pattern mining...")
    # pattern_mining = PatternMining()

    print("...")
    # pattern_mining.GetPairs()

    print("Hypernym hashing...")
    hyp = HypernymMining()
    print("...")
    hyp.hash_patterns(patternsFile)
    print("...")
    hyp.hash_hypernyms(conceptFile)

    print("Hypernym extraction...")
    hyp.extract_hypernyms(file_name)

    print("Extraction Complete.")

if __name__ == '__main__':

    if len(sys.argv) <= 1:
        main()
    elif len(sys.argv) == 4:
        customRun(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print('Not right amount of parameters')
