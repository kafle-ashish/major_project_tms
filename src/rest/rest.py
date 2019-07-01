import requests as r


class Rest:
    def __init__(self, method="GET", url="https://tmsbackend.herokuapp.com"):
        self.method = method
        self.url = url

    def get(params=None):
        resp = r.get(self.url, params)
        return resp.content

    def post(payload):
        resp = r.post(self.url, data=payload)
        return resp.content

    def put(payload):
        resp = r.put(self.url, data=payload)
        return resp.content

    def update(payload):
        if self.method == "POST":
            return self.post(payload)
        if self.method == "PUT":
            return self.put(payload)
        return self.get()

    def method(method="POST"):
        self.method = method
        return "Changed method to {}.".format(method)
