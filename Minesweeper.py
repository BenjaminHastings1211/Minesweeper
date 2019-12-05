from tkinter import *
import math, random, time
InfoH = 50
W, H = 600,600
CPL = 15

COLORS = {'1' : '#2c5e8f',
          '2' : '#008900',
          '3' : '#dc143c',
          '4' : '#193753',
          '5' : '#700a1f',
          '6' : '#1c9183',
          '7' : '#000',
          '8' : '#a2a2a2',
          '*' : '#000'

}
SAND = ['#c2b280','#b5a265','#c8ba8d','#cfc29b']

def cutList(l):
    newL = []
    for item in l:
        if item not in newL:
            newL.append(item)
    return newL

def addListToList(L1,L2):
    for item in L2: L1.append(item)
    return L1

class Tile():
    def __init__(self,board,pos,hasBomb=False):
        self.hasBomb = hasBomb
        self.pos = pos
        self.covered = True
        self.status = {True : random.choice(SAND), False : '#cdcdcd'}
        self.flip = {False : True, True : False}
        self.text = ''
        self.textColor = '#000'

        self.Obj = Frame(board,width=int(W/CPL)-2,height=int(H/CPL)-2,bg=self.status[self.covered])
        self.Obj.grid(row=self.pos[0],column=self.pos[1],padx=1,pady=1)
        self.Obj.pack_propagate(0)

        self.Display = Label(self.Obj,text=self.text,font='Roboto 18 bold',bg=self.Obj['bg'],anchor='center')
        # self.text.grid(sticky="wens")
        if self.covered == False:
            self.Display.pack(fill=Y)

        self.Obj.bind('<1>',self._handleClick)

    def _handleClick(self,event):
        self.covered = False
        if self.text == '':
            tileController.openArea(self)

class TileController():
    def __init__(self,percentBombs):
        self.tiles = []
        self.percentBombs = percentBombs
        self.totalBombs = 0
        self.unsearched = 0
        self.gameOver = False
        self.neightbourFormat = [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]

        self.board = Frame(root,width=W,height=H,bg='#000')
        self.board.grid(rowspan=CPL,columnspan=CPL,sticky='s')
        self.board.pack_propagate(0)



    def populate(self):
        bombs = [True if random.random() < self.percentBombs else False for i in range(CPL**2)]
        self.totalBombs = len([tile for tile in bombs if tile == True])
        total.config(text='Bombs: %s'%self.totalBombs)
        for y in range(CPL):
            row = []
            for x in range(CPL):
                row.append(Tile(self.board,[x,y],bombs[y*CPL+x]))
            self.tiles.append(row)

        for column in self.tiles:
            for tile in column:
                n = self.findNeighborBombs(tile)
                ln = len(n)
                if ln == 1 and type(n) == str: tile.text = n
                elif ln != 0:
                    tile.text = ln
                    tile.textColor = COLORS[str(ln)]

    def findNeighborBombs(self,tile):
        neighbors = []
        if tile.hasBomb == True:
            return '*'
        else:
            for check in self.neightbourFormat:
                row = tile.pos[0]+check[0]
                column = tile.pos[1]+check[1]
                if (row >= 0 and column >= 0) and (row <= CPL-1 and column <= CPL-1):
                    if self.tiles[column][row].hasBomb == True:
                        neighbors.append(self.tiles[column][row])

        return neighbors

    def update(self):
        totalCovered = 0;
        for column in self.tiles:
            for tile in column:
                if tile.covered == False:
                    if tile.text == '*':
                        self.gameOver = True
                    tile.Obj.config(bg=tile.status[tile.covered])
                    tile.Display.config(fg=tile.textColor,text=tile.text,bg=tile.Obj['bg'])
                    tile.Display.pack()
                else:
                    totalCovered += 1

        unsearched.config(text='Unsearched Tiles: %s'%totalCovered)
        self.unsearched = totalCovered



    def openArea(self,tile):
        # print('a')
        neighbors = [tile]
        new = None
        for i in range(10):
            new = []
            for tile in neighbors:
                new = addListToList(new,self.findNeighborEmpty(tile))
            neighbors = cutList(new)

        last = []
        for tile in neighbors:
            last = addListToList(last,self.allNeighbors(tile))

        neighbors = cutList(addListToList(neighbors,last))
        for tile in neighbors:
            tile.covered = False

    def findNeighborEmpty(self,tile):
        neighbors = []
        for check in self.neightbourFormat:
            row = tile.pos[0]+check[0]
            column = tile.pos[1]+check[1]
            if (row >= 0 and column >= 0) and (row <= CPL-1 and column <= CPL-1):
                if self.tiles[column][row].text == '':
                    neighbors.append(self.tiles[column][row])
        return neighbors

    def allNeighbors(self,tile):
        neighbors = []
        for check in self.neightbourFormat:
            row = tile.pos[0]+check[0]
            column = tile.pos[1]+check[1]
            if (row >= 0 and column >= 0) and (row <= CPL-1 and column <= CPL-1):
                neighbors.append(self.tiles[column][row])
        print(len(neighbors))
        return neighbors

root = Tk()
root.title('Minesweeper')
root.resizable(0,0)
root.wm_attributes('-topmost',1)
root.geometry('%sx%s'%(W,H+InfoH))

Info = Frame(width=W,height=InfoH,bg='#fff')
Info.grid(rowspan=CPL,columnspan=1,sticky='n')
Info.pack_propagate(0)
total = Label(Info,text='',font='Roboto 18 bold',bg=Info['bg'])
total.pack(side=LEFT,padx=25)
unsearched = Label(Info,text='',font='Roboto 18 bold',bg=Info['bg'])
unsearched.pack(side=RIGHT,padx=25)



tileController = TileController(0.15)
tileController.populate()



while 1:
    if tileController.totalBombs == tileController.unsearched and tileController.gameOver == False:
        print('you win')
    elif tileController.gameOver == True:
        print('Game Over')
    tileController.update()
    root.update()
    root.update_idletasks()
    time.sleep(0.001)
