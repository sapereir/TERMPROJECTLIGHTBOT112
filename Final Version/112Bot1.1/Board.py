# creates a board and tiles that the bot moves on 

from tkinter import *
import math

class Board(object):
    def __init__(self,matrix):
        self.matrix = matrix
        self.OGMatrix = self.matrix
        self.tiles = []
    def createTiles(self,data):
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[0])):
                tileType = self.matrix[row][col]
                self.tiles.append(Tile(row,col,tileType))
    def botLightTile(self,canvas,data,row,col):
        if self.matrix[row][col] == "blue":
            self.matrix[row][col] = "green"
        elif self.matrix[row][col] == "green":
            self.matrix[row][col] = "blue"
    def completedBoard(self,data):
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix)):
                tileType = self.matrix[row][col]
                if tileType == "blue":
                    return False
        return True
    def reset(self,data):
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix)):
                tileType = self.matrix[row][col]
                if tileType == "green":
                    self.matrix[row][col] = "blue"
    def reset2(self,data):
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix)):
                tileType = self.matrix[row][col]
                if tileType == "blue":
                    self.matrix[row][col] = "grey"
    def flip(self,eventX,eventY,data):
        col = (eventX-data.marginX2)//data.cellSize
        row = (eventY-data.marginY2)//data.cellSize
        if 0 <= col <= 7 and 0 <= row <= 7:
            tileType = self.matrix[row][col]
            if tileType == "grey":
                self.matrix[row][col] = "blue"
            elif tileType == "blue":
                self.matrix[row][col] = "grey"

class Tile(object):
    def __init__(self,row,col,tileType):
        self.row = row
        self.col = col
        self.tileType = tileType
    def draw(self,canvas,data):
        if data.innerMode == "playWorlds":
            xCoor = data.marginX + self.col*data.cellSize
            yCoor = data.marginY + self.row*data.cellSize
            width = xCoor + data.cellSize 
            height = yCoor + data.cellSize
        elif data.innerMode == "createWorlds":
            xCoor = data.marginX2 + self.col*data.cellSize
            yCoor = data.marginY2 + self.row*data.cellSize
            width = xCoor + data.cellSize 
            height = yCoor + data.cellSize
        if self.tileType == "grey":
            canvas.create_rectangle(xCoor,yCoor,width,height,fill="seashell3")
        elif self.tileType == "blue":
            canvas.create_rectangle(xCoor,yCoor,width,height,fill="light sky blue") 
        elif self.tileType == "green":
            canvas.create_rectangle(xCoor,yCoor,width,height,fill="green")
    
