import requests
import tkinter as tk


class Box(object):
    isChecked = False
    isSubmarine = False
    btnTxt = ""
    lblBox = ""

    def __init__(self, boxID, lblBox, GameBoard):
        self.boxID = boxID
        self.lblBox = lblBox
        self.GB = GameBoard

    def ShootBox(self, event):
        if self.GB.MyTurn and not self.isChecked:
            self.isChecked = True

            if self.isSubmarine:
                self.lblBox.config(bg='red')
                self.GB.CheckWin()
            else:
                self.lblBox.config(text='X')

            PARAMS = {'GameId': self.GB.GameId, 'BoxNm': self.boxID, 'nmMe': self.GB.NmMe}
            myURL = 'http://oniken.c1.biz/server/actions/SendBoxNm.php?'
            requests.get(url=myURL, params=PARAMS)
            self.GB.SetMyTurnThread()

    def setHit(self):
        self.isChecked = True
        if self.isSubmarine:
            self.lblBox.config(bg='Red')
            self.GB.CheckOpponentWin()
        else:
            self.lblBox.config(text='X')
