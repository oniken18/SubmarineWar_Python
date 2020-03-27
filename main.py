import tkinter as tk
from tkinter import messagebox
import requests
from GameBoard import WindowGameBoard


class WindowLogin:
    def __init__(self):
        def SignUp():
            x = 1

        def Login(event):
            if self.EntryName.get() == 'Enter name..' or self.EntryPassword.get() == 'Enter Password..':
                msg = 'fill name and password'
                popup = tk.messagebox.showinfo(message=msg)
                return
            PARAMS = {'name': self.EntryName.get(), 'password': self.EntryPassword.get()}
            myURL = 'http://oniken.c1.biz/server/actions/loginUser.php?'
            r = requests.get(url=myURL, params=PARAMS)
            if r.json() == '0':
                msg = 'Wrong name or passeord'
                popup = tk.messagebox.showinfo(message=msg)
                return
            else:
                # GameWindow = tk.Toplevel(self.master)
                self.canvas.destroy()
                app = WindowGameBoard(self.root)

        def resetName(event):
            if self.EntryName.get() == 'Enter name..':
                self.EntryName.delete(0, 12)
                self.EntryName.config(fg='black')

        def CheckTxt(event):
            if self.EntryName.get() == '':
                self.EntryName.insert(0, 'Enter name..')
                self.EntryName.config(fg='#30c9c4')

        def resetPass(event):
            if self.EntryPassword.get() == 'Enter Password..':
                self.EntryPassword.delete(0, 16)
                self.EntryPassword.config(fg='black')

        def CheckPass(event):
            if self.EntryPassword.get() == '':
                self.EntryPassword.insert(0, 'Enter Password..')
                self.EntryPassword.config(fg='#30c9c4')

        self.root = tk.Tk()
        self.root.title = 'Login'
        self.canvas = tk.Canvas(self.root, width=500, height=450)
        self.canvas.pack()
        self.frame = tk.Frame(self.root, width=496, height=446, )
        self.frame.place(width=496, height=446, x=4, y=4)

        self.lblTitle = tk.Label(self.frame, text='SUBMARINES WAR', font=('Tahoma', 18, 'bold'), bg='#c20000',
                                 fg='#ffffff')
        self.lblTitle.place(width=496, y=20)

        self.EntryName = tk.Entry(self.frame, fg='#30c9c4', font=('Tahoma', 12))
        self.EntryName.insert(0, 'Enter name..')
        self.EntryName.bind("<FocusIn>", resetName)
        self.EntryName.bind("<FocusOut>", CheckTxt)
        self.EntryName.place(width=140, x=178, y=120)

        self.EntryPassword = tk.Entry(self.frame, fg='#30c9c4', font=('Tahoma', 12))
        self.EntryPassword.insert(0, 'Enter Password..')
        self.EntryPassword.bind("<FocusIn>", resetPass)
        self.EntryPassword.bind("<FocusOut>", CheckPass)
        self.EntryPassword.place(width=140, x=178, y=150)

        self.butLogin = tk.Button(self.frame, text='Login')
        self.butLogin.bind("<Button-1>", Login)
        self.butLogin.place(width=80, x=208, y=190)

        self.butSignUp = tk.Button(self.frame, text='Create new account', font=('Tahoma', 11), bg='#ffffff',
                                   fg='#000000')
        self.butSignUp.bind("<Button-1>", SignUp)
        self.butSignUp.place(width=180, x=158, y=240)

        self.root.mainloop()

Game = WindowLogin()
