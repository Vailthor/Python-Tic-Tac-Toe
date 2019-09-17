#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

### Protocol Implementation

# This is just about the simplest possible protocol
class Play(LineReceiver):
    board = [["-" for x in range(3)] for y in range(3)]
    def connectionMade(self):
        self.setLineMode()
        if len(self.factory.clients) == 1:
            print("Got second client!")
            self.factory.clients.append(self)
            self.factory.clients[0].sendLine(b"Start")
            self.sendLine(b"Begin")

        elif len(self.factory.clients) == 0 : 
            print("Got first client!")
            self.factory.clients.append(self)
            

    def connectionLost(self, reason):
        print("Lost a client!")
        self.factory.clients.remove(self)
        for i in range (0,3):
              for j in range (0,3):
                self.board[i][j] = "-"
    def lineReceived(self, line):
        if len(self.factory.clients) == 2:
            #is O
            if (self == self.factory.clients[0]):
                self.updateBoard("O", line)
                for c in self.factory.clients:
                    c.sendBoard()
            
                if self.checkWin("O") == "W":
                    self.factory.clients[0].sendLine(b"Win00")
                    self.factory.clients[1].sendLine(b"Lose0")
                elif self.checkWin("X") == "T":
                    self.factory.clients[1].sendLine(b"Tie00")
                    self.factory.clients[0].sendLine(b"Tie00")
                else:    
                    self.factory.clients[0].sendLine(b"Wait0")
                    self.factory.clients[1].sendLine(b"Turn0")
            #is X
            else:
                self.updateBoard("X", line)
                for c in self.factory.clients:
                    c.sendBoard()

                if self.checkWin("X") == "W":
                    self.factory.clients[1].sendLine(b"Win00")
                    self.factory.clients[0].sendLine(b"Lose0")
                elif self.checkWin("X") == "T":
                    self.factory.clients[1].sendLine(b"Tie00")
                    self.factory.clients[0].sendLine(b"Tie00")
                else:
                    self.factory.clients[1].sendLine(b"Wait0")
                    self.factory.clients[0].sendLine(b"Turn0")
                
        else:
            self.sendLine(b"Please wait for other player")

    def updateBoard(self, player, move):
        move = move.decode("ascii")
        move0 = int(float(move[0])) - 1
        move1 = int(float(move[1])) - 1
        self.board[move0][move1] = player

    def sendBoard(self):
        boardString = "Board"
        for i in range (0,3):
              for j in range (0,3):
                boardString += self.board[i][j]
        self.sendLine(boardString.encode("ascii"))

    def checkWin(self, player):
    #still need to figure out ties
        for i in range (0,3):
            for j in range (0,3):
                if self.board[i][j] == player:
                    if j + 1 == 3:
                        return "W"
                else:
                    break
            for j in range (0,3):
                if self.board[j][i] == player:
                    if j + 1 == 3:
                        return "W"
                else:
                    break
            if i == 0:
                if self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player:
                    return "W"
                elif self.board[2][0] == player and self.board[1][1] == player and self.board[0][2] == player:
                    return "W"
        count = 0
        for i in range (0,3):
              for j in range (0,3):
                if self.board[i][j] == "O" or self.board[i][j] == "X":
                    count += 1
        if count == 9:
            return "T"
        return "N"


def main():
    f = Factory()
    f.protocol = Play
    f.clients = []
    reactor.listenTCP(8000, f)
    reactor.run()

if __name__ == '__main__':
    print("Running")
    main()

#Send data from server to echoclient!