# contains sprites for classes and for controlling bot

from tkinter import *
from Commands import * 
from time import sleep
from Board import *
import math
import random

"""Recursion with largerStack from 15112 Website"""

def callWithLargeStack(f,*args):
    import sys
    import threading
    threading.stack_size(2**27)  # 64MB stack
    sys.setrecursionlimit(2**27) # will hit 64MB stack limit first
    # need new thread to get the redefined stack size
    def wrappedFn(resultWrapper): resultWrapper[0] = f(*args)
    resultWrapper = [None]
    #thread = threading.Thread(target=f, args=args)
    thread = threading.Thread(target=wrappedFn, args=[resultWrapper])
    thread.start()
    thread.join()
    return resultWrapper[0]

"""Adapted sprites from https://stackoverflow.com/questions/16579674/using-spritesheets-in-tkinter"""

class Bot(object):
    def __init__(self,data,row,col,angle):
        self.row = row
        self.col = col
        self.xCoor = data.marginX + self.col*data.cellSize + data.cellSize//2
        self.yCoor = data.marginY + self.row*data.cellSize +  data.cellSize//2
        self.angle = angle
        self.OGangle = angle
        self.speed = 10
        self.originalPos = [self.row,self.col] 
        self.spritesheet = PhotoImage(file="images/bot.gif") 
        self.numSprites = 4 
        self.lastImage = None
        self.images = [self.subimage(32*i, 0, 32*(i+1), 48) 
            for i in range(self.numSprites)]
        self.updateImageAngle(angle)
    def subimage(self, l, t, r, b):
        dst = PhotoImage()
        dst.tk.call(dst, 'copy', self.spritesheet, '-from', l, t, r, b, '-to', 0, 0)
        return dst
    def updateimage(self,sprite,canvas,data,deltaX=0,deltaY=0):
        if data.innerMode == "createWorlds":
            self.xCoor = data.marginX2 + self.col*data.cellSize + data.cellSize//2
            self.yCoor = data.marginY2 + self.row*data.cellSize +  data.cellSize//2
        data.running = False
        canvas.delete(self.lastImage)
        if not(deltaX == 0 and deltaY == 0):
            if deltaX < 0:
                self.xCoor -= self.speed
                if data.innerMode == "playWorlds" or "createWorlds":                                                  
                    self.lastImage = canvas.create_image(self.xCoor - self.speed,self.yCoor, 
                    image=self.images[sprite])
                deltaX += self.speed
            elif deltaX > 0:
                self.xCoor += self.speed
                if data.innerMode == "playWorlds" or "createWorlds":  
                    self.lastImage = canvas.create_image(self.xCoor,self.yCoor, 
                    image=self.images[sprite])
                deltaX -= self.speed
            elif deltaY < 0:
                self.yCoor -= self.speed
                if data.innerMode == "playWorlds" or "createWorlds": 
                    self.lastImage = canvas.create_image(self.xCoor,self.yCoor, 
                    image=self.images[sprite])
                deltaY += self.speed
            elif deltaY > 0:
                self.yCoor += self.speed
                if data.innerMode == "playWorlds" or "createWorlds":  
                    self.lastImage = canvas.create_image(self.xCoor,self.yCoor, 
                    image=self.images[sprite])
                deltaY -= self.speed
        else:
            if data.innerMode == "playWorlds" or "createWorlds":  
                self.lastImage = canvas.create_image(self.xCoor, self.yCoor, 
                image=self.images[sprite])
        if data.innerMode == "playWorlds" or "createWorlds":                             
            canvas.after(150, self.updateimage, (sprite+1) % self.numSprites,canvas,data,
                deltaX, deltaY)
    def updateImageAngle(self,angle):
        if angle == 0 or angle == 360:
            rowSprite = 3
        elif angle == 90:
            rowSprite = 2
        elif angle == 180:
            rowSprite = 0
        elif angle == 270:
            rowSprite = 1
        self.images = [self.subimage(32*i, 0 + 48*rowSprite, 32*(i+1), 48*rowSprite + 48) 
            for i in range(self.numSprites)]
    def followMain(self,canvas,data,main,procedure):
        for command in range(len(main)):
            if main[command] == "P1":
                self.followP1(canvas,data,procedure)
            elif main[command] == "Foward":
                if self.angle == 0 or self.angle == 360:
                    if 0 <= self.row - 1 <= 7:
                        self.row -= 1
                        self.updateimage(0,canvas,data,0,-70)
                    else:
                        self.reset(data)
                        break
                elif self.angle == 90:
                    if 0 <= self.col + 1 <= 7:
                        self.col += 1
                        self.updateimage(0,canvas,data,70,0)
                    else:   
                        self.reset(data)
                        break
                elif self.angle == 180:
                    if 0 <= self.row + 1 <= 7:
                        self.row += 1
                        self.updateimage(0,canvas,data,0,70)
                    else:
                        self.reset(data)
                        break
                elif self.angle == 270:
                    if 0 <= self.col - 1 <= 7:
                        self.col -= 1
                        self.updateimage(0,canvas,data,-70,0)
                    else:
                        self.reset(data)
                        break
            elif main[command] == "RotateC":
                self.angle = (self.angle + 90)%360
                self.updateImageAngle(self.angle)
                # self.updateimage(0,canvas,data,0,0)
                # sleep(0.5)
            elif main[command] == "RotateCC":
                self.angle = (self.angle - 90)%360
                self.updateImageAngle(self.angle)
                # self.updateimage(0,canvas,data,0,0)
                # sleep(0.5)
            elif main[command] == "Light":
                # data.timerDelay = 100
                data.currentBoard.botLightTile(canvas,data,self.row,self.col)
            if data.currentBoard.completedBoard(data):
                data.won = True
                # canvas.create_text(data.width//2,data.height//2,
                #     text="You Won /n (Click any Key to continue)",fill="orange red",font="Bold 35")
    def followP1(self,canvas,data,procedure):
        numCommands = len(procedure)
        command = 0
        depth = 0
        while command < numCommands:
            if procedure[command] == "P1":
                command = -1
                depth += 1
                if depth >= 15:
                    canvas.create_text(data.width//2,data.height//2,text="Bad Solution",font="Bold 50")
                    break
            elif procedure[command] == "Foward":
                if self.angle == 0 or self.angle == 360:
                    if 0 <= self.row - 1 <= 7:
                        self.row -= 1
                        canvas.after(20,self.updateimage,0,canvas,data,0,-70)
                    else:
                        self.reset(data)
                        break
                elif self.angle == 90:
                    if 0 <= self.col + 1 <= 7:
                        self.col += 1
                        canvas.after(20,self.updateimage,0,canvas,data,70,0)
                    else:
                        self.reset(data)
                        break
                elif self.angle == 180:
                    if 0 <= self.row + 1 <= 7:
                        self.row += 1
                        canvas.after(20,self.updateimage,0,canvas,data,0,70)
                    else:
                        self.reset(data)
                        break
                elif self.angle == 270:
                    if 0 <= self.col - 1 <= 7:
                        self.col -= 1
                        canvas.after(20,self.updateimage,0,canvas,data,-70,0)
                    else:
                        self.reset(data)
                        break
            elif procedure[command] == "RotateC":
                self.angle = (self.angle + 90)%360
                self.updateImageAngle(self.angle)
                canvas.after(20,self.updateimage,0,canvas,data,0,0)
            elif procedure[command] == "RotateCC":
                self.angle = (self.angle - 90)%360
                self.updateImageAngle(self.angle)
                canvas.after(20,self.updateimage,0,canvas,data,0,0)
            elif procedure[command] == "Light":
                # data.timerDelay = 100
                data.currentBoard.botLightTile(canvas,data,self.row,self.col)
            if data.currentBoard.completedBoard(data):
                data.won = True
                # canvas.create_text(data.width//2,data.height//2,
                #     text="You Won /n (Click any Key to continue)",fill="orange red",font="Bold 35")
            command += 1
    def reset(self,data):
        self.row = self.originalPos[0]
        self.col = self.originalPos[1]
        if data.innerMode == "createWorlds":
            self.xCoor = data.marginX2 + self.col*data.cellSize + data.cellSize//2
            self.yCoor = data.marginY2 + self.row*data.cellSize +  data.cellSize//2
        else:
            self.xCoor = data.marginX + self.col*data.cellSize + data.cellSize//2
            self.yCoor = data.marginY + self.row*data.cellSize +  data.cellSize//2
            self.angle = self.OGangle
            self.updateImageAngle(self.angle)
    def move(self):
        self.updateImageAngle(self.angle)
        if self.angle == 0 or self.angle == 360:
            if 0 <= self.row - 1 <= 7:
                    self.row -= 1
        elif self.angle == 90:
            if 0 <= self.col + 1 <= 7:
                    self.col += 1
        elif self.angle == 180:
            if 0 <= self.row + 1 <= 7:
                self.row += 1
        elif self.angle == 270:
            if 0 <= self.col - 1 <= 7:
                self.col -= 1
    def rotate(self):   
        self.angle = (self.angle + 90)%360
        self.updateImageAngle(self.angle)

class BotDesign(object):
    def __init__(self):
        self.spritesheet = PhotoImage(file="images/bot.gif") 
        self.numSprites = 4 
        self.lastImage = None
        self.j = 48
        self.speed = -5
        self.images = [self.subimage(32*i, self.j, 32*(i+1), self.j + 48) 
            for i in range(self.numSprites)]
    def subimage(self, l, t, r, b):
        dst = PhotoImage()
        dst.tk.call(dst, 'copy', self.spritesheet, '-from', l, t, r, b, '-to', 0, 0)
        return dst
    def updateimage(self,sprite,canvas,data,x, y):
        data.drawBotUser = False
        canvas.delete(self.lastImage)
        if x - 16 < 0:
            self.j = 96
            self.speed = 5
            self.images = [self.subimage(32*i, self.j, 32*(i+1), self.j + 48) 
                for i in range(self.numSprites)]
        elif x + 16 > data.width:
            self.j = 48
            self.speed = -5
            self.images = [self.subimage(32*i, self.j, 32*(i+1), self.j + 48) 
                for i in range(self.numSprites)]
        if data.innerMode == None and data.mode == "playGame":            
            self.lastImage = canvas.create_image(x, y, image=self.images[sprite])
        x += self.speed
        if data.innerMode == None and data.mode == "playGame":
            canvas.after(100, self.updateimage, (sprite+1) % self.numSprites, canvas,data,x, y)

class BotEffect(object):
    def __init__(self):
        self.spritesheet = PhotoImage(file="images/light.png")
        self.numSprites = 8
        self.lastImg = None
        self.images = [self.subimage(128*i, 0, 128*(i+1), 512) for i in range(self.numSprites)]
    def subimage(self, l, t, r, b):
        dst = PhotoImage()
        dst.tk.call(dst, 'copy', self.spritesheet, '-from', l, t, r, b, '-to', 0, 0)
        return dst
    def updateimage(self,sprite, canvas,data,x, y):
        canvas.delete(self.lastImg)
        if data.mode == "splashScreen":
            self.lastImg = canvas.create_image(x, y, image=self.images[sprite])
        if data.mode == "splashScreen": 
            canvas.after(50, self.updateimage, (sprite+1) % self.numSprites,canvas,data, x, y)

class BotEffect2(object):
    def __init__(self,row):
        self.row = row
        self.spritesheet = PhotoImage(file="images/bot2.png")
        self.numSprites = 8
        self.lastImg = None
        self.images = [self.subimage(80*i, self.row*100, 80*(i+1), self.row*100 + 100) 
            for i in range(self.numSprites)]
    def subimage(self, l, t, r, b):
        dst = PhotoImage()
        dst.tk.call(dst, 'copy', self.spritesheet, '-from', l, t, r, b, '-to', 0, 0)
        return dst
    def updateimage(self,sprite, canvas,data,x, y):
        canvas.delete(self.lastImg)
        if data.mode == "splashScreen":
            self.lastImg = canvas.create_image(x, y, image=self.images[sprite])
        if data.mode == "splashScreen": 
            canvas.after(100, self.updateimage, (sprite+1) % self.numSprites,canvas,data, x, y)

class BotEffect3(object):
    def __init__(self):
        self.spritesheet = PhotoImage(file="images/light.png")
        self.numSprites = 8
        self.lastImg = None
        self.images = [self.subimage(128*i, 0, 128*(i+1), 512) for i in range(self.numSprites)]
    def subimage(self, l, t, r, b):
        dst = PhotoImage()
        dst.tk.call(dst, 'copy', self.spritesheet, '-from', l, t, r, b, '-to', 0, 0)
        return dst
    def updateimage(self,sprite, canvas,data,x, y):
        canvas.delete(self.lastImg)
        if data.innerMode == None and data.mode == "playGame":
            self.lastImg = canvas.create_image(x, y, image=self.images[sprite])
        if data.innerMode == None and data.mode == "playGame":
            canvas.after(50, self.updateimage, (sprite+1) % self.numSprites,canvas,data, x, y)

class BotEffect4(object):
    def __init__(self,row):
        self.row = row
        self.spritesheet = PhotoImage(file="images/bot2.png")
        self.numSprites = 8
        self.lastImg = None
        self.images = [self.subimage(80*i, self.row*100, 80*(i+1), self.row*100 + 100) 
            for i in range(self.numSprites)]
    def subimage(self, l, t, r, b):
        dst = PhotoImage()
        dst.tk.call(dst, 'copy', self.spritesheet, '-from', l, t, r, b, '-to', 0, 0)
        return dst
    def updateimage(self,sprite, canvas,data,x, y):
        canvas.delete(self.lastImg)
        if x <= data.width*5//6:
            if data.innerMode == None and data.mode == "playGame":
                self.lastImg = canvas.create_image(x, y, image=self.images[sprite])
            if data.innerMode == None and data.mode == "playGame":
                canvas.after(100, self.updateimage, (sprite+1) % self.numSprites,canvas,data, (x+15)%data.width, y)
        else:
            data.exploding = True
            data.effect6.updateimage(0,canvas,data,0,x,y)

class BotEffect5(object):
    def __init__(self):
        self.spritesheet = PhotoImage(file="images/exp.png")
        self.numSprites = 4
        self.lastImage = None
        self.image1 = [self.subimage(128*i, 0, 128*(i+1), 128) for i in range(self.numSprites)]
        self.image2 = [self.subimage(128*i, 128, 128*(i+1), 256) for i in range(self.numSprites)]
        self.image3 = [self.subimage(128*i, 256, 128*(i+1), 384) for i in range(self.numSprites)]
        self.image4 = [self.subimage(128*i, 384, 128*(i+1), 512) for i in range(self.numSprites)] 
        self.images = (self.image1 + self.image2 + self.image3 + self.image4)
    def subimage(self, l, t, r, b):
        dst = PhotoImage()
        dst.tk.call(dst, 'copy', self.spritesheet, '-from', l, t, r, b, '-to', 0, 0)
        return dst
    def updateimage(self,sprite, canvas,data,count,x, y):
        canvas.delete(self.lastImage)
        count += 100
        if count >= 1600:
            i = random.randrange(data.width//2,data.width*5//6)
            j = random.randrange(94,606)
            data.effect5.updateimage(0,canvas,data,i,j)
            data.exploding = False
        if data.innerMode == None and data.mode == "playGame" and data.exploding:
            self.lastImage = canvas.create_image(x, y, image=self.images[sprite])
        if data.innerMode == None and data.mode == "playGame" and data.exploding:
            canvas.after(75, self.updateimage, (sprite+1) % self.numSprites**2,canvas,data,count, x, y)

class Loading(object): 
    def __init__(self):
        self.spritesheet = PhotoImage(file="images/progress.png")
        self.numSprites = 11
        self.lastImg = None
        self.images = [self.subimage(0, 40*i, 400, 40*(i+1)) for i in range(self.numSprites)]
    def subimage(self, l, t, r, b):
        dst = PhotoImage()
        dst.tk.call(dst, 'copy', self.spritesheet, '-from', l, t, r, b, '-to', 0, 0)
        return dst
    def updateimage(self,sprite, canvas,data,x, y):
        canvas.delete(self.lastImg)
        if data.mode == "playGame"and data.innerMode == None and data.timer < 1100:
            self.lastImg = canvas.create_image(x, y, image=self.images[sprite])
        if data.mode == "playGame" and data.innerMode == None and data.timer < 1100: 
            canvas.after(100, self.updateimage, (sprite+1) % self.numSprites,canvas,data, x, y)
            data.timer += 100
            if data.timer >= 1100:
                if data.select == "playWorlds":
                    canvas.create_text(data.width//2,data.marginY*3,text="Ready?...Click Anywhere to Continue",
                        font="Bold 18")
                    data.innerMode = "playWorlds"
                else:
                    data.innerMode = "createWorlds"
                    canvas.create_text(data.width//2,data.marginY*3,text="Ready?...Click Anywhere to Continue",
                        font="Bold 18")

