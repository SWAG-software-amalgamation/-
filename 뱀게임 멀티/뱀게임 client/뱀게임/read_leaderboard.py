from tkinter import *
import tkinter.font as tkFont
import threading
from time import sleep
from os import startfile

def read_score():
   while True:
      sleep(0.1)
      score = [0,0,0,0,0,0,0,0,0,0]
      try:
         with open('score.txt','r') as f:
            data = f.read()[1:].split('\n')
         for i in range(len(data)):
            score.append(int(data[i]))
         score.sort()
         score = score[::-1]
      except:
         pass
      fontExample = tkFont.Font(family="neodgm.ttf", size=40)
      scorelbl.configure(font=fontExample, text=f'''1위: {score[0]}점
2위: {score[1]}점
3위: {score[2]}점
4위: {score[3]}점
5위: {score[4]}점
6위: {score[5]}점
7위: {score[6]}점
8위: {score[7]}점
9위: {score[8]}점
10위: {score[9]}점\n''')

      

def game_start(event = None):
   try:
      startfile('main.py')
   except:
      pass

root = Tk()
background_image = PhotoImage(file="background.png")
text_background_image = PhotoImage(file="text_background.png")
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

root.title('순위표')

empty = Label(root)
empty.config()
empty.pack()

leaderboardlbl = Label(root,text='Leaderboard')
leaderboardlbl.config(image=text_background_image,font=("neodgm.ttf", 40))
leaderboardlbl.pack()

scorelbl = Label(root,text='')
scorelbl.config(font=("", 30))
scorelbl.pack()

initlbl = Label(root,text='시작하기')
initlbl.config(font=("", 25))
initlbl.pack()
initlbl.bind('<Button-1>', game_start)

mainthread = threading.Thread(target=read_score)
mainthread.daemon = True
mainthread.start()

root.mainloop()
