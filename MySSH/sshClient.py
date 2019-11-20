import socket as s
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES,PKCS1_OAEP
#from Cryptodome.Random import get_random_bytes


if __name__ == "__main__":
    #Establishing connection
    #serverPort = int(input("Enter port number: "))
    #serverName = input("Enter Server address: ")
    serverPort = int(input('Enter port number: '))
    serverName = '127.0.0.1'
    user = input('User Name: ')
    clientSocket = s.socket(s.AF_INET,s.SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))

    while True:
        msg = input('> ')
        clientSocket.send(msg.encode())
        #print('receiving...')
        output = clientSocket.recv(4096).decode()
        if('cd' not in msg and output == ''):
            break
        if(len(output) > 0):
            print(output)
            output = ''
    #clientSocket.close()


