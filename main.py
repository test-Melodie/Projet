import sys
from PyQt5 import uic, QtWidgets
import j2l.pytactx.agent as pytactx

agent=None

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password=""
        self.name=""
        uic.loadUi("mainwindow.ui", self)

    def onLoginIdChanged(self, name):
        self.name=name
        print("Login Id changed:", name)

    def onPasswordChanged(self, password):
        self.password=password
    
    def onConnexionClick(self):
        global agent
        agent=pytactx.AgentFrInoffensif(nom=self.name,
                        arene="numsup2223",
                        username="demo",
                        password=self.password,
                        url="mqtt.jusdeliens.com",
                        verbosite=3)
        while True:
            agent.actualiser()
            print("Connexion")
        
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()