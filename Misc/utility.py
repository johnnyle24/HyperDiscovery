import sys
import json

def print_concept_sentences(concept_file):

    concepts = set()

    hypernyms = {'malady','body structure','disease	vascular disease','disorder','illness	clinical finding',	'sickness',	'cardiopathy pathology', 'cardiovascular disease', 'pathological state', 'enlargement', 'dilatation', 'heart disease'
}

    with open(concept_file, 'r') as concept_file:
        for concept_line in concept_file:
            concept = concept_line.split("\t")

            concepts.add(concept[0])

        for i in range(0, 369):
            file = "../Data/2A_med_pubmed_tokenized/2A_med_pubmed_tokenized_{0}.txt".format(i)

            with open(file, 'r') as f:

                tokens = json.load(f)

                tokens_iter = iter(tokens)

                sentence = ""

                isValid = False

                for token in tokens_iter:
                    if type(token[0]) is str:
                        sentence += token[0] + " "
                        continue
                    else:
                        np = ""
                        for l in token:
                            np += l[0] + " "

                        np = np.rstrip()

                        if isValid:
                            print(sentence + np + "\n")
                            isValid = False

                        if np=="aneurysm":
                            isValid = True
                            sentence = np + " "

def count_zeroes(file):
    sum = 0

    with open(file, "r") as f:
        for l in f:
            if float(l) < 0.0001:
                sum += 1
        print(sum)

def find_percents_over(file, threshold):

    with open(file, "r") as f:
        for ind, l in enumerate(f):
            if float(l) > threshold:
                print("Index: " + str(ind+1) + ", Percent: " + l)

def main():
    # print_concept_sentences("../SemEval2018-Task9/training/data/2A.medical.training.data.txt")

    medical = "../MinedData/medical_hypernym_percents.txt"

    musical = "../MinedData/musical_hypernym_percents.txt"

    count_zeroes(musical)
    find_percents_over(musical, 0.5)

if __name__ == '__main__':
    main()

