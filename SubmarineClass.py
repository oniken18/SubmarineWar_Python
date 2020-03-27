import tkinter as tk

import pyautogui as pag


class Submarine(object):
    SubFirstBox = 0
    isVertical = True
    hits = 0
    isDead = False
    LastPosX = 0
    LastPosY = 0
    lblSubmarine: tk.Frame

    def __init__(self, ID, size):
        self.ID = ID
        self.size = size

    def addLblSubmarine(self, lblSubmarine: tk.Frame):
        self.lblSubmarine = lblSubmarine
        self.StartX = self.lblSubmarine.place_info()["x"]
        self.StartY = self.lblSubmarine.place_info()["y"]

    def addArrow(self, lblArrow: tk.Label):
        self.lblArrow = lblArrow

    def setHit(self):
        self.hits = self.hits + 1

    def CheckSubmarine(self):
        if self.hits == self.size:
            self.isDead = True

        return self.isDead

    def setDirection(self, event):
        self.isVertical = not (self.isVertical)
        W = self.lblSubmarine.place_info()["width"]
        H = self.lblSubmarine.place_info()["height"]
        self.lblSubmarine.place(width=H, height=W)

    def mousePos(self, event):
        self.LastPosX, self.LastPosY = pag.position()

    def MoveSubmarine(self, event):
        if self.LastPosX == 0:
            self.LastPosX, self.LastPosY = pag.position()

        PosX, PosY = pag.position()

        submarineInfo = self.lblSubmarine.place_info()

        lblX = int(submarineInfo["x"])
        lblY = int(submarineInfo["y"])

        self.lblSubmarine.place(x=lblX - (self.LastPosX - PosX), y=lblY - (self.LastPosY - PosY))
        self.LastPosX = PosX
        self.LastPosY = PosY

    def checkSubPos(self, event):
        tempX = int(self.lblSubmarine.place_info()["x"])
        tempY = int(self.lblSubmarine.place_info()["y"])
        if self.isVertical:
            if (tempX < 25 or tempX > 625) or (
                    tempY < 25 or tempY > 625 - int(self.lblSubmarine.place_info()["height"])):
                self.lblSubmarine.place(x=self.StartX, y=self.StartY)
                self.SubFirstBox = 0
                return
        else:
            if (tempX < 25 or tempX > 625 - int(self.lblSubmarine.place_info()["width"])) or (
                    tempY < 25 or tempY > 625):
                W = self.lblSubmarine.place_info()["width"]
                H = self.lblSubmarine.place_info()["height"]
                self.isVertical = True
                self.lblSubmarine.place(x=self.StartX, y=self.StartY, width=H, height=W)
                self.SubFirstBox = 0
                return

        tempX = (round(tempX / 30) * 30)
        tempY = (round(tempY / 30) * 30)
        if tempX == 0:
            tempX = 30
        if tempY == 0:
            tempY = 30

        self.lblSubmarine.place(x=tempX, y=tempY)
        self.SubFirstBox = (tempX / 30) + (((tempY / 30) - 1) * 20)

    def GetFirstBox(self):
        return self.SubFirstBox

    def GetSize(self):
        return self.size

    def GetIsVertical(self):
        return self.isVertical
