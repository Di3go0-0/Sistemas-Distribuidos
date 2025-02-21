
import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverIP = "xxx.xxx.xx.xxx"


serverPort = 1234
clientSocket.connect((serverIP, serverPort))


while(1):
    message = input("Escribe: ")

    clientSocket.send(message.encode())

    res = clientSocket.recv(1024)

    print(f"Response: {res.decode()}")


clientSocket.close()