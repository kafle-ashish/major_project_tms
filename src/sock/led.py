from sock import Sock

while True:
    data = input("Enter the command please: \n")
    conn = Sock(ip="192.168.43.144")
    conn.connect()
    conn.send(data)
    conn.disconnect()
    print("Sent data: ", data)
