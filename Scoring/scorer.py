

class Scoring:

    def __init__(self, predictionFileName, goldFileName):
        self.predictionFileName = predictionFileName
        self.goldFileName = goldFileName
        self.predictions = None
        self.gold = None

    def recall(self):
        pass

    def precision(self):
        pass

    def fScore(self):
        pass

    def getPredictions(self):
        if self.predictions is None:
            with open(self.predictionFileName, 'r') as f:
                self.predictions = f.readlines()

    def getGold(self):
        if self.predictions is None:
            with open(self.predictionFileName, 'r') as f:
                self.predictions = f.readlines()

