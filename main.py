import sys
from PyQt5 import uic, QtWidgets
import j2l.pytactx.agent as pytactx


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("mainwindow.ui", self)

    def onLoginIdChanged(self, Qstring):
        print("Login Id changed:", Qstring)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()