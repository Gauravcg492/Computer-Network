import socket as s
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES,PKCS1_OAEP
#from Cryptodome.Random import get_random_bytes

def authenticate(clientSocket,user):
	clientSocket.send(user.encode())
	out = int(clientSocket.recv(4096).decode())
	if out:
		print('Authenticating')
		enc_sk = clientSocket.recv(4096).decode()
		return enc_sk
	else:
		print('Invalid UserName')
		return 0

def sendMessage(clientSocket,msg,sk):
	encryptor = AES.new(sk,AES.MODE_EAX)
	enc_msg,tag = encryptor.encrypt_and_digest(msg.encode())
	[clientSocket.send(x) for x in (encryptor.nonce,tag,enc_msg)]

def receiveMessage(clientSocket,sk):
	nonce = clientSocket.recv(4096)
	tag = clientSocket.recv(4096)
	enc_msg = clientSocket.recv(4096)
	decryptor = AES.new(sk,AES.MODE_EAX,nonce)
	msg = decryptor.decrypt_and_verify(enc_msg,tag)
	return msg.decode()

if __name__ == "__main__":
    #Establishing connection
    #serverPort = int(input("Enter port number: "))
    #serverName = input("Enter Server address: ")
    serverPort = int(input('Enter port number: '))
    serverName = '127.0.0.1'
    user = input('User Name: ')
    clientSocket = s.socket(s.AF_INET,s.SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
	sk = authenticate(clientSocket,user)
	if not sk == 0:
		while True:
		    msg = input('> ')
		    sendMessage(clientSocket,msg,sk)
		    #clientSocket.send(msg.encode())
		    #print('receiving...')
		    output = clientSocket.recv(4096).decode()
		    if('cd' not in msg and output == ''):
		        break
		    if(len(output) > 0):
		        print(output)
		        output = ''
    #clientSocket.close()


