import socket
import os
import sys

# The maximum header size
MAX_HEADER_SIZE = 10

# The chunk size
SENDCHUCK = 4096

# The receive chunk size
RCVSIZE = 4096

############################################################
# Receives the header size
# @param sock - the socket over which to receive the data
# @return - header size
############################################################
def recvHeader(sock):
	
	# Get the header
	header = recvAll(sock, MAX_HEADER_SIZE)
	
	# Receive The size of the data
	return int(header)

##########################################################
# Receives a command from client to server
# @param sock - the socket
# @return - receive message
##########################################################
def recvMsg(sock):
	#receives size of message
	messageSize = recvHeader(sock)
	
	return recvAll(sock, int(messageSize))

##########################################################
# Receives a file
# @param sock - the socket
# @param targetFileName - the file to which to save the data
# @result - None
##########################################################
def recvFile(sock, targetFileName):

	# Open the target file
	targetFile = open(targetFileName, "w")
	
	# The size of the data from header
	dataSize = recvHeader(sock)
	
	# Keep receiving until all is received
	while dataSize > 0:
		
		# Receive 4096 bytes of data
		data = recvAll(sock, RCVSIZE)
		
		# Save the data
		targetFile.write(data)
		
		# We now have less bytes to receive 
		dataSize -= len(data)
	
	# Close the file
	targetFile.close()
	
#######################################################
# Receives dataSize number of bytes from the socket sock
# @param sock - socket
# @param dataSize - the number of bytes to receive
# @return - the data received
#######################################################
def recvAll(sock, dataSize):

	# The received data
	data = ""
	
	# Keep receiving until all bytes have
	# been received
	while not len(data) == dataSize:

		# Try to get it all...
		tmpBuff = sock.recv(dataSize - len(data))	
		# Was the connection closed
		if tmpBuff:
			# Save the data
			data += tmpBuff
		# Break the loop
		else:	break
	return data

#################################################
# Sends the header contain data size 
# @param sock - the socket to use for sending
# @param dataSize - the dataSize to send
################################################
def sendHeader(sock, dataSize):

	# Convert the integer length into a string
	dataSizeStr = str(dataSize)
	
	# Prepadd the header with 0's
	while len(dataSizeStr) < MAX_HEADER_SIZE:
		dataSizeStr = "0" + dataSizeStr	

	# Send the header
	sendAll(sock, dataSizeStr)	
	
##########################################################
# send a command from client to server
# @param sock - the socket
# @param message - the command send to server
##########################################################
def sendMsg(sock, message):
	#send message header
	sendHeader(sock, len(message))	
	
	# Send the message data
	sendAll(sock, message)

###########################################################
# Sends the file
# @param sock - the socket over which to send the file
# @param fileName - the name of the file to send
###########################################################
def sendFile(sock, fileName):
	
	# Open the file for reading
	sourceFile = open(fileName, "r")
		
	# Get the file size
	fileSizeStr = str(os.stat(fileName).st_size)
	
	# Send the file size (header)
	sendHeader(sock, fileSizeStr)

	# Keep reading the file and sending
	while True:
	
		# Read the chunk from the file
		chunk = sourceFile.read(SENDCHUCK)	

		# I am not at the end of file
		if chunk:
			# Send the data
			sendAll(sock, chunk)

		else:
			break
	
#############################################
# Keeps sending all the data until all the 
# data is received.
# @param sock - the socket over which to send
# @param data - the data to send
#############################################
def sendAll(sock, data):

	data = str(data)
	# How many bytes were already sent
	bytesSentSoFar = 0	

	# Keep sending until all is sent
	while not bytesSentSoFar == len(data):

		# Send it!
		bytesSentSoFar += sock.send(data[bytesSentSoFar:])

