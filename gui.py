from tkinter import *
import threading
import random

from typing import List, Tuple

from avl import TreeNode, AVL_Tree

Point = Tuple[int, int]


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
OPTION_FRAME_WIDTH = 170 

class app:

    def __init__(self, root):



     

        self.root = root

        self.winWidth = WINDOW_WIDTH
        self.winHeight = WINDOW_HEIGHT


        self.pointList = []
        
     
        self.root.title("Convex Hull")
        self.root.geometry(str(self.winWidth) + "x" + str(self.winHeight))

        self.mainFrame = Frame(self.root, borderwidth=1, relief=FLAT, width = self.winWidth, height = self.winHeight)
        self.mainFrame.pack()

        self.canvas = Canvas(self.mainFrame, width= self.winWidth - OPTION_FRAME_WIDTH, height=self.winHeight)
        self.canvas.bind("<Button-1>", lambda event, canvas=self.canvas, pointList=self.pointList: self.onClick(event, canvas, pointList))
        self.canvas.pack(side=LEFT, fill='both') 

        self.optionFrame = Frame(self.mainFrame, borderwidth=1, relief=RAISED, width= OPTION_FRAME_WIDTH, height=self.winHeight)
        self.optionFrame.pack(side=RIGHT,  expand=True, fill='both', anchor=E)

       

        

        self.startButton = Button(self.optionFrame, width=10, height=1, text="Start", padx=1, pady=1, command=  self.startButtonPressed)
      




        self.startButton.pack(side=TOP,  expand=False, fill="none")
        
       
        self.generatePointsLabel = Label(self.optionFrame, text="Number of Points:", width=20)
        self.numOfPointsField = Entry(self.optionFrame, width = 10)
        self.generatePointsLabel.pack(side=TOP)
        self.numOfPointsField.pack(side=TOP)

        self.generateButton = Button(self.optionFrame, width=10, height=1, text="Generate", padx=1, pady=1, command=lambda num = self.numOfPointsField, pointList=self.pointList, rangeX=self.winWidth - OPTION_FRAME_WIDTH - 25, rangeY = self.winHeight - 25, canvas=self.canvas: self.generateButtonPressed(num, pointList, rangeX, rangeY, canvas))
        self.generateButton.pack(side=TOP)

        

        



    # generateButtonPressed --------------------------------------------------------------------------------------------
    # Called when the generate Button is pressed, erases pointList and generates a set of random points within range: (rangeX, rangeY)
    #   Parameters: num tkinter.Entry : int, pointList: List[Point], rangeX: int, rangeY: int
    #
    #   Modifies: pointList
    # --> Returns: None
    def generateButtonPressed(self, numEntry, pointList, rangeX, rangeY, canvas):

        num = int(numEntry.get())
        
        del pointList[:]
        for _ in range(num):
            self.addPoint((random.randrange(25, rangeX), random.randrange(25,rangeY)), canvas, pointList)

        print(pointList)
        print("TODO: create stop button functionality")




    # stopButtonPressed --------------------------------------------------------------------------------------------
    # Called when the stop Button is pressed on, stops any current animation
    #   Parameters: None
    #
    #   Modifies: None
    # --> Returns: None
    def stopButtonPressed(self):
        print("TODO: create stop button functionality")


    # startButtonPressed --------------------------------------------------------------------------------------------
    # Called when the start Button is pressed on
    #
    #   Modifies: None
    # --> Returns: None

    def startButtonPressed(self):
        print("Start Button Pressed")
        
        

        

    # onClick --------------------------------------------------------------------------------------------
    # Called when canvas(self.canvas) is left clicked on
    #   Parameters: Event (tkinter), Canvas (tkinter), pointList: List[Point]
    #
    #   Modifies: pointList
    # --> Returns: None

    def onClick(self, event, canvas, pointList):
        # print(event.x)
        x,y = event.x, event.y
        self.addPoint((x,y), canvas, pointList)
        
   


    
    # addPoint --------------------------------------------------------------------------------------------
    # Adds a point to the list and draws it to the canvas tkinter
    #   Parameters: Point: (x,y), Canvas (tkinter), pointList: List[Point]
    #
    #   Modifies: pointList
    # --> Returns: None

    def addPoint(self, point, canvas, pointList):

        pointList.append((point[0], point[1]))
        
        python_green = "#476042"
        x1, y1 = (point[0] - 2), (point[1] - 2)
        x2, y2 = (point[0] + 2), (point[1] + 2)
        canvas.create_oval(x1, y1, x2, y2, fill=python_green)


        




if __name__ == "__main__":

    root = Tk()
    root.title("Convex Hull")
    # root.iconbitmap(r'favicon.ico')
    # root.geometry('300x300')
    mainwin = app(root)
    mainloop()
