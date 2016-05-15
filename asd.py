from Tkinter import *

class myObject():
    #--------------------------------
    def __init__(self,root):
        self.root = root

        #place a Frame on the root:
        self.f = Frame(self.root, bg="yellow", width=600, height=400)
        self.f.pack()

        #place a Canvas on the Frame:
        self.c =Canvas(self.f, bg="cyan",width=100,height=50)
        #NW-vtx of Canvas:
        self.xNW=10
        self.yNW=10
        self.c.place(x=self.xNW,y=self.yNW)

        ##event-generators:
        self.c.bind('<ButtonPress-1', self.startMoveWindow)
        self.c.bind('<B1-Motion', self.MoveWindow)

        self.c2=Canvas(self.f,bg="red",width=100,height=100)
        self.c2.place(x=300,y=200)
        self.c2.lower(self.c)

    #-----------------------------------------------
    def startMoveWindow(self, event):
        ## at start: record current root coordinates
        self.xo, self.yo = event.x_root, event.y_root

    #--------------------------------------
    def MoveWindow(self, event):
        self.root.update_idletasks()

        ## use root coordinates for offset of Widget (canvas) coordinates
        self.xNW += event.x_root - self.xo
        self.yNW+= event.y_root - self.yo
        ## update coordinates
        self.xo, self.yo= event.x_root, event.y_root

        ## Move & redraw Widget (canvas)
        self.c.place_configure(x=self.xNW, y=self.yNW)

#==================================
root=Tk()
x = myObject(root)
root.mainloop()
