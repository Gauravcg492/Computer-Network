import socket as s
import os
import subprocess
import getpass
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES,PKCS1_OAEP
from Cryptodome.Random import get_random_bytes


def authenticate(clientSocket,sessionKey,username):
	user = clientSocket.recv(4096).decode()
	if(username == user):
		clientSocket.send('Authenticating'.encode())
		publicKey = clientSocket.recv(4096).decode()
		encrytor = PKCS1_OAEP.new(publicKey)
		encrypted_SK = encrytor.encrypt(sessionKey)
		clientSocket.send(encrypted_SK)
	else:
		clientSocket.send('Invalid user'.decode())
		return 0


if __name__ == "__main__":
    #setting server
    serverPort = int(input('Enter the port number: '))
    server = s.socket(s.AF_INET,s.SOCK_STREAM)
    server.bind(('',serverPort))
    server.listen(5)
    userName = getpass.getuser()
    #print("listening: ")
    while True:
        clientSocket, address = server.accept()
        sessionKey = get_random_bytes(16)
        if authenticate(clientSocket,sessionKey,username):        
		    while True:
		        #print('Receiving..')
		        cmd = clientSocket.recv(4096).decode()
		        output = b'NULL'
		        if(cmd.lower() == 'exit'):
		            break
		        if(len(cmd) >= 2 and 'cd' == cmd[:2]):
		            if cmd == 'cd':
		                #print('calling cd here')
		                os.chdir(os.path.expanduser('/')+'/home/'+userName)
		            else:
		                print('changing directory')
		                try:
		                    os.chdir(cmd[3:])
		                except:
		                    output = 'FileNotFoundError: [Errno 2] No such file or directory: ' + cmd[3:]
		        elif len(cmd) > 0:
		            print('calling systems')
		            #cwd = os.getcwd()
		            #print(cwd)
		            output = subprocess.check_output(cmd,shell=True)
		        print('sending ',output)
		        clientSocket.send(output)
		else:
			clientSocket.send('Unauthorized User'.encode())
        clientSocket.close()
