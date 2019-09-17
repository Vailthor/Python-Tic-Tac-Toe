#!/usr/bin/python

# This is TCPServer.py

from socket import *
import sys

board = [["-" for x in range(3)] for y in range(3)]

def updateTable(player, move):
  board[move[0]][move[1]] = player
def checkWin(player):
  #still need to figure out ties
  for i in range (0,3):
    for j in range (0,3):
      if board[i][j] == player:
        if j + 1 == 3:
          return "W"
    for j in range (0,3):
      if board[j][i] == player:
        if j + 1 == 3:
          return "W"
    if i == 0:
      for j in range (0,3):
        if board[j][j] == player:
          if j + 1 == 3:
            return "W"
  return "C"
  

DEFAULT_VALUE = 6789
MSIZE = 50
serverPort = int(sys.argv[1]) if len(sys.argv) == 2 else DEFAULT_VALUE
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
socketO = 0
addrO = 0
print ('The Server is ready to receive')
try:
   while 1:
      socketX, addrX = serverSocket.accept()
      #socketO, addrO = serverSocket.accept()
      #Once both players have connected begin
      print ("Hello")
      if socketO != 0:
        socketO.send("Start".encode())
        socketX.send("Begin".encode())
        turns = True
        while turns:
          move = None
          move = SocketO.recv(MSIZE).decode()
          updateTable("O", move)
          #send board to players
          boardString = ""
          for i in range (0,3):
            for j in range (0,3):
              boardString += board[i][j]
          socketO.send(boardString.encode())
          socketX.send(boardString.encode())
          state = checkWin("O")
          if state == "W":
            socketO.send("Win")
            socketX.send("Lose")
            for i in range (0,3):
              for j in range (0,3):
                boardString += board[i][j]
            socketO.send(boardString.encode())
            socketX.send(boardString.encode())
            turns = False
          elif state == "T":
            socketO.send("Tie".encode())
            socketX.send("Tie".encode())
            for i in range (0,3):
              for j in range (0,3):
                boardString += board[i][j]
            socketO.send(boardString.encode())
            socketX.send(boardString.encode())
            turns = False
          else:
            socketO.send("Wait")
            socketX.send("Turn")
            move = SocketX.recv(MSIZE).decode()
            updateTable("X", move)
            for i in range (0,3):
              for j in range (0,3):
                boardString += board[i][j]
            socketO.send(boardString.encode())
            socketX.send(boardString.encode())
            state = checkWin("X")
            
            #X Wins
            if state == "W":
              socketO.send("Lose")
              socketX.send("Win")
              for i in range (0,3):
                for j in range (0,3):
                  boardString += board[i][j]
              socketO.send(boardString.encode())
              socketX.send(boardString.encode())
              turns = False
            
            #A Tie
            elif state == "T":
              socketO.send("Tie")
              socketX.send("Tie")
              for i in range (0,3):
                for j in range (0,3):
                  boardString += board[i][j]
              socketO.send(boardString.encode())
              socketX.send(boardString.encode())
              turns = False             
            else:
              socketO.send("Turn".encode())
              socketX.send("Wait".encode())
        socketO.close()
        socketX.close()
      else:
        socketO = socketX
        addrO = addrX
except KeyboardInterrupt:
   print ("\nClosing Server")
   serverSocket.close()

