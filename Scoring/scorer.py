from Scoring import build_score_file as score
from nltk.stem.porter import *

class Scoring:

    def __init__(self, predictionFileName=None, goldFileName=None):
        if predictionFileName is None or goldFileName is None:
            print('Filenames cannot be None')
            return
        self.predictionFileName = predictionFileName
        self.goldFileName = goldFileName
        self.predictions = None
        self.gold = None
        self.rec = None
        self.prec = None
        self.stemmer = PorterStemmer()


        with open(self.predictionFileName, 'r') as f:
                self.predictions = f.readlines()

        with open(self.goldFileName, 'r') as f:
                self.gold = f.readlines()

        if len(self.gold) != len(self.predictions):
            raise Exception('Length of gold and predictions do not match')

    def recall(self):
        correct = 0
        tot = 0
        count = 0
        visited = set()
        for i in range(len(self.gold)):

            pred = self.predictions[i]

            if self.predictions[i].replace('\n', '') == 'None':
                count += 1
                continue

            gold = self.gold[i].replace('\n', '').split('\t')
            predicted = self.predictions[i].replace('\n', '').split('\t')

            gold_tokenized = []

            for g in gold:
                r = [self.stemmer.stem(t).lower() for t in g.split()]
                gold_tokenized.append(set(r))

            predicted_tokenized = []
            for p in predicted:
                r = [self.stemmer.stem(t).lower() for t in p.split()]
                predicted_tokenized.append(set(r))


            for pred in predicted_tokenized:

                for gold_val in gold_tokenized:

                    for g in gold_val:
                        if g in pred and g not in visited:
                            visited.add(g)
                            correct += 1

            tot += len(gold)

        if tot == 0:
            return 0

        self.rec = correct / tot
        return self.rec

    def precision(self):
        correct = 0
        tot = 0
        visited = set()
        for i in range(len(self.gold)):

            gold = self.gold[i].replace('\n', '').split('\t')
            predicted = self.predictions[i].replace('\n', '').split('\t')

            gold_tokenized = []

            for g in gold:
                r = [self.stemmer.stem(t).lower() for t in g.split()]
                gold_tokenized.append(set(r))

            predicted_tokenized = []
            for p in predicted:
                r = [self.stemmer.stem(t).lower() for t in p.split()]
                predicted_tokenized.append(set(r))


            for pred in predicted_tokenized:

                for gold_val in gold_tokenized:

                    for g in gold_val:
                        if g in pred and g not in visited:
                            visited.add(g)
                            correct += 1

            tot += sum([len(p) for p in predicted])

        if tot == 0:
            return 0

        self.prec = correct / tot
        return self.prec

    def fScore(self):
        if self.rec is None:
            self.recall()
        if self.prec is None:
            self.precision()

        num = (self.prec * self.rec)
        denom = (self.prec + self.rec)

        return 0 if denom == 0 else 2 *  num / denom

def get_scores(data_file):
    # score.get_file(data_file, 'predictions.txt')

    # s = Scoring(data_file, 'predictions.txt')
    s = Scoring(predictionFileName='../MinedData/medical_hypernym_results_match.txt',
                goldFileName=data_file)

    return {'recall' : s.recall(),
            'precision' : s.precision(),
            'fscore' : s.fScore()}

if __name__ == '__main__':

    # score.get_file('../SemEval2018-Task9/training/gold/2A.medical.training.gold.txt', 'predictions.txt')

    # s = Scoring(predictionFileName='predictions.txt',
    #             goldFileName='../SemEval2018-Task9/training/gold/2A.medical.training.gold.txt')


    # s = Scoring(predictionFileName='../MinedData/medical_hypernym_results_match.txt',
    #             goldFileName='../SemEval2018-Task9/training/gold/2A.medical.training.gold.txt')

    s = Scoring(predictionFileName='../MinedData/medical_hypernym_results_match.txt',
                goldFileName='../SemEval2018-Task9/test/gold/2A.medical.test.gold.txt')

    # s = Scoring('../Misc/test.pred.txt',
    #             '../Misc/test.gold.txt')

    # s = Scoring('../Data/Model/hypernyms.txt',
    #             '../SemEval2018-Task9/training/gold/2B.music.training.gold.txt')

    print('Recall: {0}'.format(s.recall()))
    print('Precision: {0}'.format(s.precision()))
    print('F Score: {0}'.format(s.fScore()))