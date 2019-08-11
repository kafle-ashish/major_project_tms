class Watcher:
    def __init__(self):
        self.FUTURE = 0
        self.AWARD = []
        self.TIME = 45
        self.buffer = {'1a': [0, 0], '2a': [0, 0], '1b': [0, 0], '2b': [0, 0]}
        self.average = self.buffer
        self.GO = ['2a', '2b']
        self.STOP = ['1a', '1b']
        self.iters = 0

    def update(self, data):
        average(data)
        self.buffer[data['name']][0] = data['count']
        self.buffer[data['name']][1] = data['density']
        self.iters += 1

    def average(self, data):
        self.average[data['name']][0] += data['count']
        self.average[data['name']][1] += data['density']

    def getStatus(self):
        for key, values in self.average:
            self.average[key][0] = values[0]/iters
            self.average[key][1] = values[1]/iters
        compare()
        return self.average, self.AWARD, self.FUTURE, self.GO

    def compare(self):
        count_GO = self.average[self.GO[0]][0] + self.average[self.GO[1]][0]
        count_STOP = self.average[STOP[0]][0] + self.average[STOP[1]][0]
        if count_GO > count_STOP:
            self.AWARD = self.GO
            self.FUTURE = 15
        else:
            self.FUTURE = 0
            self.AWARD = []

        self.GO, self.STOP = self.STOP, self.GO
