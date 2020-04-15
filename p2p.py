import socket
import threading
import sys
import emoji
import os
connected = False
connection = ''

#A simple method waiting for input and then sending it to the
#socket connection
def sendMsg(sock):
				while True: 
						# send what is inputed via the socket
						theInput = input("")
						# I don't like using os._exit as it doesn't do any cleanup,
						# but this is the only way I can think of to terminate a 
						# process from a child thread
						if(theInput == "quit"):
								os._exit(0)
						print(emoji.emojize("You: " + theInput))
						sock.send(bytes(theInput, 'utf-8'))

#If we include more than just the program in the command line arguements,
#then we are trying to connect to an IP address				
if(len(sys.argv) > 1):
		try:
				# Our socket will be a TCP connection using IPv4
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.connect((sys.argv[1], 10000))
				connection = sys.argv[1]
				print("Connection Established")
				connected = True
		except:
				print("Could not connect at " + str(sys.argv[1]))
				
#if we either didn't include additional command line arguments or couldn't 
#reach that IP address, open up a connectable Socket
if not connected:
		# Our socket will be a TCP connection using IPv4
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# 0.0.0.0 to run "the server" on any configured IP address
		# arbitrary port choice, I went with 10000
		sock.bind(('0.0.0.0', 10000))

		# listen for a connection
		sock.listen(1)
		print("Listening for connection")

		c,a = sock.accept()

		# store our connection in connections
		connection = c
		# print who connected
		print(str(a[0]) + ":" + str(a[1]), "connected")
		
		# we make a new thread to allow us to send and receive at the same time
		#the target of our message is the connection we accepted
		inputThread = threading.Thread(target=sendMsg, args=(c,))
		# this allows us to close the program regardless of any extra threads open
		inputThread.daemon = True
		inputThread.start()
		#wait for a message
		while True:
				data = c.recv(1024)
				if not data:
						break	
				print(emoji.emojize("Peer: " + str(data, 'utf-8')))
		
		
# we make a new thread to allow us to send and receive at the same time
# the target of our message is the socket connection we made
inputThread = threading.Thread(target=sendMsg, args=(sock,))
# this allows us to close the program regardless of any extra threads open
inputThread.daemon = True
inputThread.start()

#wait for a message
while True:
		data = sock.recv(1024)
		if not data:
				break	
		print(emoji.emojize("Peer: " + str(data, 'utf-8')))
