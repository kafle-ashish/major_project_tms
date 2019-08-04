
class DataQueue:
    def __init__(self):
        self.priority = {'e': 0, 'w': 1, 'n': 2, 's': 3}
        self.e = {'up': [0, 0], 'down': [0, 0]}
        self.w = self.e
        self.n = self.e
        self.s = self.e

    def update(data):
        self.e['up'][0] = data['east']['up']['count']
        self.e['up'][1] = data['east']['up']['density']
        self.e['down'][0] = data['east']['down']['count']
        self.e['down'][1] = data['east']['down']['density']

        self.w['up'][0] = data['east']['up']['count']
        self.w['up'][1] = data['east']['up']['density']
        self.w['down'][0] = data['east']['down']['count']
        self.w['down'][1] = data['east']['down']['density']

        self.n['up'][0] = data['east']['up']['count']
        self.n['up'][1] = data['east']['up']['density']
        self.n['down'][0] = data['east']['down']['count']
        self.n['down'][1] = data['east']['down']['density']

        self.s['up'][0] = data['east']['up']['count']
        self.s['up'][1] = data['east']['up']['density']
        self.s['down'][0] = data['east']['down']['count']
        self.s['down'][1] = data['east']['down']['density']

    def setPriority(self):
        temp = {}

    def get(self):
        pass
