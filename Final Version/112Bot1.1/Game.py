# this is where everything is run from and controlled

from tkinter import *
from PlayGame import *
from Instructions import *
from SplashScreen import *
from Board import *
from Bot import *
from Commands import * 



"""idea overall was adapted from lightbot itself.
all PICTURES were from previous said in other files sources, but same came from listed below: Laurent Haan; Github,
loading bar: https://answers.unity.com/questions/667862/how-to-call-sprite-at-run-time.html
The different modes and run function came from the 15-112 website
https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Progressbar: alot of the tkinter widgets or features are 
from the library
Other things were cited where they used
"""

####################################
# init
####################################    

def init(data):
    # There is only one init, not one-per-moder
    data.mode = "splashScreen"
    data.innerMode = None
    data.score = 0
    data.level = None   
    data.edit = True
    data.boardLevel1 = [["grey","grey","grey","grey","grey","grey","grey","blue"],
                        ["grey","grey","grey","grey","grey","grey","blue","grey"],
                        ["grey","grey","grey","grey","grey","blue","grey","grey"],
                        ["grey","grey","grey","grey","blue","grey","grey","grey"],
                        ["grey","grey","grey","blue","grey","grey","grey","grey"],
                        ["grey","grey","blue","grey","grey","grey","grey","grey"],
                        ["grey","blue","grey","grey","grey","grey","grey","grey"],
                        ["blue","grey","grey","grey","grey","grey","grey","grey"]]
    data.boardLevel2 = [["blue","grey","grey","grey","grey","grey","grey","blue"],
                        ["grey","grey","grey","grey","grey","grey","grey","grey"],
                        ["grey","grey","grey","grey","grey","grey","grey","grey"],
                        ["grey","grey","grey","grey","grey","grey","grey","grey"],
                        ["grey","grey","grey","grey","grey","grey","grey","grey"],
                        ["grey","grey","grey","grey","grey","grey","grey","grey"],
                        ["grey","grey","grey","grey","grey","grey","grey","grey"],
                        ["blue","grey","grey","grey","grey","grey","grey","blue"]]
    data.boardLevel3 = [["blue","blue","blue","blue","blue","blue","blue","blue"],
                        ["blue","grey","grey","grey","grey","grey","grey","blue"],
                        ["blue","grey","grey","grey","grey","grey","grey","blue"],
                        ["blue","grey","grey","grey","grey","grey","grey","blue"],
                        ["blue","grey","grey","grey","grey","grey","grey","blue"],
                        ["blue","grey","grey","grey","grey","grey","grey","blue"],
                        ["blue","grey","grey","grey","grey","grey","grey","blue"],
                        ["blue","blue","blue","blue","blue","blue","blue","blue"]]
    data.createWorld = [["grey","grey","grey","grey","grey","grey","grey","grey"],
                        ["grey","grey","grey","grey","grey","grey","grey","grey"],
                        ["grey","grey","grey","grey","grey","grey","grey","grey"],
                        ["grey","grey","grey","grey","grey","grey","grey","grey"],
                        ["grey","grey","grey","grey","grey","grey","grey","grey"],
                        ["grey","grey","grey","grey","grey","grey","grey","grey"],
                        ["grey","grey","grey","grey","grey","grey","grey","grey"],
                        ["grey","grey","grey","grey","grey","grey","grey","grey"]]
    data.cellSize = 70
    data.marginX = 250
    data.marginY = 25
    data.marginX2 = 325
    data.marginY2 = 75
    data.main = True
    data.boardOne = Board(data.boardLevel1)
    data.boardTwo = Board(data.boardLevel2)
    data.boardThree = Board(data.boardLevel3)
    data.boardWorld = Board(data.createWorld)
    data.currentBoard = data.boardOne
    data.botOne = Bot(data,0,7,180)
    data.botTwo = Bot(data,0,0,180)
    data.botThree = Bot(data,7,0,0)
    data.botCreate = Bot(data,0,0,180)
    data.functionOne = Functions()
    data.functionTwo = Functions()
    data.functionThree = Functions()
    data.functionCreate = Functions()
    data.running = False
    data.imageBackground = PhotoImage(file="images/background.png")
    data.imageCommands = PhotoImage(file="images/commands.gif")
    data.imageSingleCommands = []
    data.completeBoard = False
    createImageCommands(data)
    data.drawBotOne = True
    data.userInterface = BotDesign()
    data.drawBotUser = False
    data.back = [10,10,50]
    data.effect1 = BotEffect()
    data.effect2 = BotEffect2(3)
    data.effect3 = Loading()
    data.effect4 = BotEffect3()
    data.effect5 = BotEffect4(0)
    data.effect6 = BotEffect5()
    data.loading = False
    data.animating = False
    data.timer = 0
    data.r = 180
    data.radius = 150
    data.exploding = False
    data.rad = 50
    data.won = False
    data.score = 0

def createImageCommands(data):
    possibleCommands = 1
    while possibleCommands <= 5:
        path = "images/command%s.gif" %(possibleCommands)
        image = PhotoImage(file=path)
        data.imageSingleCommands.append(image)
        possibleCommands += 1

####################################
# mode dispatcher
####################################

def mousePressed(event, data):
    if (data.mode == "splashScreen"): splashScreenMousePressed(event, data)
    elif (data.mode == "playGame"):   playGameMousePressed(event, data)
    elif (data.mode == "instructions"):  instructionsMousePressed(event, data)

def keyPressed(event, data):
    if (data.mode == "splashScreen"): splashScreenKeyPressed(event, data)
    elif (data.mode == "playGame"):   playGameKeyPressed(event, data)
    elif (data.mode == "instructions"): instructionsKeyPressed(event, data)

def timerFired(data):
    if (data.mode == "splashScreen"): splashScreenTimerFired(data)
    elif (data.mode == "playGame"):   playGameTimerFired(data)
    elif (data.mode == "instructions"):  instructionsTimerFired(data)

def redrawAll(canvas, data):
    App()
    canvas.create_rectangle(0,0,data.width,data.height,fill="lemon chiffon",width=0)
    if (data.mode == "splashScreen"): splashScreenRedrawAll(canvas, data)
    elif (data.mode == "playGame"):   playGameRedrawAll(canvas, data)
    elif (data.mode == "instructions"):  instructionsRedrawAll(canvas, data)


####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100000 # milliseconds
    data.root = Tk(className="112Bot")
    init(data)
    # create the root and the canvas
    canvas = Canvas(data.root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    data.root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    data.root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    data.root.mainloop()  # blocks until window is closed
    print("bye!")

run(1200, 700)


