from tkinter import *
from Bot import *

def splashScreenMousePressed(event, data):
    if data.width//2-data.r < event.x < data.width//2+data.r and\
        data.height//1.75-data.r//3 < event.y < data.height//1.75+data.r//3:
            data.mode = "instructions"
    elif data.width//2-data.r < event.x < data.width//2+data.r and\
        data.height//2.8-data.r//3 < event.y < data.height//2.8+data.r//3:
            data.mode = "playGame"

def splashScreenKeyPressed(event, data):
    pass

def splashScreenTimerFired(data):
    pass

def splashScreenRedrawAll(canvas, data):
    canvas.create_image(data.width//2,data.height//2,image=data.imageBackground)
    canvas.create_rectangle(data.width//2-data.r,data.height//1.75-data.r//3,
        data.width//2+data.r,data.height//1.75+data.r//3,fill="cadet blue")
    canvas.create_text(data.width//2,data.height//1.75,text="Instructions",font="bold 30",fill="white")
    canvas.create_rectangle(data.width//2-data.r,data.height//2.8-data.r//3,
        data.width//2+data.r,data.height//2.8+data.r//3,fill="cadet blue")
    canvas.create_text(data.width//2,data.height//2.8,text="Play",font="bold 30",fill="white")
    if data.mode == "splashScreen":
        data.effect1.updateimage(0,canvas,data,data.width//4,data.height//2)
        data.effect2.updateimage(0,canvas,data,data.width//1.55,data.height//3.7)