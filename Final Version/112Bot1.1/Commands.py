# stores the commands the bot will use later

from tkinter import *
import math

class Functions(object):
    def __init__(self):
        self.main = []
        self.mainNum = []
        self.procedure1 = []
        self.procedure1Num = []
        self.centersMain = []
        self.centersP1 = []
        self.lenMain = [(0,0),(0,0)]
        self.lenP1 = [(0,0),(0,0)]
    def saveCommand(self,event,data):
        if data.main:
            if len(self.main) < 16:
                if event.char == '1':
                    self.main.append("Foward")
                    self.mainNum.append(1)
                elif event.char == '2':
                    self.main.append("Light")
                    self.mainNum.append(2)
                elif event.char == '3':
                    self.main.append("RotateCC")
                    self.mainNum.append(3)
                elif event.char == '4':
                    self.main.append("RotateC")
                    self.mainNum.append(4)
                elif event.char == '5':
                    self.main.append("P1")
                    self.mainNum.append(5)
            if event.keysym == "BackSpace":
                if len(self.main) != 0:
                    self.main.pop()
                    self.mainNum.pop() 
        else:
            if len(self.procedure1) < 16:
                if event.char == '1':
                    self.procedure1.append("Foward")
                    self.procedure1Num.append(1)
                elif event.char == '2':
                    self.procedure1.append("Light")
                    self.procedure1Num.append(2)
                elif event.char == '3':
                    self.procedure1.append("RotateCC")
                    self.procedure1Num.append(3)
                elif event.char == '4':
                    self.procedure1.append("RotateC")
                    self.procedure1Num.append(4)
                elif event.char == '5':
                    self.procedure1.append("P1")
                    self.procedure1Num.append(5)
            if event.keysym == "BackSpace":
                if len(self.procedure1) != 0:
                    self.procedure1.pop()
                    self.procedure1Num.pop() 
    def draw(self,canvas,data): 
        canvas.create_image(data.width//2.25,data.height - data.marginY*2.25,image=data.imageCommands)
        self.drawMainGrid(canvas,data)
        self.drawP1Grid(canvas,data)
    def drawMainGrid(self,canvas,data):
        numCols,numRows = 4,4
        marginX, marginY = data.width - 320, 60
        canvas.create_text(marginX + 28,marginY - 16,text="Main",fill="Green", font="Helvetica 20 bold")
        cellSize = 65
        for row in range(numCols):
            for col in range(numRows):
                startX = marginX + col*cellSize
                endX =  cellSize*col + cellSize + marginX
                startY = marginY + row*cellSize
                endY =  cellSize*row + cellSize + marginY
                self.lenMain[0] = (marginX, cellSize*numCols + cellSize + marginX)
                self.lenMain[1] = (marginY, cellSize*numRows + cellSize + marginY)
                if data.main:
                    canvas.create_rectangle(startX,startY,endX,endY, fill="khaki1",width=2)
                    self.centersMain.append((startX + cellSize//2,startY + cellSize//2))
                else:
                    canvas.create_rectangle(startX,startY,endX,endY, fill="white",width=2)
        counter = 0
        for commands in self.mainNum:
            currentCD = data.imageSingleCommands[commands - 1]
            centerX,centerY = self.centersMain[counter]
            canvas.create_image(centerX,centerY,image=currentCD)
            counter += 1
    def drawP1Grid(self,canvas,data):
        numCols,numRows = 4,4
        marginX, marginY = data.width - 320, 375
        cellSize = 65
        canvas.create_text(marginX + 77,marginY - 16,text="Procedure 1",fill="Green", font="Helvetica 20 bold")
        for row in range(numCols):
            for col in range(numRows):
                startX = marginX + col*cellSize
                endX =  cellSize*col + cellSize + marginX
                startY = marginY + row*cellSize
                endY =  cellSize*row + cellSize + marginY
                self.lenP1[0] = (marginX, cellSize*numCols + cellSize + marginX)
                self.lenP1[1] = (marginY, cellSize*numRows + cellSize + marginY)
                if not data.main:
                    canvas.create_rectangle(startX,startY,endX,endY, fill="khaki1",width=2)
                    self.centersP1.append((startX + cellSize//2,startY + cellSize//2))
                else:
                    canvas.create_rectangle(startX,startY,endX,endY, fill="white",width=2)  
        counter = 0
        for commands in self.procedure1Num:
            currentCD = data.imageSingleCommands[commands - 1]
            centerX,centerY = self.centersP1[counter]
            canvas.create_image(centerX,centerY,image=currentCD)
            counter += 1   
    def typeFunction(self,event,data):
        if (self.lenMain[0][0] < event.x < self.lenMain[0][1]) and\
                (self.lenMain[1][0] < event.y < self.lenMain[1][1]):
            data.main = True
        elif (self.lenP1[0][0] < event.x < self.lenP1[0][1]) and\
            (self.lenP1[1][0] < event.y < self.lenP1[1][1]):
            data.main = False