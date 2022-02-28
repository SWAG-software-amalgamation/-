import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from os import startfile

def score_get_data():
    return list(map(int, open("./score.txt", 'r').readlines()))

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.score_data = score_get_data()
        screen_rect = app.desktop().screenGeometry()
        wScreen, hScreen = screen_rect.width(), screen_rect.height()
        self.wScr, self.hScr = hScreen*0.7, hScreen*0.9
        #self.setFixedSize(self.wScr, self.hScr)

        self.setGeometry(100,100,self.wScr, self.hScr)

        print(score_get_data()[0])
        if score_get_data()[0] == 1:
            background_image = '부딪힘2p.jpg'
        elif score_get_data()[0] == 2:
            background_image = '부딪힘1p.jpg'
        elif score_get_data()[0] == 3:
            background_image = '추락2p.jpg'
        elif score_get_data()[0] == 4:
            background_image = '추락1p.jpg'
            
        oImage = QImage(background_image)
        sImage = oImage.scaled(QSize(self.wScr,self.hScr))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        
        self.setPalette(palette)
        #self.setLayout(layout1)
        self.setWindowTitle('순위표')
        
def reload_appear(mainwindows):
    mainwindows.reload()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindows = MainWindow()
    mainwindows.show()
    sys.exit(app.exec())
