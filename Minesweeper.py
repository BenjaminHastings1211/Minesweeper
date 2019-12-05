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
        self.flagged = False
        self.status = {True : random.choice(SAND), False : '#cdcdcd'}
        self.flip = {False : True, True : False}
        self.text = ''
        self.textColor = '#000'

        self.Obj = Frame(board,width=int(W/CPL)-2,height=int(H/CPL)-2,bg=self.status[self.covered])
        self.Obj.grid(row=self.pos[0],column=self.pos[1],padx=1,pady=1)
        self.Obj.pack_propagate(0)

        self.Display = Label(
            self.Obj,
            width=self.Obj['width'],
            height=self.Obj['height'],
            text=self.text,
            font='Roboto %i bold'%(eval(tileController.textSize.replace('x',str(CPL)))),
            bg=self.Obj['bg'],
            anchor='center'
        )
        if self.covered == False:
            self.Display.pack(fill=BOTH)

        self.Obj.bind('<1>',self._handleClick)

    def _handleClick(self,event):
        self.covered = False
        if self.text == '':
            tileController.openArea(self)

    def reset(self):
        self.text = ''
        self.textColor = '#000'
        self.covered = True
        self.status[True] = random.choice(SAND)

class TileController():
    def __init__(self,percentBombs):
        self.tiles = []
        self.percentBombs = percentBombs
        self.totalBombs = 0
        self.unsearched = 0
        self.gameOver = False
        self.neightbourFormat = [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]
        self.textSize = '-2.8*x + 70'

        self.board = Frame(root,width=W,height=H,bg='#000')
        self.board.grid(rowspan=CPL,columnspan=CPL,sticky='s')
        self.board.pack_propagate(0)

        root.bind('n',self._handleNew)

    def _handleNew(self,event):
        self.gameOver = False
        self.populate(False)


    def populate(self,inital=True):
        bombs = [True if random.random() < self.percentBombs else False for i in range(CPL**2)]
        self.totalBombs = bombs.count(True)
        total.config(text='Bombs: %s'%self.totalBombs)
        if inital == True:
            for y in range(CPL):
                row = []
                for x in range(CPL):
                    row.append(Tile(self.board,[x,y],bombs[y*CPL+x]))
                self.tiles.append(row)

        else:
            for y, column in enumerate(self.tiles):
                for x, tile in enumerate(column):
                    tile.hasBomb = bombs[y*CPL+x]
                    tile.reset()

        for column in self.tiles:
            for tile in column:
                n = [t for t in self.allNeighbors(tile) if t.hasBomb == True]
                ln = len(n)
                if tile.hasBomb == True:
                    tile.text = '*'
                elif ln != 0:
                    tile.text = ln
                    tile.textColor = COLORS[str(ln)]

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
                    tile.Display.pack_forget()
                    tile.Obj.config(bg=tile.status[tile.covered])
                    totalCovered += 1

        unsearched.config(text='Unsearched Tiles: %s'%totalCovered)
        self.unsearched = totalCovered


    def openArea(self,tile):
        neighbors = [tile]
        new = None
        for i in range(10):
            new = []
            for tile in neighbors:
                new = addListToList(new,[t for t in self.allNeighbors(tile) if t.text == ''])
            neighbors = cutList(new)

        last = []
        for tile in neighbors:
            last = addListToList(last,self.allNeighbors(tile))

        neighbors = cutList(addListToList(neighbors,last))
        for tile in neighbors:
            tile.covered = False


    def allNeighbors(self,tile):
        neighbors = []
        for check in self.neightbourFormat:
            row = tile.pos[0]+check[0]
            column = tile.pos[1]+check[1]
            if (row >= 0 and column >= 0) and (row <= CPL-1 and column <= CPL-1):
                neighbors.append(self.tiles[column][row])
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



tileController = TileController(0.1)
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
