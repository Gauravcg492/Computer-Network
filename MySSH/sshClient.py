from socket import *


if __name__ == "__main__":
    #Establishing connection
    #serverPort = int(input("Enter port number: "))
    #serverName = input("Enter Server address: ")
    serverPort = 19999
    serverName = '127.0.0.1'
    clientSocket = socket(AF_INET,SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    while True:
        msg = input('> ')
        clientSocket.send(msg.encode())
        print('receiving...')
        output = clientSocket.recv(4096).decode()
        if('cd' not in msg and output == ''):
            break
        if(len(output) > 0):
            print(output)
            output = ''
    #clientSocket.close()


