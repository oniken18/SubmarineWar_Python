import ast
import json as json
import threading
import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from BoxClass import Box
from SubmarineClass import Submarine


class WindowGameBoard:
    isGameOn = False
    opponentBoxes = []
    boxes = []
    BoxesWar = []
    submarines = []
    smallBoxes = []
    nmWidth = 1000
    nmHeight = 700
    size = 10, 10
    GameId = 0
    NmMe = 0
    NmOpponent = 0
    MyTurn = False
    Sec = 60
    BoxesJson = ""
    timeIsUp = False
    StopClock = False
    isStartPressed = False
    isGameOver = False

    # def RunClock(self):
    #     seconds = 60
    #     for i in range(seconds):
    #         time.sleep(1)
    #         self.lblTimer.config(text=(seconds-i))
    #         self.lblTimer.after(200)
    #
    #         if self.StopClock:
    #             self.lblTimer.config(text=seconds)
    #             self.lblTimer.after(200)
    #             break
    #
    #     if self.StopClock:
    #         self.StopClock = False
    #     else:
    #         self.timeIsUp = True

    def CheckWin(self):
        isWin = True

        for box in self.boxes:
            if box.isSubmarine and not box.isChecked:
                isWin = False

        if isWin:
            self.isGameOver = True
            msg = "You Win"
            tk.messagebox.showinfo(message=msg)
            print("You Win")

    def CheckOpponentWin(self):
        isOpWin = True

        for OpBox in self.smallBoxes:
            if OpBox.isSubmarine and not OpBox.isChecked:
                isOpWin = False

        if isOpWin:
            self.isGameOver = True
            msg = "You Loss"
            tk.messagebox.showinfo(message=msg)
            print("You Loss")

    def CheckOpponent(self):
        PARAMS = {'GameId': self.GameId}
        myURL = 'http://oniken.c1.biz/server/actions/CheckOpponent.php?'

        while not self.isGameOn and not self.timeIsUp:
            r = requests.get(url=myURL, params=PARAMS)

            if r.text != '0':
                self.opponentBoxes = (r.json()[0]['OpBoxes'])
                self.opponentBoxes = ast.literal_eval(self.opponentBoxes)
                self.isGameOn = True

        if not self.isGameOn or self.timeIsUp:
            msg = "no opponent! game canceled"
            popup = tk.messagebox.showinfo(message=msg)
            PARAMS = {'GameId': self.GameId}
            myURL = 'http://oniken.c1.biz/server/actions/CancelGame.php?'
            r = requests.get(url=myURL, params=PARAMS)
            return

        smallBoard = tk.Frame(self.canvas, bd=2, bg='#DDDDDD')
        smallBoard.place(width=304, height=304, x=670, y=30)

        counter = 0
        for i in range(20):
            for j in range(20):
                smallBox = tk.Label(smallBoard, bd=1, relief="solid")
                MyBox2 = Box(counter, smallBox, self)
                if self.boxes[counter].isSubmarine:
                    smallBox.configure(background='green')
                    MyBox2.isSubmarine = True

                smallBox.place(width=15, height=15, relx=j / 20, rely=i / 20)
                self.smallBoxes.append(MyBox2)

                counter = counter + 1

        for bx in self.boxes:
            bx.lblBox.bind("<Button-1>", bx.ShootBox)
            bx.isSubmarine = False

        for nm in self.opponentBoxes:
            self.boxes[nm - 1].isSubmarine = True

        for sub in self.submarines:
            sub.lblSubmarine.destroy()

        self.submarines.clear()
        self.butStart.destroy()

        if not self.MyTurn:
            self.SetMyTurnThread()

    def SetMyTurnThread(self):
        MyTurnThread = threading.Thread(target=self.SetMyTurn)
        MyTurnThread.start()

    def SetMyTurn(self):
        self.MyTurn = False
        self.lblUserTurn.config(text='Opponent Turn')
        PARAMS = {'GameId': self.GameId, 'NmMe': self.NmMe}
        myURL = 'http://oniken.c1.biz/server/actions/CheckForOpponentHit.php?'

        while not self.timeIsUp and not self.MyTurn:
            r = requests.get(url=myURL, params=PARAMS)
            if r.json()[0]['Hit'] != '-1':
                self.opponentBoxes = (r.json()[0]['Hit'])
                self.opponentBoxes = ast.literal_eval(self.opponentBoxes)
                self.MyTurn = True
                self.lblUserTurn.config(text='My Turn')
                self.smallBoxes[self.opponentBoxes].setHit()

        if not self.MyTurn or self.timeIsUp:
            msg = "opponent Left The Game! game canceled"
            popup = tk.messagebox.showinfo(message=msg)
            PARAMS = {'GameId': self.GameId}
            myURL = 'http://oniken.c1.biz/server/actions/CancelGame.php?'
            r = requests.get(url=myURL, params=PARAMS)
            return

    def setLblTimer(self):
        self.lblTimer.config(text=self.Sec)
        self.Sec = self.Sec - 1
        self.root.after(500, self.setLblTimer)

    def startGame(self):
        if self.isStartPressed:
            return

        for sub in self.submarines:
            if sub.GetFirstBox() == 0:
                msg = "put all submarines on the board"
                tk.messagebox.showinfo(message=msg)
                return
        self.BoxesWar.clear()

        for box in self.boxes:
            box.isSubmarine = False

        msg = "submarines can not touch"
        for sub in self.submarines:
            if sub.isVertical:
                for nm in range(sub.size):
                    if self.boxes[int(sub.SubFirstBox + (20 * nm - 1))].isSubmarine:
                        tk.messagebox.showinfo(message=msg)
                        return
                    self.boxes[int(sub.SubFirstBox + (20 * nm - 1))].isSubmarine = True
                    self.BoxesWar.append(int(sub.SubFirstBox + (20 * nm)))
            else:
                for nm in range(sub.size - 1):
                    if self.boxes[int(sub.SubFirstBox + nm)].isSubmarine:
                        tk.messagebox.showinfo(message=msg)
                        return
                    self.boxes[int(sub.SubFirstBox + nm)].isSubmarine = True
                    self.BoxesWar.append(int(sub.SubFirstBox + nm))

        self.isStartPressed = True
        self.BoxesJson = json.dumps(self.BoxesWar)
        PARAMS = {'Id': self.MyId, 'SubList': self.BoxesJson}
        myURL = 'http://oniken.c1.biz/server/actions/NewGame.php?'
        r = requests.get(url=myURL, params=PARAMS)

        if len(r.json()[0]) == 2:
            self.GameId = (r.json()[0]['GameId'])
            self.opponentBoxes = (r.json()[0]['OpBoxes'])
            self.opponentBoxes = ast.literal_eval(self.opponentBoxes)
            self.isGameOn = True
            self.MyTurn = False
            self.lblUserTurn.config(text='My Turn')
            self.NmOpponent = 1
            self.NmMe = 2
        else:
            self.GameId = (r.json()[0]['GameId'])
            self.MyTurn = True
            self.lblUserTurn.config(text='Opponent Turn')
            self.NmOpponent = 2
            self.NmMe = 1

        thread2 = threading.Thread(target=self.CheckOpponent)
        thread2.start()

    def __init__(self, root, myId):

        def StartGameThread(event):
            thread1 = threading.Thread(target=self.startGame)
            thread1.start()

        load = Image.open(r"Graphics\WhiteArrow.png")
        load.thumbnail(self.size, Image.ANTIALIAS)
        arrowIMG = ImageTk.PhotoImage(load)

        self.MyId = myId
        self.root = root
        self.root.title = 'Submarine War'

        self.canvas = tk.Canvas(self.root, width=self.nmWidth, height=self.nmHeight)
        self.canvas.pack()

        # self.lblTimer = tk.Label(self.canvas, text='60', bd=1, relief="solid")
        # self.lblTimer.place(width=50, height=25, x=900, y=350)

        # self.ClockThread = RunClock(60, self.lblTimer, self)

        self.lblUserTurn = tk.Label(self.canvas, font=("Helvetica", 24), text='', bd=1, relief="solid")
        self.lblUserTurn.place(width=150, height=50, x=750, y=400)

        self.boardFrame = tk.Frame(self.canvas, bd=2, bg='#DDDDDD')
        self.boardFrame.place(width=604, height=604, x=27, y=27)

        self.butStart = tk.Button(self.canvas, text='Ready To Start')
        self.butStart.bind("<Button-1>", StartGameThread)
        self.butStart.place(x=650, y=600)

        counter = 0
        for i in range(4):
            for j in range(2):
                submarine1 = Submarine(counter, i + 1)

                lblSubmarine = tk.Frame(self.canvas, bd=1, relief="solid", bg='#FF0000')
                lblSubmarine.bind("<B1-Motion>", submarine1.MoveSubmarine)
                lblSubmarine.bind("<Button-1>", submarine1.mousePos)
                lblSubmarine.bind("<ButtonRelease-1>", submarine1.checkSubPos)
                lblSubmarine.place(width=28, height=((30 * (i + 1)) - 2), x=((counter + 1) * 35) + 650, y=80)

                Arrow = tk.Label(lblSubmarine, font="Wingdings", text='', bg='#FF0000', image=arrowIMG)
                Arrow.bind("<Button-1>", submarine1.setDirection)
                Arrow.place(width=25, height=20)
                submarine1.addArrow(Arrow)

                submarine1.addLblSubmarine(lblSubmarine)
                self.submarines.append(submarine1)
                counter = counter + 1

        counter = 0
        for i in range(20):
            for j in range(20):
                BigBox = tk.Button(self.boardFrame, bd=1, text='', relief="solid")
                MyBox = Box(counter, BigBox, self)
                BigBox.place(width=30, height=30, relx=j / 20, rely=i / 20)
                self.boxes.append(MyBox)
                counter = counter + 1

        WinW = root.winfo_screenwidth()
        WinH = root.winfo_screenheight()
        size = tuple(int(pos) for pos in root.geometry().split('+')[0].split('x'))
        x = WinW / 2 - self.nmWidth / 2
        y = WinH / 2 - ((self.nmHeight / 2) + 30)
        root.geometry("%dx%d+%d+%d" % (self.nmWidth, self.nmHeight, x, y))

        self.root.mainloop()
