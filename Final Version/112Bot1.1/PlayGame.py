# this is where all the features of the game are controlled

from tkinter import *
from Board import *
from Bot import *
from Commands import * 
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import messagebox
import string
import os
import random

def playGameMousePressed(event, data):
    if data.mode == "playGame" and data.innerMode == None:
        if data.back[0] < event.x < data.back[0] + data.back[2]*2 and \
            data.back[1] < event.y < data.back[1] + data.back[2]:
            data.mode = "splashScreen"
            data.timer = 0
            data.innerMode = None
            data.loading = False
        elif data.width//3 - data.radius < event.x < data.width//3 + data.radius and \
            data.height//2 - data.radius < event.y < data.height//2 + data.radius:
            answer = simpledialog.askinteger("Input", "What level do you want to Play?",parent=data.root, 
                minvalue=1, maxvalue=3)
            """http://interactivepython.org/runestone/static/thinkcspy/GUIandEventDrivenProgramming/02_standard_dialog_boxes.html"""
            if answer is not None:
                data.level = answer
                if data.level == 1:
                    data.edit = True
                    data.currentBoard = data.boardOne
                elif data.level == 2:
                    data.edit = True
                    data.currentBoard = data.boardTwo
                elif data.level == 3:
                    data.edit = True
                    data.currentBoard = data.boardThree
                data.loading = True
                data.select = "playWorlds"
        elif data.width//1.5 - data.radius < event.x < data.width//1.5 + data.radius and \
            data.height//2 - data.radius < event.y < data.height//2 + data.radius:
                data.loading = True
                data.select = "createWorlds" 

    if (data.innerMode == "playWorlds"): playWorldsMousePressed(event, data)
    elif (data.innerMode == "createWorlds"): createWorldsMousePressed(event, data)

def playGameKeyPressed(event, data):
    if (data.innerMode == "playWorlds"): playWorldsKeyPressed(event, data)
    elif (data.innerMode == "createWorlds"): createWorldsKeyPressed(event, data)

def playGameTimerFired(data):
    if (data.innerMode == "playWorlds"): playWorldsTimerFired(data)
    elif (data.innerMode == "createWorlds"): createWorldsTimerFired(data)

def playGameRedrawAll(canvas, data): # 10,10,110,60
    if data.innerMode == None and data.mode == "playGame":
        canvas.create_rectangle(0,0,data.width,data.height,fill="slateGray3")
        canvas.create_rectangle(data.back[0],data.back[1],data.back[0] + data.back[2]*2,
            data.back[1] + data.back[2],fill="lime green")
        canvas.create_text(data.back[0] + data.back[2],data.back[0] + data.back[2]//2, 
            text="Back", fill="white", font=12)
        canvas.create_rectangle(data.width//3 - data.radius,data.height//2 - data.radius, 
            data.width//3 + data.radius,data.height//2 + data.radius, fill="sky blue")
        canvas.create_text(data.width//3,data.height*2//5,text="Play",fill="Black",font="Bold 40")
        canvas.create_text(data.width//3,data.height*2.75//5,text="(Play Pre-Made Levels" + "\n" 
            "of Increasing Difficulty)",fill="Black",font="Bold 22")
        canvas.create_rectangle(data.width//1.5 - data.radius,data.height//2 - data.radius, 
            data.width//1.5 + data.radius,data.height//2 + data.radius, fill="sky blue")
        canvas.create_text(data.width//1.5,data.height*2//5,text="Create",fill="Black",font="Bold 40")
        canvas.create_text(data.width//1.5,data.height*2.75//5,text="(Make a Level" + "\n" 
            "your Own Way)",fill="Black",font="Bold 22")
        data.drawBotUser = True
        data.effect4.updateimage(0,canvas,data,data.width//1.55,data.height//3.7)
        # if data.drawBotUser:
        #     data.drawBotUser = False
        #     data.userInterface.updateimage(0,canvas,data,data.width - 5, data.height - data.marginY)
        if data.loading:
            data.effect3.updateimage(0,canvas,data,data.width//2,data.marginY*4)
        data.effect4.updateimage(0,canvas,data,data.width*5//6,data.height//2)
        x = random.randrange(data.width//2,data.width*5//6)
        y = random.randrange(94,606)
        if not data.exploding:
            data.effect5.updateimage(0,canvas,data,x,y)
    if (data.innerMode == "playWorlds"): playWorldsRedrawAll(canvas,data)
    elif (data.innerMode == "createWorlds"): createWorldsRedrawAll(canvas,data)

################################################################################################
def playWorldsMousePressed(event, data):
    if data.mode == "playGame" and data.innerMode == "playWorlds":
        if data.back[0] < event.x < data.back[0] + data.back[2]*2 and \
            data.back[1] < event.y < data.back[1] + data.back[2]:
            data.mode = "playGame"
            data.innerMode = None
            data.loading = False
            data.select = None
            data.timer = 0
            data.botOne.reset(data)
            data.boardOne.reset(data)
            data.botTwo.reset(data)
            data.boardTwo.reset(data)
            data.botThree.reset(data)
            data.boardThree.reset(data)
            if data.won == True:
                data.score = len(data.functionOne.procedure1)*32
                answer = simpledialog.askstring("Input", "What is your name?",parent=data.root)
                if answer is not None:
                    print("Your first name is ", answer)
                else:
                    print("You don't have a first name?")
                path1=os.getcwd()+"\\score.txt"
                content = readFile(path1)
                result1 = decode2(content)
                score = str(data.score)
                result1.append((answer,score))
                newContent = encode2(result1)
                writeFile(path1,newContent)
                data.won = False
        elif data.level == 1:
            data.edit = True
            data.timerDelay = 100
            if data.edit:
                data.functionOne.typeFunction(event,data)
            if data.width//10 - data.rad*2 < event.x < data.width//10 + data.rad*2 and \
                data.height//4 - data.rad//1.5 < event.y < data.height//4 + data.rad//1.5:
                data.running = True
                data.edit = False
            elif data.width//10 - data.rad*2 < event.x < data.width//10 + data.rad*2 and \
                data.height//2 - data.rad//1.5 < event.y < data.height//2 + data.rad//1.5:
                data.running = False
                data.botOne.reset(data)
                data.edit = True
                data.boardOne.reset(data)
            elif data.width//10 - data.rad*2 < event.x <  data.width//10 + data.rad*2 and \
                data.height//1.30 - data.rad//1.5 < event.y < data.height//1.30 + data.rad//1.5:
                board = [["grey","grey","grey","grey","grey","grey","grey","blue"],
                        ["grey","grey","grey","grey","grey","grey","blue","grey"],
                        ["grey","grey","grey","grey","grey","grey","grey","grey"],
                        ["grey","grey","grey","grey","grey","grey","grey","grey"],
                        ["grey","grey","grey","grey","grey","grey","grey","grey"],
                        ["grey","grey","grey","grey","grey","grey","grey","grey"],
                        ["grey","grey","grey","grey","grey","grey","grey","grey"],
                        ["grey","grey","grey","grey","grey","grey","grey","grey"]]
                try:
                    ans = backTrack(board,[],data.botOne.angle,[data.botOne.row,data.botOne.col])
                    messagebox.showinfo("Hint", "%s" %str(ans))
                except:
                    print("No Solutions")
        elif data.level == 2:
            data.edit = True
            if data.edit:
                data.functionTwo.typeFunction(event,data)
            if data.width//10 - data.rad*2 < event.x < data.width//10 + data.rad*2 and \
                data.height//4 - data.rad//1.5 < event.y < data.height//4 + data.rad//1.5:
                data.running = True
                data.edit = False
            elif data.width//10 - data.rad*2 < event.x < data.width//10 + data.rad*2 and \
                data.height//2 - data.rad//1.5 < event.y < data.height//2 + data.rad//1.5:
                data.running = False
                data.botTwo.reset(data)
                data.edit = True
                data.boardTwo.reset(data)
        elif data.level == 3:
            data.edit = True
            if data.edit:
                data.functionThree.typeFunction(event,data)
            if data.width//10 - data.rad*2 < event.x < data.width//10 + data.rad*2 and \
                data.height//4 - data.rad//1.5 < event.y < data.height//4 + data.rad//1.5:
                data.running = True
                data.edit = False
            elif data.width//10 - data.rad*2 < event.x < data.width//10 + data.rad*2 and \
                data.height//2 - data.rad//1.5 < event.y < data.height//2 + data.rad//1.5:
                data.running = False
                data.botThree.reset(data)
                data.edit = True
                data.boardThree.reset(data)
        elif data.level == "createWorlds":
            data.currentBoard = data.boardWorld
            if data.edit:
                data.functionCreate.typeFunction(event,data)
            if data.width//10 - data.rad*2 < event.x < data.width//10 + data.rad*2 and \
                data.height//4 - data.rad//1.5 < event.y < data.height//4 + data.rad//1.5:
                data.running = True
                data.edit = False
            elif data.width//10 - data.rad*2 < event.x < data.width//10 + data.rad*2 and \
                data.height//2 - data.rad//1.5 < event.y < data.height//2 + data.rad//1.5:
                data.running = False
                data.botCreate.reset(data)
                data.edit = True
                data.boardWorld.reset(data)
    pass

def playWorldsKeyPressed(event, data):
    if data.edit:
        if data.level == 1:
            data.functionOne.saveCommand(event,data)
        elif data.level == 2:
            data.functionTwo.saveCommand(event,data)
        elif data.level == 3:
            data.functionThree.saveCommand(event,data)
        elif data.level == "createWorlds":
            data.functionCreate.saveCommand(event,data)
    
def playWorldsTimerFired(data):
    pass

def playWorldsRedrawAll(canvas,data):
    if data.innerMode == "playWorlds":
        canvas.create_rectangle(data.width//10 - data.rad*2, data.height//4 - data.rad//1.5,
            data.width//10 + data.rad*2,data.height//4 + data.rad//1.5,fill="light blue")
        canvas.create_rectangle(data.width//10 - data.rad*2, data.height//2 - data.rad//1.5,
            data.width//10 + data.rad*2,data.height//2 + data.rad//1.5,fill="red")
        canvas.create_rectangle(data.width//10 - data.rad*2, data.height//1.30 - data.rad//1.5,
            data.width//10 + data.rad*2,data.height//1.30 + data.rad//1.5,fill="Orange")   
        canvas.create_text(data.width//10,data.height//4,text="Run",font="Bold 25",fill="Black")
        canvas.create_text(data.width//10,data.height//2,text="Stop",font="Bold 25",fill="white")
        canvas.create_text(data.width//10,data.height//1.30,text="Help",font="Bold 25",fill="Black")
        canvas.create_rectangle(data.back[0],data.back[1],data.back[0] + data.back[2]*2,
            data.back[1] + data.back[2],fill="lime green")
        canvas.create_text(data.back[0] + data.back[2],data.back[0] + data.back[2]//2, 
            text="Back", fill="white", font=12)
        if data.level == 1:
            data.boardOne.createTiles(data)
            for tile in data.boardOne.tiles:
                tile.draw(canvas,data)
            data.functionOne.draw(canvas,data)
            if data.running:
                data.botOne.followMain(canvas,data,data.functionOne.main,data.functionOne.procedure1)
            data.botOne.updateimage(0,canvas,data)
        elif data.level == 2:
            data.boardTwo.createTiles(data)
            for tile in data.boardTwo.tiles:
                tile.draw(canvas,data)
            data.functionTwo.draw(canvas,data)
            if data.running:
                data.botTwo.followMain(canvas,data,data.functionTwo.main,data.functionTwo.procedure1)
            data.botTwo.updateimage(0,canvas,data)
        elif data.level == 3:
            data.boardThree.createTiles(data)
            for tile in data.boardThree.tiles:
                tile.draw(canvas,data)
            data.functionThree.draw(canvas,data)
            if data.running:
                data.botThree.followMain(canvas,data,data.functionThree.main,data.functionThree.procedure1)
            data.botThree.updateimage(0,canvas,data)
        elif data.level == "createWorlds":
            data.boardWorld.createTiles(data)
            for tile in data.boardWorld.tiles:
                tile.draw(canvas,data)
            data.functionCreate.draw(canvas,data)
            if data.running:
                data.botCreate.followMain(canvas,data,data.functionCreate.main,data.functionCreate.procedure1)
            data.botCreate.updateimage(0,canvas,data)
        if data.won:
            canvas.create_text(data.width//2,data.height//2,
                text="You Won (Click Back)",fill="red",font="Bold 35")
            
def encode2(content):
    print(content)
    result = ""
    for tup in content:
        result += tup[0]
        result += " "
        result += tup[1]
        result += "\n"
    return result

def decode2(content):   
    result = []
    for line in content.splitlines():
        row = []
        for word in line.split(" "):
            row.append(word)
        myTuple = tuple(row)
        result.append(myTuple)
    return result

def backTrack(board,ans,angle,botPos):
    possibleMoves = ["Light","Foward","Rotate"]
    if isCompleteBoard(board):
        return ans
    else:
        for move in possibleMoves:
            if move == "Foward":
                if angle == 0 or angle == 360:
                    botPos[0] -= 1
                    ans.append(move)
                elif angle == 90:
                    botPos[1] += 1
                    ans.append(move)
                elif angle == 180:
                    botPos[0] += 1
                    ans.append(move)
                elif angle == 270:
                    botPos[1] -= 1
                    ans.append(move)
            elif move == "Rotate":
                angle = (angle + 90)%360
                ans.append(move)
            elif move == "Light":
                row,col = botPos[0],botPos[1]
                if board[row][col] == "blue":
                    board[row][col] = "green"
                    ans.append(move)
                    continue
                elif board[row][col] == "grey":
                     board[row][col] = "red"
                     ans.append(move)
        if isLegalMove(board,):
            tmpSolution = backTrack(board,ans,angle,botPos)
            if tmpSolution != None:
                return tmpSolution
            lastMove = ans.pop()
            if lastMove == "Light":
                board[row][col] = "grey"
            if lastMove == "Foward":
                if angle == 0 or angle == 360:
                    botPos[0] += 1   
                elif angle == 90:
                    botPos[1] -= 1
                elif angle == 180:
                    botPos[0] -= 1
                elif angle == 270:
                    botPos[1] += 1
    return None

def isLegalMove(botPos):
    row,col = botPos[0],botPos[1]
    if row == -1 or row == 8 or col == -1 or col == 8:
        return False
    else:
        return True
    
def isCompleteBoard(board):
    for rows in range(len(board)):
        for cols in range(len(board[0])):
            if board[rows][cols] == "blue":
                return False
    return True

#############################################################################

def createWorldsMousePressed(event, data):
    data.boardWorld.flip(event.x,event.y,data)
    if data.back[0] < event.x < data.back[0] + data.back[2]*2 and \
            data.back[1] < event.y < data.back[1] + data.back[2]:
            data.mode = "playGame"
            data.innerMode = None
            data.loading = False
            data.select = None
            data.boardWorld.reset2(data)
            data.timer = 0
    # reset
    elif (data.width*1//8 - data.radius*3//4 < event.x < data.width*1//8 + data.radius*3//4) and \
        (data.height*3//6 - data.radius//3 < event.y < data.height*3//6 + data.radius//3):
        data.boardWorld.reset2(data)
        data.botCreate.reset(data)
    # play
    elif (data.width*7//8 - data.radius*3//4) < event.x < (data.width*7//8 + data.radius*3//4) and \
        (data.height*2//6 - data.radius//3) < event.y < (data.height*2//6 + data.radius//3):
        data.botCreate.xCoor = data.marginX + data.botCreate.col*data.cellSize + data.cellSize//2
        data.botCreate.yCoor = data.marginY + data.botCreate.row*data.cellSize + data.cellSize//2
        data.innerMode = "playWorlds"
        data.mode = "playGame"
        data.level = "createWorlds"
        data.botCreate.originalPos[0],data.botCreate.originalPos[1] = data.botCreate.row, data.botCreate.col
        data.botCreate.OGangle = data.botCreate.angle
    # save
    elif (data.width*7//8 - data.radius*3//4) < event.x < (data.width*7//8 + data.radius*3//4) and \
        (data.height*3//6 - data.radius//3) < event.y < (data.height*3//6 + data.radius//3):
        matrix = data.boardWorld.matrix
        my_filetypes = [('text files', '.txt')]
        path = filedialog.asksaveasfilename(parent=data.root,initialdir=os.getcwd()+"/boards",
        title="Please name the file your saving:",filetypes=my_filetypes)
        path += ".txt"
        botPos = [0,0,"N"]
        botPos[0] = data.botCreate.row
        botPos[1] = data.botCreate.col
        angle = data.botCreate.angle
        if angle == 0 or angle == 360:
            direction = "N"
        elif angle == 90:
            direction = "E"
        elif angle == 180:
            direction = "S"
        elif angle == 270:
            direction = "W"
        botPos[2] = direction
        encoded = encode(matrix,botPos)
        writeFile(path,encoded)
    # open
    elif (data.width*7//8 - data.radius*3//4) < event.x < (data.width*7//8 + data.radius*3//4) and \
        (data.height*4//6 - data.radius//3) < event.y < (data.height*4//6 + data.radius//3):
        my_filetypes = [('text files', '.txt')]
        path = filedialog.askopenfilename(parent=data.root,initialdir=os.getcwd()+"/boards",
        title="Please select a file:",filetypes=my_filetypes)
        content = readFile(path)
        decoded = decode(content)
        matrix,botPos = decoded
        if botPos[2] == "N":
            angle = 0
        elif botPos[2] == "E":
            angle = 90
        elif botPos[2] == "S":
            angle = 180
        elif botPos[2] == "W":
            angle = 270
        data.botCreate.row, data.botCreate.col,data.botCreate.angle = botPos[0],botPos[1],angle
        data.botCreate.originalPos[0],data.botCreate.originalPos[1] = botPos[0],botPos[1]
        data.botCreate.OGangle = angle
        data.botCreate.updateImageAngle(angle)
        data.boardWorld.matrix = matrix

def encode(content,botPos):
    result = ""
    for rows in range(len(content)): # fix
        if rows != 0:
            result += "\n"
        for cols in range(len(content)):
            if content[rows][cols] == "grey":
                result += "g"
            elif content[rows][cols] == "blue":
                result += "b"
    row,col,direction = botPos[0],botPos[1],botPos[2]
    botString = str(row) +  str(col) + direction
    result = result + "\n" + botString
    return result   

def decode(content):   
    matrix = [["color"]*8 for row in range(8)]
    i = 0
    for line in content.splitlines():
        if len(line) == 3:
            botPos = [0,0,0]
            row,col,direction = line[0],line[1],line[2]
            botPos[0],botPos[1],botPos[2] = int(row),int(col),direction
        j = 0
        for c in line:
            if c == "g":
                matrix[i][j] = "grey"
                j += 1
            elif c == "b":
                matrix[i][j] = "blue"
                j += 1
        i += 1
    return matrix,botPos    
        
"""from 15112 notes on String-week"""

def readFile(path):
    print(path)
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    print(path)
    with open(path, "wt") as f:
        f.write(contents)
    
def createWorldsKeyPressed(event, data):
    if event.keysym == "Up":
        data.botCreate.move()
    elif event.char == "r":
        data.botCreate.rotate()

def createWorldsTimerFired(data):
    pass

def createWorldsRedrawAll(canvas,data):
    if data.innerMode == "createWorlds":
        canvas.create_rectangle(data.back[0],data.back[1],data.back[0] + data.back[2]*2,
            data.back[1] + data.back[2],fill="lime green")
        canvas.create_text(data.back[0] + data.back[2],data.back[0] + data.back[2]//2, 
            text="Back", fill="white", font=12)
        canvas.create_rectangle(data.width*1//8 - data.radius*3//4,data.height*3//6 - data.radius//3,
            data.width*1//8 + data.radius*3//4,data.height*3//6 + data.radius//3,fill="green2")
        canvas.create_text(data.width*1//8,data.height*3//6,text="Reset", fill="Black", font="Bold 22")
        canvas.create_rectangle(data.width*7//8 - data.radius*3//4,data.height*2//6 - data.radius//3,
            data.width*7//8 + data.radius*3//4,data.height*2//6 + data.radius//3,fill="yellow2")
        canvas.create_text(data.width*7//8,data.height*2//6,text="Play", fill="Black", font="Bold 22")
        canvas.create_rectangle(data.width*7//8 - data.radius*3//4,data.height*3//6 - data.radius//3,
            data.width*7//8 + data.radius*3//4,data.height*3//6 + data.radius//3,fill="orange2")
        canvas.create_text(data.width*7//8,data.height*3//6,text="Save", fill="Black", font="Bold 22")
        canvas.create_rectangle(data.width*7//8 - data.radius*3//4,data.height*4//6 - data.radius//3,
            data.width*7//8 + data.radius*3//4,data.height*4//6 + data.radius//3,fill="red2")
        canvas.create_text(data.width*7//8,data.height*4//6,text="Open", fill="Black", font="Bold 22")
        data.boardWorld.createTiles(data)
        for tile in data.boardWorld.tiles:
            tile.draw(canvas,data)
        data.botCreate.updateimage(0,canvas,data)
