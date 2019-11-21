import socket as s
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
#from Cryptodome.Random import get_random_bytes


def authenticate(clientSocket, user):
	clientSocket.send(user.encode())
	out = int(clientSocket.recv(4096).decode())
	if out:
		print('Authenticating')
		key = RSA.generate(2048)
		clientSocket.send(key.publickey().export_key())
		enc_sk = clientSocket.recv(4096)
		#print(enc_sk)
		decryptor = PKCS1_OAEP.new(key)
		sk = decryptor.decrypt(enc_sk)		
		return sk
	else:
		print('Invalid UserName')
		return 0


def sendMessage(clientSocket, msg, sk):
	encryptor = AES.new(sk, AES.MODE_EAX)
	enc_msg, tag = encryptor.encrypt_and_digest(msg.encode())
	#print('sending\n',encryptor.nonce + b'|$' + tag + b'|$' + enc_msg)
	clientSocket.sendall(encryptor.nonce + b'|$' + tag + b'|$' + enc_msg)


def receiveMessage(clientSocket, sk):
	nonce,tag,enc_msg =[i for i in clientSocket.recv(4096).strip(b'|$').split(b'|$')]
	#print(nonce)
	decryptor = AES.new(sk, AES.MODE_EAX, nonce)
	msg = decryptor.decrypt(enc_msg)
	return msg.decode()


if __name__ == "__main__":
    # Establishing connection
    #serverPort = int(input("Enter port number: "))
    #serverName = input("Enter Server address: ")
	serverPort = int(input('Enter port number: '))
	serverName = '127.0.0.1'
	user = input('User Name: ')
	clientSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
	clientSocket.connect((serverName, serverPort))
	sk = authenticate(clientSocket, user)
	if not sk == 0:
		while True:
			msg = input('> ')
			#print('Sending ',msg)
			sendMessage(clientSocket, msg, sk)
			#clientSocket.send(msg.encode())
			#print('receiving...')
			if msg.lower() == 'exit':
				excess = clientSocket.recv(4096)
				break
			output = receiveMessage(clientSocket, sk)
			#output = clientSocket.recv(4096).decode()
			if('cd' not in msg and output == ''):
				break
			if(len(output) > 0 and output != 'NULL' ):
				print(output)
				output = ''
			else:
				print()
    # clientSocket.close()
