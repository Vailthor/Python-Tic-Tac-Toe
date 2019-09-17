#!/usr/bin/env python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from __future__ import print_function

from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver



class EchoClient(LineReceiver):
    end = b"Bye-bye!"
    currentBoard = [["-" for x in range(3)] for y in range(3)]
    #delimter = '\n'

    def displayBoard(self, board):
        print ("   1   2   3")
        count = 1
        for i in range (0,9):
            if i == 3 or i == 6:
                print ("  ---+---+---")
    
            if i % 3 != 0:
                print ("|", end = "")
            else:
                print (count, end = " ")
                count += 1
    
            
    
            if board[i] == '-':
                print ("   ", end = "")
            else:
                print (" " + board[i] + " ", end = "")
            if i == 2 or i == 5 or i == 8:
                print ("")
        print("")
        i = 0;
        for r in range (0,3):
            for c in range (0,3):
                self.currentBoard[r][c] = board[i]
                i += 1

    def checkInput(self, mSend):
        keepGoing = True
        while keepGoing:
            if len(mSend) != 2:
                mSend = input("Please enter a play move e.g.(12 for row 1 column 2): ")
            elif mSend.isdigit():
                move0 = int(float(mSend[0])) - 1
                move1 = int(float(mSend[1])) - 1
                if move0 > 2 or move0 < 0 or move1 > 2 or move1 < 0:
                    mSend = input("Please enter a play move e.g.(12 for row 1 column 2): ")
                elif self.currentBoard[move0][move1] != "-":
                    mSend = input("That spot is full, please choose a diffrent one: ")
                else:
                    keepGoing = False
            else:
                mSend = input("Please enter a play move e.g.(12 for row 1 column 2): ")
                
        return mSend
            
    def connectionMade(self):
        print("Welcome!")
        #play = input("Please enter a play: ")
        #self.sendLine(play.encode('ascii'))
        #self.sendLine(self.end)

    def lineReceived(self, line):
        line = line.decode("ascii")
        if line == self.end:
            self.transport.loseConnection()
        
        mSend = 0
        #line = line[2:]
        #line = line[:-1]
        lineTag = line[:5]
        line = line[5:]
        #print (line)
        #print (lineTag)
        if lineTag == "Start":
            print ("You are 'O'\n")
            self.displayBoard("---------")
            mSend = input("Please play your move e.g.(12 for row 1 column 2): ")
            print("")
            mSend = self.checkInput(mSend)
            self.sendLine(mSend.encode('ascii'))

        if lineTag == "Board":
            self.displayBoard(line)

        elif lineTag == "Begin":
            print ("You are 'X' please wait...\n")
        
        elif lineTag == "Turn0":
            mSend = input("It is your turn, play your move e.g.(12 for row 1 column 2): ")
            print("")
            mSend = self.checkInput(mSend)
            self.sendLine(mSend.encode('ascii'))
    
        elif lineTag == "Wait0":
            print ("Please wait your turn...\n")
      
        elif lineTag == "Win00":
            print ("You Win!\n")
            self.transport.loseConnection()
    
        elif lineTag == "Lose0":
            print ("You Lose!\n")
            self.transport.loseConnection()
    
        elif lineTag == "Tie00":
            print ("Cat's Game!\n")
            self.transport.loseConnection()
  
        elif line == 0:
            self.transport.loseConnection()

        
    




class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def __init__(self):
        self.done = Deferred()


    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)


    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)



def main(reactor):
    factory = EchoClientFactory()
    reactor.connectTCP('localhost', 8000, factory)
    return factory.done



if __name__ == '__main__':
    task.react(main)
