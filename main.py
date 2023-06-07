import sys
from PyQt5 import uic, QtWidgets, QtCore
import j2l.pytactx.agent as pytactx

agent=None

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password=""
        self.name=""
        self.agent = None
        # Création d'un timer pour régulièrement envoyer les requêtes de l'agent au server et actualiser son état 
        self.timer = QtCore.QTimer()
        self.timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.onTimerUpdate)
        self.ui = uic.loadUi("mainwindow.ui", self)

    def onConnexionClicked(self):
        """
        Callback de slot associée au signal du PushButton 
        dans Qt Designer, via 
        - click droit sur MainWindow -> Modifier signaux/slots -> "+" -> onPushButtonClicked
        - menu Editeur de signaux et slots -> "+" -> 
            Emetteur : "pushButton"
            Signal : clicked()
            Receveur : MainWindow
            Slot : onConnexionClicked()
        """
        print("Connexion")
        self.timer.start()
        self.agent = pytactx.AgentFr(
            nom=self.name, 
            arene="numsup2223", 
            username="demo",
            password=self.password, 
            url="mqtt.jusdeliens.com", 
            verbosite=3
        )        

    def onLoginIdChanged(self, name):
        self.name=name
        print("Login Id changed:", name)

    def onPasswordChanged(self, password):
        self.password=password

    def onTimerUpdate(self):
        if ( self.agent != None ):
            self.agent.orienter((self.agent.orientation+1)%4)
            self.agent.actualiser()
            if ( self.agent.vie > self.ui.LifeBar.maximum() ):
                self.ui.LifeBar.setMaximum(self.agent.vie)
            self.ui.LifeBar.setValue(self.agent.vie)
            if ( self.agent.vie > self.ui.MunitionsBar.maximum() ):
                self.ui.MunitionsBar.setMaximum(self.agent.munitions)
            self.ui.MunitionsBar.setValue(self.agent.munitions)
    
    def onHautClicked(self):
        self.agent.deplacerVers(0,0)
        print("Direction : haut")

    def onGaucheClicked(self):
        self.agent.deplacerVers(0,29)
        print("Direction : gauche")

    def onDroiteClicked(self):
        self.agent.deplacerVers(39,0)
        print("Direction : droite")

    def onBasClicked(self):
        self.agent.deplacerVers(39,29)
        print("Direction : bas")

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()