from tkinter import *
import threading
import random
from orthogonalRangeSearch import OrthogonalRangeSearch
from orthogonalRangeSearchAnimate import OrthogonalRangeSearch as OrthogonalRangeSearchAnimate
import threading


from typing import List, Tuple


import sys
sys.setrecursionlimit(1500)

Point = Tuple[int, int]


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
OPTION_FRAME_WIDTH = 170 

class app:

    def __init__(self, root):

     

        self.root = root

        self.winWidth = WINDOW_WIDTH
        self.winHeight = WINDOW_HEIGHT


        self.pointList = set()
        self.targetRange = ()
     
        self.root.title("Convex Hull")
        self.root.geometry(str(self.winWidth) + "x" + str(self.winHeight))

        self.mainFrame = Frame(self.root, borderwidth=1, relief=FLAT, width = self.winWidth, height = self.winHeight)
        self.mainFrame.pack()

        self.canvas = Canvas(self.mainFrame, width= self.winWidth - OPTION_FRAME_WIDTH, height=self.winHeight)
        self.canvas.bind("<Button-1>", lambda event, canvas=self.canvas, pointList=self.pointList: self.onClick(event, canvas, pointList))
        self.canvas.bind("<Button-3>", lambda event, canvas=self.canvas: self.onRightClick(event, canvas) )
        self.canvas.pack(side=LEFT, fill='both') 

        self.optionFrame = Frame(self.mainFrame, borderwidth=1, relief=RAISED, width= OPTION_FRAME_WIDTH, height=self.winHeight)
        self.optionFrame.pack(side=RIGHT,  expand=True, fill='both', anchor=E)

       
        self.animateVar = IntVar(0)

        

        self.startButton = Button(self.optionFrame, width=10, height=1, text="Start", padx=1, pady=1, command=  lambda canvas=self.canvas, pointList=self.pointList, animate=self.animateVar: self.startButtonPressed(canvas, pointList, animate))
        self.startButton.pack(side=TOP,  expand=False, fill="none")

        self.animateCheckbox = Checkbutton(self.optionFrame, text="Animate", variable=self.animateVar)
        self.animateCheckbox.pack(side=TOP)
       
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
        
        pointList.clear()

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
    #
    #   Modifies: None
    # --> Returns: None

    def startButtonPressed(self, canvas, pointList, animateFlag):
        
        print(pointList)
        print(range)


        leftX = min(self.targetRange[0][0],self.targetRange[1][0])
        rightX = max(self.targetRange[0][0],self.targetRange[1][0])
        bottomY = min(self.targetRange[0][1],self.targetRange[1][1])
        topY = max(self.targetRange[0][1],self.targetRange[1][1])        

        newRange = ((leftX, rightX),(bottomY, topY))


        if not animateFlag.get():
            ORS = OrthogonalRangeSearch()
            result = ORS.orthogonalRangeSearch(pointList, newRange)

            for x,y in result:
                canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='red')


        else:

            self.t1 = threading.Thread(target=self.animateORS, args=(pointList, newRange, canvas) )
            self.t1.start()

        
    def animateORS(self, pointList, newRange, canvas):

        ORS = OrthogonalRangeSearchAnimate(canvas)
        result = ORS.orthogonalRangeSearch(pointList, newRange, canvas)

        for x,y in result:
            canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='red')

        

        

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
        
   
   # onRightClick --------------------------------------------------------------------------------------------
    # Called when canvas(self.canvas) is right clicked on, draws the range area if a point was previously selected
    #   Parameters: Canvas (tkinter), range: Tuple[Point]
    #
    #   Modifies: self.targetRange
    # --> Returns: None

    def onRightClick(self, event, canvas):
        # print(event.x)
        x,y = event.x, event.y
        print(range)
        print("x: ", x, " y: ", y)

        if self.targetRange == ():
            canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill='blue', tag="rangePoint")
            self.targetRange = ((x,y), None)
            print(self.targetRange)

        elif self.targetRange[1] == None:
            print("range already created")
            self.targetRange = ((self.targetRange[0][0], self.targetRange[0][1]),(x,y))
            canvas.delete("rangePoint")
            canvas.create_rectangle(self.targetRange[0][0], self.targetRange[0][1], self.targetRange[1][0], self.targetRange[1][1], fill='blue', stipple='gray50', tag="range")
        else:
            canvas.delete("range")
            self.targetRange = ((x,y), None)

     
        
   


    


    
    # addPoint --------------------------------------------------------------------------------------------
    # Adds a point to the list and draws it to the canvas tkinter
    #   Parameters: Point: (x,y), Canvas (tkinter), pointList: List[Point]
    #
    #   Modifies: pointList
    # --> Returns: None

    def addPoint(self, point, canvas, pointList):

        pointList.add((point[0], point[1]))
        
        python_green = "#476042"
        x1, y1 = (point[0] - 2), (point[1] - 2)
        x2, y2 = (point[0] + 2), (point[1] + 2)
        canvas.create_oval(x1, y1, x2, y2, fill=python_green)


        




if __name__ == "__main__":

    root = Tk()
    root.title("Orthogonal Range Search")
    # root.iconbitmap(r'favicon.ico')
    # root.geometry('300x300')
    mainwin = app(root)
    mainloop()
