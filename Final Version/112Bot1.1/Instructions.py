# Instructions are stored here as well as the leaderboard features

from tkinter import *
from tkinter import font
from tkinter import ttk
import string

def instructionsMousePressed(event, data):
    if data.back[0] < event.x < data.back[0] + data.back[2]*2 and \
        data.back[1] < event.y < data.back[1] + data.back[2]:
        data.mode = "splashScreen"
        data.innerMode = None

def instructionsKeyPressed(event, data):
    pass

def instructionsTimerFired(data):
    pass

def instructionsRedrawAll(canvas, data):
    canvas.create_rectangle(data.back[0],data.back[1],data.back[0] + data.back[2]*2,
            data.back[1] + data.back[2],fill="lime green")
    canvas.create_text(data.back[0] + data.back[2],data.back[0] + data.back[2]//2, 
            text="Back", fill="white", font="bold 12")
    canvas.create_text(data.width//2,data.marginY*2,text="Instructions",font="Bold 30")
    canvas.create_image(data.width//2,data.height - 100,image=data.imageCommands)
    paragraph = """
                        There are 3 levels in this game where the user needs to solve a puzzle to light all the 
                    blue boxes. There are variety of commands to complete the board, these commands can  
                    solve the pattern of this board in a variety of ways. The Foward commands moves user
                    in the direction it is facing, rotate will move the robot 90 in either counter clockwise or 
                    clockwise. Lastly, light will turn blue tiles green and green tiles blue. The user can hard 
                    code the solution, write it iteratively or write it recursively that would move the bot to 
                    light all the squares. There is a main function called when the user clicks run, which can 
                    call a secondary function, which could call itself. 
                                                                                                
                        The user can create a board of their own to save and play later or play directly, you can
                    change the starting position and angle of the bot, as well as fill tiles with blue spaces which 
                    need to be lit up. 
                     """
    canvas.create_text(data.width//2-75,data.height//2 - 50,text=paragraph,font="Bold 22")

import tkinter
from tkinter import font
from tkinter import ttk
import os


def decode3(content):   
    result = []
    for line in content.splitlines():
        row = []
        for word in line.split(" "):
            row.append(word)
        myTuple = tuple(row)
        result.append(myTuple)
    return result

def encode3(content):
    result = ""
    for tup in content:
        result += tup[0]
        result += tup[1]
        result += "\n"
    return result


"""from 15112 notes on String-week"""


def readFile(path):
    with open(path, "rt") as f:
        return f.read()

path1=os.getcwd()+"\\score.txt"
content = readFile(path1)

treeColumns = ("Player", "Score")
treeData = decode3(content)


def sortby(tree, col, descending):
    """Sort tree contents when a column is clicked on."""
    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    data.sort(reverse=descending)
    for indx, item in enumerate(data):
        tree.move(item[1], '', indx)
    tree.heading(col,
        command=lambda col=col: sortby(tree, col, int(not descending)))


"""https://docs.python.org/3/library/tkinter.ttk.html"""
"""https://svn.python.org/projects/stackless/trunk/Demo/tkinter/ttk/treeview_multicolumn.py"""

class App(object):
    def __init__(self):
        self.tree = None
        self.setupWidgets()
        self.buildTree()

    def setupWidgets(self):
        container = ttk.Frame()
        container.pack(fill='both', expand=True)
        self.tree = ttk.Treeview(columns=treeColumns, show="headings")
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

    def buildTree(self):
        for col in treeColumns:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
            self.tree.column(col, width=font.Font().measure(col.title()))

        for item in treeData:
            self.tree.insert('', 'end', values=item)
            for indx, val in enumerate(item):
                ilen = font.Font().measure(val)
                if self.tree.column(treeColumns[indx], width=None) < ilen:
                    self.tree.column(treeColumns[indx], width=ilen)

