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


def ON(led):
    led.on()


def onPair(ledA, ledB):
    ledA.on()
    ledB.on()


def offPair(ledA, ledB):
    ledA.off()
    ledB.off()


def OFF(led):
    led.off()


def switchCommand(command, id):
    if command == 'ON':
        print(command, id)
        if id == 'ONEA':
            ON(oneA[1])
            OFF(oneA[0])
        if id == 'ONEB':
            ON(oneB[1])
            OFF(oneB[0])
        if id == 'TWOA':
            ON(twoA[1])
            OFF(twoA[0])
        if id == 'TWOB':
            ON(twoB[1])
            OFF(twoB[0])
    if command == 'OFF':
        print(command, id)
        if id == 'ONEA':
            OFF(oneA[1])
            ON(oneA[0])
        if id == 'ONEB':
            OFF(oneB[1])
            ON(oneB[0])
        if id == 'TWOA':
            OFF(twoA[1])
            ON(twoA[0])
        if id == 'TWOB':
            OFF(twoB[1])
            ON(twoB[0])
    if command == "ALL":
        closeAll()


while True:
    client, address = s.accept()
    print("Connection from {} has been established.".format(address))
    msg = client.recv(BUFFER)
    msg = msg.decode()
    command, id = msg.split(";")
    switchCommand(command, id)
    client.close()
