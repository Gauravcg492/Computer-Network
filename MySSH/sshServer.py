import socket as s
import os
import subprocess
import getpass
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Random import get_random_bytes


def authenticate(clientSocket, sessionKey, username):
	user = clientSocket.recv(4096).decode()
	#print(user,username)
	if(username == user):
		clientSocket.send('1'.encode())
		publicKey = clientSocket.recv(4096)
		publicKey = RSA.import_key(publicKey)
		encrytor = PKCS1_OAEP.new(publicKey)
		encrypted_SK = encrytor.encrypt(sessionKey)
		#print(encrypted_SK)
		clientSocket.send(encrypted_SK)
		return 1
	else:
		clientSocket.send('0'.encode())
		return 0


def sendMessage(clientSocket, msg, sk):
	encryptor = AES.new(sk, AES.MODE_EAX)
	enc_msg, tag = encryptor.encrypt_and_digest(msg)
	#print('sending\n',encryptor.nonce + b'|$' + tag + b'|$' + enc_msg)
	clientSocket.sendall(encryptor.nonce + b'|$' + tag + b'|$' + enc_msg)


def receiveMessage(clientSocket, sk):
    nonce,tag,enc_msg =[i for i in clientSocket.recv(4096).strip(b'|$').split(b'|$')]
    decryptor = AES.new(sk, AES.MODE_EAX, nonce)
    msg = decryptor.decrypt(enc_msg)
    return msg.decode()


if __name__ == "__main__":
	# setting server
	serverPort = int(input('Enter the port number: '))
	server = s.socket(s.AF_INET, s.SOCK_STREAM)
	server.bind(('', serverPort))
	server.listen(5)
	userName = getpass.getuser()
	while True:
		clientSocket, address = server.accept()
		sessionKey = get_random_bytes(16)
		if authenticate(clientSocket, sessionKey, userName):
			while True:
				#print('Receiving..')
				cmd = receiveMessage(clientSocket, sessionKey)
				output = b'NULL'
				if(cmd.lower() == 'exit'):
					break
				if(len(cmd) >= 2 and 'cd' == cmd[:2]):
					if cmd == 'cd':
						#print('calling cd here')
						os.chdir(os.path.expanduser('/'))
					else:
						#print('changing directory')
						try:
							os.chdir(cmd[3:])
						except:
							output = ('FileNotFoundError: [Errno 2] No such file or directory: ' + cmd[3:])
				elif len(cmd) > 0:
					#print('calling systems')
					#print('Executing cmd ',cmd)
					output = subprocess.check_output(cmd, shell=True)
				if output == '':
					output = b'NULL'
				#print('sending ', output)
				#clientSocket.send(output)
				sendMessage(clientSocket,output,sessionKey)
		else:
			clientSocket.send('Unauthorized User'.encode())
		clientSocket.close()
