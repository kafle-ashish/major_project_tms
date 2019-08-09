import socket
import pickle


class Sock:
    def __init__(self, ip='192.168.43.144', port=5005, buffer=20, header=10):
        self.TCP_IP = ip
        self.TCP_PORT = port
        self.BUFFER_SIZE = buffer
        self.HEADER_SIZE = header
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            return self.s.connect((self.TCP_IP, self.TCP_PORT))
        except Exception as e:
            return e

    def disconnect(self):
        try:
            return self.s.close()
        except Exception as e:
            return e

    def send(self, data):
        try:
            message = pickle.dumps(data)
            message = bytes(f"{len(msg):<{self.HEADER_SIZE}}", 'utf-8')+message
            self.s.send(message)
            data = self.s.recv(self.BUFFER_SIZE)
            return pickle.loads(data)
        except Exception as e:
            return e
