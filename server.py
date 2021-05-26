import socket
import requests
import json
import os
import threading
import hashlib
HEADER = 64
# Choose a port that is free
PORT = 5050
DISCONNECT_MESSAGE = "!DISCONNECT"
# An IPv4 address is obtained
# for the server.
SERVER = socket.gethostbyname(socket.gethostname())

# Address is stored as a tuple
ADDRESS = (SERVER, PORT)

# the format in which encoding
# and decoding will occur
FORMAT = "utf-8"

# Lists that will contains
# all the clients connected to
# the server and their names.
clients, names = [], []

# Create a new socket for
# the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the address of the
# server to the socket
try:
	server.bind(ADDRESS)
except socket.error as e:
	print(str(e))

HashTable = {}

try:
	with open('data.json', 'r') as JSON:
	   HashTable = json.loads(JSON.read())
except:
	print("UNABLE TO LOAD DATA.JSON\n")

def sendCommand(conn):
	conn.send("USERNAME".encode(FORMAT))
	# 1024 represents the max amount of data that can be received (bytes)
	name = conn.recv(1024).decode(FORMAT)
			
	conn.send("PASSWORD".encode(FORMAT))
	# password = conn.recv(1024).decode(FORMAT)
	password = conn.recv(1024).decode(FORMAT)
	# append the name and client # to the respective list
			
	# password = hashlib.sha256(str.encode(password)).hexdigest() # Password hash using SHA256

	print(f"USERNAME is: {name}")
	print(f"PASSWORD is: {password}")
	# broadcast message
	# broadcastMessage(f"{name} has joined the chat!".encode(FORMAT))
			
	# conn.send("CONNECTED!!".encode(FORMAT))
	try:
		password = hashlib.sha256(str.encode(password)).hexdigest() # Password hash using SHA256
		print("HASH DONE")
		if name in HashTable:
			if HashTable[name] == password:
				conn.send("LOGIN SUCCESS".encode(FORMAT))
				print("Connected: ", name)
			else:
				conn.send("LOGIN FAIL".encode(FORMAT))
				print("Connection denied: ", name)
		else:
			conn.send("USER NOT FOUND".encode(FORMAT))
			print("User not found: ", name)
	except:
		print('LOGIN VERIFY FAIL')

# function to start the connection
def startChat():
	print("SERVER now is on " + SERVER)
	
	# listening for connections
	server.listen()
	
	while True:
		try:
			# accept connections and returns
			# a new connection to the client
			# and the address bound to it
			conn, addr = server.accept()
			
			sendCommand(conn)
			# Start the handling thread
			thread = threading.Thread(target = handle, args = (conn, addr))
			thread.start()
				# no. of clients connected
				# to the server
			print(f"ACTIVE CONNECTIONS: {threading.activeCount()-1}")

			

		except:
			print("Send Error...")

# method to handle the
# incoming messages

def handle(conn, addr):
	
	print(f"NEW CONNECTION: {addr}")
	connected = True
	
	while connected:
		# recieve message
		message = conn.recv(1024).decode(FORMAT)
		if message == DISCONNECT_MESSAGE:
			connected = False
			print(f"{DISCONNECT_MESSAGE}, {addr}")
			break
		elif message == 'LIVE SCORE':
			print("LIVE SCORE")
			try:
				apiRequest = requests.get("https://livescore-api.com/api-client/scores/live.json?key=lQNUCP8IbJHbBeIe&secret=1l6a2MSLYLk0ry8MpWG1MPKYzr9aGRpH")
				ScoreData = json.loads(apiRequest.content)
				for obj in ScoreData['data']['match']:
					# conn.send(f"{obj['+id']} + {obj['ht_score']} + {obj['ft_score']} + {obj['status']} \n".encode(FORMAT))
					conn.send("{:<8} {:<8} {:<20} {:<8} {:<20} \n".format(obj['id'], obj['status'], obj['home_name'], obj['score'], obj['away_name']).encode(FORMAT))

		# 		print("{:<8} {:<20}".format('USER','PASSWORD'))
        # for k, v in HashTable.items():
        #     label, num = k,v
        #     print("{:<8} {:<20}".format(label, num))
			except Exception as e:
				api = "Error..."
		else:
			# print(message)
			# broadcast message
			try:
				conn.send(message.encode(FORMAT))
			except:
				print("A error occured!")
				while not connected:
					try:
						conn.connect(addr)
						connected = True
					except socket.error as e:
						print(e)
				break
		
	# close the connection
	conn.close()

# method for broadcasting
# messages to the each clients

# call the method to
# begin the communication
startChat()
