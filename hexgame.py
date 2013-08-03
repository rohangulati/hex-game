from __future__ import print_function
from Tkinter import *
import array
from sys import stdout
from collections import namedtuple
from math import *

# Introduction to the game-------------------------------------------------------------------------------------------------------------
"""This is a two player Hex Game. In this game the player has to build a bridge from his side to his other side of
the hex paralellogram, players take turn alternatively,the one who builds first wins.A player can place his stone at

any empty place.As soon as an unbroken chain of stones connects two opposite sides of the board, the game ends
declaring the winner of the game. This game was invented by Piet Hein. It is a win or lose game proved by

John Nash an independent inventor of this game.
"""

#Some Implementation and Algorithm Details----------------------------------------------------------------------------------------------
"""The game is implemented as Union Find and Union Join Algorithm.

1. Intitally every node is the parent of itself.
2. A Cmponent will have one parent . Priority of deciding the parent is done by following steps:

a. If the node at top or bottom layer of the board is not available as a parent , choose any parent that is available.
b. But if the node at top or bottom layer is available choose it , if more than one of them are available choose any.

3. In case when greater than equal to one parent is available from top layer and simultaneously from bottom layer,
bridge is formed and game is over.

"""




GRID_SIZE = 7
IMG_SIZE = 35
XPAD = 40
YPAD = 40
WIN_HEIGHT = 2 * YPAD + GRID_SIZE * IMG_SIZE + 100
WIN_WIDTH = 2 * XPAD + (3 * GRID_SIZE - 1) * IMG_SIZE

# Data Structure
data = namedtuple('data', 'i j')

# Game Variables
dx = [0, 1, 0, -1, -1, 1]
dy = [-1, -1, 1, 1, 0, 0]


class playInfo():

    def __init__(self):
        self.board = [[-1 for x in xrange(GRID_SIZE + 5)] for x in \
                                                        xrange(GRID_SIZE + 5)]
        self.Par = [[data(0, 0) for x in xrange(GRID_SIZE + 5)] \
                                                for x in xrange(GRID_SIZE + 5)]
        self.initParent()
        self.mode = 0

    def initParent(self):
        for row in xrange(GRID_SIZE + 1):
            for col in xrange(GRID_SIZE + 1):
                self.Par[row + 1][col + 1] = data(row + 1, col + 1)

    def givePar(self, par):
        if self.Par[par.i][par.j].i == par.i and \
                                            self.Par[par.i][par.j].j == par.j:
            return self.Par[par.i][par.j]
        par = self.givePar(self.Par[par.i][par.j])
        return par	

    def isConnect(self, sameNode, r, c):
        flup, fllr = False, False
        for same in sameNode:
            root = self.givePar(same)
            if((root.i == 1 and self.mode == 0) or (root.j == 1 and self.mode == 1)):
                flup = True
            if((root.i == GRID_SIZE and self.mode == 0) or (root.j==GRID_SIZE and self.mode == 1)):
                fllr = True
        if(flup and fllr ):
            return True
        if((flup and (r==GRID_SIZE or c==GRID_SIZE) ) or (fllr and (r==1 or c==1) )):
            return True
        return False

    def getNeighbour(self, sameNode):
        for same in sameNode:
            keep = self.givePar(same)
            if((self.mode == 0 and (keep.i == 1 or keep.i == GRID_SIZE)) or
                            (self.mode == 1 and (keep.j == 1 or keep.j == GRID_SIZE))):
                return same
        return data(-1, -1)

    def inRange(self, r, c):
        if r<1 or r>GRID_SIZE or c<1 or c>GRID_SIZE:
            return False
        return True

    def findSame(self, r, c):
        sameNode = []
        for k in xrange(6):
            if not self.inRange(r + dy[k], c + dx[k]) :
                continue;
            if self.board[r + dy[k]][c + dx[k]] == self.mode:
                sameNode.append(data(r + dy[k], c + dx[k]))
        return sameNode

    def isWinning(self, r, c):
        sameNode = self.findSame(r, c)
        if len(sameNode) == 0:
            return False
        if self.isConnect(sameNode,r,c):
            return True
        friend = self.getNeighbour(sameNode)
        print(friend.i,end='\n')
        if friend.i == -1:
            self.Par[r][c] = self.givePar(sameNode[0])
            for same in sameNode[1:]:
                tmp = self.givePar(same)
                if self.Par[r][c] != tmp:
                    self.Par[tmp.i][tmp.j] = data(r, c)
        else:
            self.Par[r][c] = self.givePar(friend)
            for same in sameNode:
                if same == friend:
                    continue
                tmp = self.givePar(same)
                if self.Par[r][c] != tmp:
                    self.Par[tmp.i][tmp.j] = data(r, c)
        return False

    def printBoard(self):
        n = GRID_SIZE
        i,j = 0,0
        print ("Current Board Display: ",end="\n")
        for i in range(1,n+1):
            for k in range(1,i):
                stdout.write(" ")
                for j in range(1,n+1):
                    print(self.board[i][j],end=" ")
                stdout.write("\n")


class gameGrid():
    def __init__(self, frame):
        self.frame = frame
        self.white = PhotoImage(file="./media/white35.gif")
        self.red = PhotoImage(file="./media/red35.gif")
        self.blue = PhotoImage(file="./media/blue35.gif")
        self.drawGrid()
        self.playInfo = playInfo()

    def drawGrid(self):
        for yi in range(0, GRID_SIZE):
            xi = XPAD + yi * IMG_SIZE
            for i in range(0, GRID_SIZE):
                l = Label(self.frame, image=self.white)
                l.pack()
                l.image = self.white
                l.place(anchor=NW, x=xi, y=YPAD + yi * IMG_SIZE)
                l.bind('<Button-1>', lambda e: self.on_click(e))
                xi += 2 * IMG_SIZE

    def getCoordinates(self, widget):
        row = (widget.winfo_y() - YPAD) / IMG_SIZE
        col = (widget.winfo_x() - XPAD - row * IMG_SIZE) / (2 * IMG_SIZE)
        return row + 1, col + 1

    def toggleColor(self, widget):
        if self.playInfo.mode == 1:
            widget.config(image=self.red)
            widget.image = self.red
        else:
            widget.config(image=self.blue)
            widget.image = self.blue

    def display_winner(self, winner):
        winner_window = Tk()
        winner_window.wm_title("Winner")
        frame = Frame(winner_window, width=40, height=40)
        frame.pack()
        label = Label(frame,text = "Winner is Player : " + winner )
        label.pack()
        label.place(anchor=nW, x = 20, y = 20)

    def on_click(self, event):
        if event.widget.image != self.white:
            return
        self.toggleColor(event.widget)
        a, b = self.getCoordinates(event.widget)
        self.playInfo.board[a][b] = self.playInfo.mode
        #self.playInfo.printBoard()
        if self.playInfo.isWinning(a, b):
            winner = ""
            if self.playInfo.mode == 0:
                winner = " 1 ( Blue ) "
            else:
                winner += " 2 ( Blue ) "
            self.display_winner(winner)
            exit()
        self.playInfo.mode = (self.playInfo.mode + 1) % 2

class gameWindow:
    def __init__(self, window):
        self.frame = Frame(window, width=WIN_WIDTH, height=WIN_HEIGHT)
        self.frame.pack()
        self.gameGrid = gameGrid(self.frame)


def main():
    window = Tk()
    window.wm_title("Hex Game")
    gameWindow(window)
    window.mainloop()


main()

