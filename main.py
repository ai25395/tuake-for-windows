#By LTC
#2020年9月28日 18:32:01
#MIT License
import sys
from subprocess import run,PIPE,CREATE_NO_WINDOW
from PyQt5.QtGui import QMouseEvent,QFont,QColor,QGradient
from PyQt5.QtWidgets import (QWidget,QLineEdit, QApplication,QTextEdit,QPushButton)
from PyQt5.QtCore import Qt
class Tuake(QWidget):
    #cmdlineInput
    cmd=None
    cmd_Geometry=[0,0,500,30]
    #mainWindow's
    Geometry=[710,0,500,30,180,5]
    #output
    result=None
    #a button to hide the whole window
    hideButton=None
    #a flag to judge if the window is hidden
    hide=False
    def __init__(self):
        super().__init__()
        self.initUI()
        #monitoring the mouse to make it appeared
        self.setMouseTracking(True)
    def initUI(self):
        #init cmdline
        self.cmd = QLineEdit(self)
        self.cmd.setGeometry(self.cmd_Geometry[0],self.cmd_Geometry[1],self.cmd_Geometry[2],self.cmd_Geometry[3])
        self.cmd.returnPressed.connect(self.onReturn)
        self.cmd.setFont(QFont("Microsoft YaHei"))
        self.cmd.setStyleSheet("border:none");
        #init output
        self.result = QTextEdit(self)
        self.result.setFocusPolicy(Qt.NoFocus)
        self.result.setVisible(False)
        self.result.verticalScrollBar().hide()
        self.result.resize(0,0)
        self.result.setStyleSheet("border:none");
        #init hideButton
        self.hideButton = QPushButton(self)
        self.hideButton.setText("↑")
        self.hideButton.setStyleSheet("border:none")
        self.hideButton.setGeometry(470,0,30,30)
        self.hideButton.clicked.connect(self.hideWindow)
        #init the main window
        self.setGeometry(self.Geometry[0],self.Geometry[1],self.Geometry[2],self.Geometry[3])
        self.setMaximumSize(500,180)
        self.setMinimumSize(500,0)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("border:none");
        self.show()

    #process the command
    def onReturn(self):
        command=self.cmd.text()
        show=False
        if(command=="hide"):
            self.cmd.clear()
            self.result.clear()
            self.result.resize(0, 0)
            self.result.setVisible(True)
            self.resize(self.Geometry[2],self.Geometry[3])
            return
        if(command=="clear"):
            self.cmd.clear()
            self.result.clear()
            return
        if(command=="exit"):
            self.close()
        #if you append "  " to your command,it will show the output.
        #otherwise,there is no output
        if(command[-2:]=="  "):
            command=command[0:-2]
            show=True
        args1 = [r"powershell", command]
        ret = run(args1, shell=False,stdout=PIPE,stderr=PIPE,stdin=PIPE,creationflags=CREATE_NO_WINDOW)
        if(show):
            self.resize(500, 180)
            self.result.setVisible(True)
            self.result.move(0, 30)
            self.result.resize(500, 150)
            self.result.insertPlainText(ret.stdout.decode("GBK")+ret.stderr.decode("GBK"))
        self.cmd.clear()
    def mouseMoveEvent(self,event):
        if(self.hide==True):
            self.resize(self.Geometry[2],self.Geometry[3])
            self.cmd.resize(self.cmd_Geometry[2],self.cmd_Geometry[3])
            self.hide=False
    def hideWindow(self):
        self.resize(self.Geometry[2],self.Geometry[5])
        self.cmd.resize(0,0)
        self.hide=True
        self.result.clear()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Tuake()
    sys.exit(app.exec_())

