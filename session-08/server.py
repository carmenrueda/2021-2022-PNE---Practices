import socket #new module--> first import it

# Configure the Server's IP and PORT
PORT = 8000
IP = "localhost"
MAX_OPEN_REQUESTS = 5

# Counting the number of connections
number_con = 0

# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket is a class
#we will always use it like this
try:
    serversocket.bind((IP, PORT)) # IP needs to be an existing ip address in my machine
    # ip address = ipconfig
    # become a server socket
    # MAX_OPEN_REQUESTS connect requests before refusing outside connections
    serversocket.listen(MAX_OPEN_REQUESTS) #up to 5 requests in parallel
    #now im prepare to receive requests form the exterior

    while True:
        # accept connections from outside
        print("Waiting for connections at {}, {} ".format(IP, PORT))
        (clientsocket, address) = serversocket.accept() #address of the client that is talking to me

        # Another connection!e
        number_con += 1 #increasing everytime there is a new connection

        # Print the connection number
        print("CONNECTION: {}. From the IP: {}".format(number_con, address))

        # Read the message from the client, if any
        msg = clientsocket.recv(2048).decode("utf-8")
        print("Message from client: {}".format(msg))

        # Send the messag
        message = "Hello from the teacher's server"
        send_bytes = str.encode(message) #== str((message).encode()
        # We must write bytes, not a string
        clientsocket.send(send_bytes)
        clientsocket.close()

except socket.error:
    print("Problems using port {}. Do you have permission?".format(PORT))

except KeyboardInterrupt:
    print("Server stopped by the user")
    serversocket.close()