import socket
import time
from gpiozero import LEDBoard
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.43.144", 5005))
s.listen(5)

oneA = LEDBoard(2, 3)
oneB = LEDBoard(4, 14)
twoA = LEDBoard(15, 18)
twoB = LEDBoard(17, 27)
leds = [oneA, oneB, twoA, twoB]

BUFFER = 50
print("Server started ...")


def closeAll():
    for led in leds:
        led[0].off()
        led[1].off()


def onPair(ledA, ledB):
    ledA.on()
    ledB.on()


def offPair(ledA, ledB):
    ledA.off()
    ledB.off()


def switchCommand(command, id):
    if command == 'ON':
        print(command, id)
        if id == 'ONE':
            closeAll()
            onPair(oneA[1], oneB[1])
            onPair(twoA[0], twoB[0])
        if id == "TWO":
            closeAll()
            onPair(oneA[0], oneB[0])
            onPair(twoA[1], twoB[1])
    if command == 'OFF':
        closeAll()


while True:
    client, address = s.accept()
    print("Connection from {} has been established.".format(address))
    msg = client.recv(BUFFER)
    msg = msg.decode()
    command, id = msg.split(";")
    switchCommand(command, id)
    client.close()
