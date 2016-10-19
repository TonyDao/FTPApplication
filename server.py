import socket
import sys
import commands
from header import *

###############################################
# forking child server to services client request
# @param listenConn - listen connection
# @return - None
###############################################
def clientServices(listenConn):
	while True:
		# Get the request command from client
		requestMsg = recvMsg(listenConn)	
			
		# split request message
		cmdType = requestMsg[:5].replace(' ', '')
		fileName = requestMsg[5:25].replace(' ', '')
		dataPortNum = requestMsg[25:].replace(' ', '')
		
		# print client request message
		print str(addr[0]) + ":" + str(addr[1]) + " request: " + cmdType + " " + fileName
		
		# client request get
		if cmdType == "get":
			#connect to data sock
			cliDataSock = connClientPort(addr, dataPortNum)
		
			# check file exit and send respond message
			if not os.path.isfile(fileName):
				print("ERROR: The file " + fileName + " is not exit in current directory.")
				
				#send spond message
				sendMsg(cliDataSock, "0")
				
				print "FAILURE"
			
			#find exit and send file
			else:
				#send spond message for client to receive file
				sendMsg(cliDataSock, "1")
			
				# Receive the file
				sendFile(cliDataSock, fileName)
				
				print "SUCCESS"
			
			#close data connection

			cliDataSock.close()
		
		# client request put	
		elif cmdType == "put":	
			#connect to client data connection
			cliDataSock = connClientPort(addr, dataPortNum)
						
			# Receive client message
			message = recvMsg(cliDataSock)
			
			# client send file
			if message == "1":
				#receive file
				recvFile(cliDataSock, fileName)
				print "SUCCESS Transfer file " + fileName + " size " + str(os.path.getsize(fileName))
				
			#client don't send file
			else:
				print "FAILURE."
				
		
		# client request ls
		elif cmdType == "ls":
			#connect to client data connection
			cliDataSock = connClientPort(addr, dataPortNum)
			
			# Receive the file
			sendMsg(cliDataSock, "1")
			
			# result of ls command
			state, result = commands.getstatusoutput("ls -l")
			
			# send message through data sock	
			sendMsg(cliDataSock, result)
			
			print "SUCCESS"
				
		
		# client request quit
		elif cmdType == "quit":
			sendMsg(listenConn, "accept")
			
			listenConn.close()
			print "SUCCESS"
			break
		
		# error request
		else:
			print("FAILURE")

###############################################
# connect to client data port
# @param addr - IP and port address of client
# @param dataPortNum - data port number
# @return - data port
###############################################
def connClientPort (addr, dataPortNum):	
	# Get the client's IP
	cliIP = addr[0]
	
	# Make a socket
	cliDataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			
	# Connect to the client!
	cliDataSock.connect((cliIP, int(dataPortNum)))
		
	#print "Got port: ", dataPortNum
	
	return cliDataSock
	

# Check the arguments
if len(sys.argv) < 2:
	print "USAGE: " + sys.argv[0] + " <PORT>"
	exit(1)

# Get the port number
port = int(sys.argv[1])

# Create a socket
listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
listenSock.bind(('', port))

# Start listening!
listenSock.listen(5) 

# Wait forever to receive connections
while True:

	# Accept the connection from the client
	listenConn, addr = listenSock.accept()
	
	# fork server 
	pid = os.fork()

	# server child service client requests
	if pid == 0:
		clientServices(listenConn)
	
