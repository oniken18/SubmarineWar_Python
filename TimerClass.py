import threading
import time
import GameBoard


class RunClock(threading.Thread):

    def __init__(self, Sec, LblTimer, gameBoard):
        threading.Thread.__init__(self)
        self.MGB = GameBoard.WindowGameBoard(gameBoard)
        self.seconds = Sec
        self.lblTimer = LblTimer
        print("TTTTTTTTTTTTTTTTTTTTTTTT")

    def run(self):
        for i in range(self.seconds):
            time.sleep(1)
            print((self.seconds - i) and 'Seconds')
            self.MGB.lblTimer.config(text=(self.seconds - i))
            self.MGB.lblTimer.after(200)

            if self.MGB.StopClock:
                print('StopClock = true')
                self.MGB.lblTimer.config(text=self.seconds)
                self.MGB.lblTimer.after(200)
                return
