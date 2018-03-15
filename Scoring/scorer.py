

class Scoring:

    def __init__(self, predictionFileName, goldFileName):
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
        for i in range(len(self.gold)):

            gold = self.gold[i].replace('\n', '').split('\t')
            predicted = self.predictions[i].replace('\n', '').split('\t')

            for j in range(len(gold)):

                if j < len(predicted) and predicted[j] in gold: #gold[j] == predicted[j]:
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

if __name__ == '__main__':

    s = Scoring('../SemEval2018-Task9/training/gold/2A.medical.training.gold.txt',
                '../SemEval2018-Task9/training/gold/2A.medical.training.gold.txt')

    # s = Scoring('../Misc/test.pred.txt',
    #             '../Misc/test.gold.txt')

    print(s.recall())
    print(s.precision())
    print(s.fScore())