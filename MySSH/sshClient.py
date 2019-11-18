from socket import *


if __name__ == "__main__":
    #Establishing connection
    serverPort = int(input("Enter port number: "))
    serverName = input("Enter Server address: ")

    clientSocket = socket(AF_INET,SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    msg = input()
    clientSocket.send(msg.encode())
    msg = clientSocket.recv(4096)
    print(msg.decode())
    #clientSocket.close()


