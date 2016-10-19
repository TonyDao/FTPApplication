import socket
import os
import commands
import sys
from header import *

# the command header size
CMD_MESSAGE_SIZE = 5

# the file name size
FILE_MESSAGE_SIZE = 20

# the transer port size
PORT_MESSAGE_SIZE = 10

###############################################
# prepadd the header message with space
# @param cmd - command type
# @param fileName - file name
# @param portNum - ephemeral port number
# @return - prepadd command into 35 bytes
###############################################
def prepadd (cmd, filename, portNum):
	
	while len(cmd) < CMD_MESSAGE_SIZE:
		cmd = " " + str(cmd)
	
	while len(filename) < FILE_MESSAGE_SIZE:
		filename = " " + str(filename)
				
	while len(str(portNum)) < PORT_MESSAGE_SIZE:
		portNum = " " + str(portNum)
		
	request = cmd + filename + portNum
	
	return request

###############################################
# create ephemeral port for data transfer 
# from client to server
# @param sock - the socket
# @param cmd - command type
# @param fileName - fileName
# @result - data connection 
###############################################
def createEphermeral (sock, cmd, fileName):
	# Make an epemeral socket
	dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# bind data sock to 0
	dataSock.bind(('',0))

	# Listen 1 connection
	dataSock.listen(1)

	# Get the port
	dataPortNum = dataSock.getsockname()[1]
	
	# prepadd request message
	requestMsg = prepadd(cmd, fileName, dataPortNum)
		
	# send request message
	sendMsg(sock, requestMsg)
	
	# Wait for the server to connect
	dataConn, addr = dataSock.accept()
	
	return dataConn

# Check the arguments
if len(sys.argv) < 3:
	print "USAGE: " + sys.argv[0] + " <IP> <PORT>"
	exit(1)

# Get the ip address number
ipAddr = sys.argv[1]

# The port number
port = int(sys.argv[2])

# Create a socket
listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
listenSock.connect((ipAddr, port))

while True:
	# initialize client command
	request = ""

	#store client command into array
	request = raw_input("ftp> ").split(' ')
	
	#split request message into cmdType and fileName	
	cmdType = request[0]
	
	if(len(request) > 1):
		fileName = request[1]
	else:
		fileName = ""
			
	#get file from server
	if cmdType == "get":
		#create ephermeral port and send request message
		dataConn = createEphermeral (listenSock, cmdType, fileName)	
	
		# receive respond message from server
		sepondMsg = recvMsg(dataConn)
		
		#receive file
		if sepondMsg == "1":
			#receive file from data connection
			recvFile(dataConn, fileName)
			
			# print filename and size in bytes
			print "File " + fileName + " transfered " + str(os.path.getsize(fileName)) + " bytes"
			
		#file doesn't find in server directory
		else:
			# print file not find
			print "There file " + fileName + " is not exit in server directory."
			
		#close data connection
		dataConn.close()
		
	#send file to server
	elif cmdType == "put":
		#create ephermeral port and send request message
		dataConn = createEphermeral(listenSock, cmdType, fileName)
		
		# find is not exit in current directory
		if not os.path.isfile(fileName):
			# print error
			print("ERROR: The file " + fileName + " is not exit in current directory.")
			
			# send server to not receive file
			sendMsg(dataConn, "0")
			
		# the file exit and send file
		else:
			# send server to receive file
			sendMsg(dataConn, "1")
			
			#send file to server
			sendFile(dataConn, fileName)
			
			# print file and size
			print "File " + fileName + " transfered " + str(os.path.getsize(fileName)) + " bytes"
		
		#close data sock connection
		dataConn.close()					

	#list files on the server
	elif cmdType == "ls":
		#create ephermeral port and send request message
		dataConn = createEphermeral(listenSock, cmdType, fileName)
		
		# receive respond message from server
		sepondMsg = recvMsg(dataConn)
		
		# receive message
		if sepondMsg == "1":
			#receive message from data connection
			data = recvMsg(dataConn)
			print data
		else:
			print "Error: can't receive message from server."
			
		#close data connection
		dataConn.close()
	
	#list files on the client
	elif cmdType == "lls":
		state, result = commands.getstatusoutput('ls -l')
		print result
	
	#disconnects from server and exits
	elif cmdType == "quit":
		# prepadd request message
		requestMsg = prepadd(cmdType, "", "")
			
		# send request message
		sendMsg(listenSock, requestMsg)
		
		# receive respond message from server
		sepondMsg = recvMsg(listenSock)
		
		# close listen connection
		if sepondMsg:
			listenSock.close()
			break;
				
	#command not valid
	else:
		print("Usage:\n\tget <file name>\n\tput <file name>\n\tls\n\tlls\n\tquit")
