import sys
from subprocess import run,PIPE,CREATE_NO_WINDOW
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import (QWidget,QLineEdit, QApplication,QTextEdit,QPushButton)
from PyQt5.QtCore import Qt
class Example(QWidget):
    cmd=None
    cmd_Geometry=[0,0,500,30]
    Geometry=[710,0,500,30,180,3]
    result=None
    hideButton=None
    historyCmd=[]
    hide=False
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)
    def initUI(self):
        self.cmd = QLineEdit(self)
        self.cmd.setGeometry(self.cmd_Geometry[0],self.cmd_Geometry[1],self.cmd_Geometry[2],self.cmd_Geometry[3])
        self.cmd.returnPressed.connect(self.onChanged)
        self.cmd.setStyleSheet("border:none");
        self.result = QTextEdit(self)
        self.result.setFocusPolicy(Qt.NoFocus)
        self.result.setVisible(False)
        self.result.verticalScrollBar().hide()
        self.result.resize(0,0)
        self.result.setStyleSheet("border:none");
        self.hideButton = QPushButton(self)
        self.hideButton.setText("↑")
        self.hideButton.setStyleSheet("border:none")
        self.hideButton.setGeometry(470,0,30,30)
        self.hideButton.clicked.connect(self.hideWindow)
        self.hideButton.show()
        self.setGeometry(self.Geometry[0],self.Geometry[1],self.Geometry[2],self.Geometry[3])
        self.setMaximumSize(500,180)
        self.setMinimumSize(500,0)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setStyleSheet("border:none");
        self.show()
    def onChanged(self):
        s=self.cmd.text()
        show=False
        if(s=="hide"):
            self.cmd.clear()
            self.result.clear()
            self.result.resize(0, 0)
            self.result.setVisible(True)
            self.resize(self.Geometry[2],self.Geometry[3])
            return
        if(s=="clear"):
            self.cmd.clear()
            self.result.clear()
            return
        if(s=="exit"):
            self.close()
        if(s[-2:]=="  "):
            s=s[0:-2]
            show=True
        args1 = [r"powershell", s]
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
    ex = Example()
    sys.exit(app.exec_())
