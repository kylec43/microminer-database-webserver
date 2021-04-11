from FirebaseController import FirebaseController
import re
import time
import Constants


def runDatabaseManager(parent, connection, client_address):

	success = True
	firebaseController = FirebaseController()

	try:
		buffer_size = 500000
		#Recieve input lines and noise words from client.
		connection.settimeout(10)
		requestType = connection.recv(buffer_size)
		print("Recieved data from client:", client_address)

		connection.sendall(b'received')

		total_time_start = time.time()
		if requestType.decode('utf-8') == Constants.REQUEST_TYPE_UPLOAD:
			
			originalUrlKeywords = connection.recv(buffer_size)
			connection.sendall(b'received')
			kwicUrlKeywords = connection.recv(buffer_size)

			print('made it1')
			#convert data to string!
			originalUrlKeywords = originalUrlKeywords.decode('utf-8')
			kwicUrlKeywords = kwicUrlKeywords.decode('utf-8')

			originalUrlKeywords = formatUpload(originalUrlKeywords)
			kwicUrlKeywords = formatUpload(kwicUrlKeywords)

			firebaseController.upload(originalUrlKeywords, kwicUrlKeywords)
	

			



		total_time_end = time.time()
		total_time = total_time_end - total_time_start
		print('total time', total_time)
		print('---------------------------------------------------')

	except Exception as e:
		success = False
		print("Error has occured:", e)

	finally:
		# Close the client connection after the try or except block
		if success:
			connection.sendall(Constants.SERVER_RESPONSE_SUCCESS.encode('utf-8'))
		else:
			print('failed')
			connection.sendall(Constants.SERVER_RESPONSE_FAILURE.encode('utf-8'))

		connection.close()
		print("Connection has been closed")


def formatUpload(UrlsKeywords):
	formattedUrlsKeywords = []
	UrlsKeywords = UrlsKeywords.split('\n')
	if UrlsKeywords[-1] == '': UrlsKeywords.pop()

	for i in range(len(UrlsKeywords)):
		lis = UrlsKeywords[i].split()
		url = lis[0]
		keywords = " ".join(lis[1:])
		formattedUrlsKeywords.append({Constants.ARG_URL : url, Constants.ARG_KEYWORDS: keywords})
		

	return formattedUrlsKeywords
