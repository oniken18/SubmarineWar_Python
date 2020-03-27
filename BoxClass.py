import requests


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
            else:
                self.lblBox.config(text='X')

            PARAMS = {'GameId': self.GB.GameId, 'BoxNm': self.boxID, 'nmMe': self.GB.NmMe}
            myURL = 'http://oniken.c1.biz/server/actions/SendBoxNm.php?'
            requests.get(url=myURL, params=PARAMS)
            self.GB.SetMyTurn()

    def setHit(self):
        self.isChecked = True
        if self.isSubmarine:
            self.lblBox.config(bg='Red')
        else:
            self.lblBox.config(text='X')
