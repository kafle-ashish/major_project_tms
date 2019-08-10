import socket
import time
import pickle
from sock.led import Led

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 5005))
s.listen(5)

# green = Led(18)
red = Led('BOARD3')
# yellow = Led(13)

BUFFER = 100
while True:
    # now our endpoint knows about the OTHER endpoint.
    client, address = s.accept()
    print(f"Connection from {address} has been established.")

    # d = {1:"hi", 2: "there"}
    # msg = pickle.dumps(d)
    # msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
    msg = client.recv(BUFFER)
    msg = pickle.dumps(msg)
    if msg['status'] == 'ON':
        # green.on()
        red.on()
    else:
        # green.off()
        red.off()
    print(msg)
    # clientsocket.send(msg)
