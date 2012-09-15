#! /usr/bin/python
#moo.py

import sys, SocketServer, socket, random, threading

#Server class
class MyUDPHandler(SocketServer.BaseRequestHandler):
	def handle(self):
                guess = self.request[0].strip().split(':')[1]
                socket = self.request[1]
                socket.sendto(guess_response(guess),self.client_address)
              
#Deal with input arguments
if len(sys.argv) != 4:
        sys.exit('Error: 4 arguments are required')
	
secret = sys.argv[1]
my_port = int(sys.argv[2])
opp_port = int(sys.argv[3])
game_over = False

def guess_msg(guess):
        return 'GUESS:'+ str(guess)

def guess_response(guess):
        if guess == secret:
                global game_over
                game_over = True
                return 'WIN'
        else:
                bulls = cows = 0
                for i in range(4):
                        if guess[i] == secret[i]:
                                bulls += 1
                        elif guess[i] in secret:
                                cows += 1
                return str(bulls) + 'B' + str(cows) + 'C'

#Set up server
server = SocketServer.UDPServer(("localhost",my_port), MyUDPHandler)

#Set up client
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(3)

data = 1234

#client-server turn-based loop
while not game_over:
        client.sendto(guess_msg(data) + "\n", ("localhost", opp_port))
        received = ''
        try:
                received = client.recv(1024)
                print received
        except socket.timeout:
                pass
        if received != 'WIN':
                server.handle_request()
        else:
                game_over = True
        data += 1
