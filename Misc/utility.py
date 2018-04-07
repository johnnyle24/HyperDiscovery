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

def main():
    print_concept_sentences("../SemEval2018-Task9/training/data/2A.medical.training.data.txt")


if __name__ == '__main__':
    main()

