from Scoring import build_score_file as score

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
        for i in range(len(self.gold)):

            pred = self.predictions[i]

            if self.predictions[i].replace('\n', '') == 'None':
                count += 1
                continue

            gold = self.gold[i].replace('\n', '').split('\t')
            predicted = self.predictions[i].replace('\n', '').split('\t')

            for j in range(len(gold)):
                if gold[j] in predicted:
                    correct += 1
                tot += 1
        self.rec = correct / tot
        return self.rec



    def precision(self):
        correct = 0
        tot = 0
        for i in range(len(self.gold)):

            gold = self.gold[i].replace('\n', '').split('\t')
            predicted = self.predictions[i].replace('\n', '').split('\t')

            for j in range(len(predicted)):

                if predicted[j] in gold: #gold[j] == predicted[j]:
                    correct += 1
                tot += 1

        self.prec = correct / tot
        return self.prec

    def fScore(self):
        if self.rec is None:
            self.recall()
        if self.prec is None:
            self.precision()

        return 2 * (self.prec * self.rec) / (self.prec + self.rec)

def get_scores(data_file):
    score.get_file(data_file, 'predictions.txt')

    s = Scoring(data_file, 'predictions.txt')

    return {'recall' : s.recall(),
            'precision' : s.precision(),
            'fscore' : s.fScore()}

if __name__ == '__main__':

    # score.get_file('../SemEval2018-Task9/training/gold/2A.medical.training.gold.txt', 'predictions.txt')

    s = Scoring(predictionFileName='predictions.txt',
                goldFileName='../SemEval2018-Task9/training/gold/2A.medical.training.gold.txt')

    # s = Scoring('../Misc/test.pred.txt',
    #             '../Misc/test.gold.txt')

    # s = Scoring('../Data/Model/hypernyms.txt',
    #             '../SemEval2018-Task9/training/gold/2B.music.training.gold.txt')

    print('recall: {0}'.format(s.recall()))
    print(s.precision())
    print(s.fScore())