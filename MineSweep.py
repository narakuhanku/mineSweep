from tkinter import *
from tkinter import messagebox
import random

class mineGrid(Frame):
    def __init__(self, master, width, height, numBombs):
        Frame.__init__(self,master, bg='black')
        self.width=width
        self.height=height
        self.numBombs=numBombs
        self.surround = ((-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1))
        self.grid()
        self.menu = mineMenu(self,width,height,numBombs)
        self.bombs = numBombs
        self.flags = numBombs
        self.count = 0
        self.win = False
        self.lose = False
        self.flagTrack = Label(self, text=self.flags, height=1, width=2, font = ("Arial",12))
        self.flagTrack.grid(row=height,columnspan=width)
        self.cells = {}
        for i in range(numBombs):
            y = random.randint(0,width-1)
            x = random.randint(0,height-1)
            while (x,y) in self.cells.keys():
                y = random.randint(0,width-1)
                x = random.randint(0,height-1)
            self.cells[(x,y)] = mineCell(self)
            self.cells[(x,y)].setValue(9)
            self.cells[(x,y)].grid(row=x,column=y)

        for row in range(height):
            for column in range(width):
                if (row,column) not in self.cells.keys():
                    self.count = 0
                    for (srow,scol) in self.surround:
                        if (row+srow,column+scol) in self.cells.keys():
                            if self.cells[(row+srow,column+scol)].getValue()==9:
                                self.count = self.count + 1
                    self.cells[(row,column)] = mineCell(self)
                    self.cells[(row,column)].setValue(self.count)
                    self.cells[(row,column)].grid(row=row,column=column)

    def revealOther(self,cell):
        for coords, mine in self.cells.items():
            if mine == cell:
                c = coords
        x = int(float(c[0]))
        y = int(float(c[1]))
        cell.checked = True
        for (bx,by) in self.surround:
            if (x+bx,y+by) in self.cells.keys():
                if self.cells[(x+bx,y+by)].checked  == False:
                    self.cells[(x+bx,y+by)].reveal()

    def winCheck(self):
        doneList = []
        for key in self.cells.keys():
            if self.cells[key].clicked == True and self.cells[key].value != 9:
                doneList.append(self.cells[key])
        if len(doneList) == self.height*self.width-self.numBombs:
            messagebox.showinfo('Minesweep','You\'ve Won!', parent=self)
            self.win = True                                                                            

    def gameLoss(self):
        self.flagTrack['text'] = '0'
        for key in self.cells.keys():
            if self.cells[key].value == 9:
                self.cells[key].flagged = False
                self.cells[key].reveal()
        messagebox.showerror('Minesweep','You\'ve Lost!', parent=self)
        self.lose = True

class mineCell(Label):
    def __init__(self, master):
        Label.__init__(self,master,font=('Verdana',12),width=2,height=1,bg='gray',relief=GROOVE)
        self.value = ''
        self.clicked = False
        self.flagged = False
        self.checked = False
        self.colorMap = ['','maroon','maroon','maroon','maroon','maroon','maroon','maroon','maroon']
        self.bind('<Button-1>',self.leftClick)
        self.bind('<Button-3>',self.rightClick)

    def getValue(self):
        return self.value

    def setValue(self,value):
        self.value = value

    def rightClick(self, event):
        if self.flagged == False and self.clicked == False and self.master.flags > 0 and self.master.win == False:
            self['text'] = 'o'
            self.master.flags = self.master.flags - 1
            self.master.flagTrack['text'] = str(self.master.flags)
            self.flagged = True
        elif self.flagged == True and self.clicked == False and self.master.flags < self.master.bombs and self.master.win == False:
            self['text']=''
            self.master.flags = self.master.flags + 1
            self.master.flagTrack['text'] = str(self.master.flags)
            self.flagged = False 

    def leftClick(self,event):
        if self.clicked == False:
            if 0 < self.value and self.value < 9:
                if self.flagged == False and self.master.lose == False:
                    self['relief'] = SUNKEN
                    self['text'] = str(self.value)
                    self['fg'] = self.colorMap[self.value]
                    self['bg'] = 'DarkGray'
                    self.clicked = True
                    self.master.winCheck()
            elif self.value == 9:
                if self.master.win == False and self.flagged == False:
                    self['text']='o'
                    self['bg']='red'
                    self['relief'] = SUNKEN
                    self.clicked = True
                    self.master.gameLoss()
            elif self.value == 0:
                if self.flagged == False and self.master.lose == False:
                    self['text'] = ''
                    self.master.revealOther(self)
                    self['relief'] = SUNKEN
                    self['bg'] = 'DarkGray'
                    self.clicked = True
                    self.master.winCheck()

    def reveal(self):
        if self.clicked == False:
            if 0 < self.value and self.value < 9:                    
                if self.flagged == False and self.master.lose == False:
                    self['text']=str(self.value)
                    self['fg'] = self.colorMap[self.value]
                    self['relief'] = SUNKEN
                    self['bg'] = 'DarkGray'
                    self.clicked = True
                    self.master.winCheck()
            elif self.value == 9:                      
                if self.flagged == False:
                    self['text']='o'
                    self['bg']='red'
                    self['relief'] = SUNKEN
                    self.clicked = True
            elif self.value == 0:
                if self.flagged == False and self.master.lose == False:
                    self['text'] = ''
                    self.master.revealOther(self)
                    self['relief'] = SUNKEN
                    self['bg'] = 'DarkGray'
                    self.clicked = True
                    self.master.winCheck()

class mineMenu():
    def __init__(self,game,width,height,numBombs):
        self.game=game
        self.width=width
        self.height=height
        self.numBombs=numBombs
        self.fields = 'width', 'height', 'numBombs'
        menubar = Menu(root)
        gameMenu = Menu(menubar, tearoff=0)
        gameMenu.add_command(label="New Game", command=self.newGame)
        gameMenu.add_command(label="Settings", command=self.setUp)
        gameMenu.add_command(label="Exit Game", command=self.exitGame)
        menubar.add_cascade(label="Menu", menu=gameMenu)

        diffMenu = Menu(menubar, tearoff=0)
        diffMenu.add_command(label="Beginner", command=lambda:self.doNumber(9,9,10))#9x9x10
        diffMenu.add_command(label="Intermediate", command=lambda:self.doNumber(16,16,40))#16x16x40
        diffMenu.add_command(label="Advanced", command=lambda:self.doNumber(16,30,99))#16x30x99
        menubar.add_cascade(label="Difficulty", menu=diffMenu)

        root.config(menu=menubar)

    def doNumber(self,a,b,c):
        self.height=a
        self.width=b
        self.numBombs=c
        self.newGame()

    def exitGame(self):
        raise SystemExit
    
    def newGame(self):
        for w in mineGrid.winfo_children(root):
            w.destroy()
        self.game.destroy()
        self.game = mineGrid(root,self.width,self.height,self.numBombs)
    
    def setUp(self):
        self.form = Tk()
        ents = self.createForm(self.form, self.fields)
        self.form.title('Settings')
        b1 = Button(self.form, text='Play!',command=(lambda: self.doFetch(ents)))
        b1.pack(side=BOTTOM, padx=5, pady=5)
    
    def doFetch(self,entries):
        for entry in entries:
            field = entry[0]
            text  = entry[1].get()
            if field == 'width':
                if int(text)<9:
                    self.width=9
                elif int(text)>30:
                    self.width=30
                else:
                    self.width=int(text)
            if field == 'height':
                if int(text)<9:
                    self.height=9
                elif int(text)>24:
                    self.height=24
                else:
                    self.height=int(text)
            if field == 'numBombs':
                if int(text)<10:
                    self.numBombs=10
                elif int(text)>100:
                    self.numBombs=100
                else:
                    self.numBombs=int(text)
        self.form.destroy()
        self.newGame()
    
    def createForm(self,root,fields):
        entries = []
        for field in fields:
            row = Frame(root)
            lab = Label(row, width=10, text=field, anchor='w')
            ent = Entry(row)
            row.pack(side=TOP, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT)
            entries.append((field, ent))
        return entries

if __name__ == '__main__':
    root = Tk()
    root.title('Minesweep')
    game = mineGrid(root,9,9,10)
    game.mainloop()