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

        
        oImage = QImage("every_background.jpg")
        sImage = oImage.scaled(QSize(self.wScr,self.hScr))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        """
        palette = QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap("background.png")))
        self.setPalette(palette)
        """
        fontDB = QFontDatabase()
        font_id = fontDB.addApplicationFont("./neodgm.ttf")
        families = fontDB.applicationFontFamilies(font_id)
        self.families_def = families

        label = QLabel('순위표', self)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont(families[0], 74))

        label_enter = QLabel('', self)
        label_enter.setAlignment(Qt.AlignCenter)
        label_enter.setFont(QFont(families[0], 30))

        label_enter1 = QLabel('', self)
        label_enter1.setAlignment(Qt.AlignCenter)
        label_enter1.setFont(QFont(families[0], 5))

        label_enter2 = QLabel('', self)
        label_enter2.setAlignment(Qt.AlignCenter)
        label_enter2.setFont(QFont(families[0], 10))

        self.big_data = QLabel(f'1위. {self.score_data[0]}점\n2위. {self.score_data[1]}점\n3위. {self.score_data[2]}점', self)
        self.big_data.setAlignment(Qt.AlignCenter)
        self.big_data.setFont(QFont(families[0], 43))

        self.small_data = QLabel(f'4위. {self.score_data[3]}점\n5위. {self.score_data[4]}점\n6위. {self.score_data[5]}점\n7위. {self.score_data[6]}점\n8위. {self.score_data[7]}점\n9위. {self.score_data[8]}점\n10위. {self.score_data[9]}점', self)
        self.small_data.setAlignment(Qt.AlignCenter)
        self.small_data.setFont(QFont(families[0], 23))

        btn = QPushButton(self)
        btn.setGeometry(200, 150, 100, 30)
        btn.clicked.connect(self.handleButton)
        btn.setStyleSheet(" background-color: rgba(255, 255, 255, 0); ")
        btn.setIcon(QIcon('start_button.png'))
        btn.setIconSize(QSize(self.hScr*0.25, self.hScr*0.25))
        btn.setMaximumHeight(200)

        layout = QGridLayout()
        layout.addWidget(label, 0, 0)
        layout.addWidget(label_enter, 1, 0)
        layout.addWidget(self.big_data, 2, 0)
        layout.addWidget(label_enter1, 3, 0)
        layout.addWidget(self.small_data, 4, 0)
        layout.addWidget(label_enter1, 5, 0)
        layout.addWidget(label_enter2, 6, 0)
        layout.addWidget(btn,7 ,0)

        layout1 = QVBoxLayout()
        layout1.addStretch(1)
        layout1.addLayout(layout)
        layout1.addStretch(10)
        

        self.setPalette(palette)
        self.setLayout(layout1)
        self.setWindowTitle('순위표')
        self.setWindowIcon(QIcon('snack.png'))
        
    def handleButton(self):
        startfile('main.py')
        sys.exit()
def reload_appear(mainwindows):
    mainwindows.reload()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindows = MainWindow()
    mainwindows.show()
    sys.exit(app.exec())
