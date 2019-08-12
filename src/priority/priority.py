class Watcher:
    def __init__(self):
        self.countOne = 0
        self.countTwo = 0
        self.iters = 0
        self.FUTURE = 0
        self.AWARD = []
        self.GO = ['2a', '2b']
        self.STOP = ['1a', '1b']
        self.avg = {'1a': [0, 0], '2a': [0, 0], '1b': [0, 0], '2b': [0, 0]}

    def update(self, data):
        self.avg[data['name']][0] = data['count']
        self.avg[data['name']][1] += data['density']
        if data['density'] is not 0:
            self.iters += 1

    def getStatus(self):
        for key, values in self.avg.items():
            self.avg[key][0] = values[0]
            if self.iters > 0:
                self.avg[key][1] = values[1]/self.iters
            else:
                self.avg[key][1] = values[1]
        self.avg['1a'][0] = abs(self.countOne - self.avg['1a'][0])
        self.avg['2a'][0] = abs(self.countTwo - self.avg['2a'][0])
        self.compare()
        self.iters = 0
        self.countOne += self.avg['1a'][0]
        self.countTwo += self.avg['2a'][0]
        copy = self.avg
        self.avg = {'1a': [0, 0], '2a': [0, 0], '1b': [0, 0], '2b': [0, 0]}
        return copy, self.AWARD, self.FUTURE, self.GO

    def compare(self):
        count_GO = self.avg[self.GO[0]][0] + self.avg[self.GO[1]][0]
        count_STOP = self.avg[self.STOP[0]][0] + self.avg[self.STOP[1]][0]
        if count_GO > count_STOP:
            self.AWARD = self.GO
            self.FUTURE = -4
        else:
            self.FUTURE = 0
            self.AWARD = []

        self.GO, self.STOP = self.STOP, self.GO
