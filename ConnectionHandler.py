from Event import Event
import Constants
from time import time
from time import sleep
from threading import Thread
import socket
from runDatabaseManager import runDatabaseManager
import Constants

def ConnectionHandler(parent):

	#Port Number
	PORT_NO = 12001

	#0.0.0.0 will bind to all available IPV4 addresses.
	#This allows client connections from outside the servers's network
	SERVER_IP = '0.0.0.0'
	SERVER_ADDRESS = (SERVER_IP, PORT_NO)

	try:
		# Create a TCP/IP socket
		#AF_INET allows us to communicate to ipv4 client connections
		#SOCK_STREAM specifies using the TCP Protocol.
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("Socket has been created.")


		# Bind the socket to the specified port
		server_socket.bind(SERVER_ADDRESS)
		print("Server Socket is now binded to the specified address:", SERVER_ADDRESS)


		#Listen for incoming connections
		server_socket.listen()
		print("Server is now listening for incoming connections")

	except Exception:
		event = Event(Constants.EVT_CONNECTION_ERROR)
		parent.addEvent(event)
		event = Event(Constants.EVT_PRINT_ERROR, "Failed to bind socket to port")
		parent.addEvent(event)
		server_socket.close()
		return


	threads = []
	server_socket.settimeout(1)
	while True:

		try:
			#wait for and accept incoming client connection
			connection, client_address = server_socket.accept()
			print('accepted connection from:', client_address)

			#starts a new thread
			#_thread.start_new_thread(function, (arguments))
			connection_thread = Thread(target = runDatabaseManager, args = (parent, connection, client_address))
			threads.append(connection_thread)
			connection_thread.start()
		except:

			if not parent.serverIsRunning():
				for thread in threads:
					thread.join()
				break
			else:
				#timeout
				pass

		
	server_socket.close()
	print("Socket closed")

	
