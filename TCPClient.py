#!/usr/bin/python

# This is TCPClient.py

from socket import *
import sys

serverName = "127.0.0.1"
DEFAULT_VALUE = 6789
MSIZE = 50
serverPort = int(sys.argv[1]) if len(sys.argv) == 2 else DEFAULT_VALUE
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

def displayBoard(board):
  print ("   1   2   3")
  count = 1
  for i in range (0,9):
    if i == 3 or i == 6:
      print ("---+---+---")
    
    if i % 3 != 0:
      print ("|", end = " ")
    else:
      print (count, end = " ")
      count += 1
    
    if i == 2 or i == 5 or i == 8:
      print ("")
    
    if board[i] == '-':
      print ("   ", end = "")
    else:
      print (" " + board[i] + " ", end = "")
  
keepGoing = True
while keepGoing:
  mRecv = 0
  mSend = 0
  mRecv = clientSocket.recv(MSIZE).decode()
  print (mRecv)

  if mRecv == "Start":
    print ("You are 'O'\n")
    displayBoard("---------")
    mSend = input("Please play your move e.g.(12 for row 1 column 2):")
    mSend = checkInput(mSend)
    clientSocket.send(mSend).encode()
    mRecv = clientSocket.recv(MSIZE).decode()
    displayBoard(mRecv)

  elif mRecv == "Begin":
    print ("You are 'X' please wait...\n")
    mRecv = clientSocket.recv(MSIZE).decode()
    displayBoard(mRecv)
  
  elif mRecv == "Turn":
    mSend = input("It is your turn play your move e.g.(12 for row 1 column 2): \n")
    mSend = checkInput(mSend)
    clientSocket.send(mSend).encode()
    mRecv = clientSocket.recv(MSIZE).decode()
    displayBoard(mRecv)
    
  elif mRecv == "Wait":
    print ("Please wait...\n")
    mRecv = clientSocket.recv(MSIZE).decode()
    displayBoard(mRecv)
      
  elif mRecv == "Win":
    mRecv = clientSocket.recv(MSIZE).decode()
    displayBoard(mRecv)
    print ("You Win!")
    keepGoing = False
    
  elif mRecv == "Lose":
    mRecv = clientSocket.recv(MSIZE).decode()
    displayBoard(mRecv)
    print ("You Lose!")
    keepGoing = False
    
  elif mRecv == "Tie":
    mRecv = clientSocket.recv(MSIZE).decode()
    displayBoard(mRecv)
    print ("Cat's Game!")
    keepGoing = False
  
  elif mRecv == 0:
    keepGoing = False
    

clientSocket.close()


