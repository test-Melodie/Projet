import sys
from PyQt5 import uic, QtWidgets, QtCore
import j2l.pytactx.agent as pytactx

agent=None
# État initial de la machine à états FSM1
etatFSM1 = "recherche"  # valeurs possibles : "recherche", "evaluation", "poursuite", "attaque"
# État initial de la recherche
etatFSMRecherche = "gauche"  # valeurs possibles : "gauche", "haut", "droite", "bas"
voisinCibleInfos = None

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
        self.agent = pytactx.AgentFr(
            nom=self.name, 
            arene="numsup2223beta", 
            username="demo",
            password=self.password, 
            url="mqtt.jusdeliens.com", 
            verbosite=3
        )        
        self.timer.start()

    def onLoginIdChanged(self, name):
        self.name=name
        print("Login Id changed:", name)

    def onPasswordChanged(self, password):
        self.password=password

    def onTimerUpdate(self):
        if ( self.agent != None ):
            self.agent.actualiser()
            if ( self.agent.vie > self.ui.LifeBar.maximum() ):
                self.ui.LifeBar.setMaximum(self.agent.vie)
            self.ui.LifeBar.setValue(self.agent.vie)
            if ( self.agent.vie > self.ui.MunitionsBar.maximum() ):
                self.ui.MunitionsBar.setMaximum(self.agent.munitions)
            self.ui.MunitionsBar.setValue(self.agent.munitions)

    def onManuelClicked(self):
        self.onHautClicked()
        self.onGaucheClicked()
        self.onDroiteClicked()
        self.onBasClicked()
        self.onTirClicked()
        self.onNonTirClicked()
    
    def onHautClicked(self):
        x,y = self.agent.x, self.agent.y
        self.agent.deplacerVers(x,y-1)
        print("Direction : haut")

    def onGaucheClicked(self):
        x,y = self.agent.x, self.agent.y
        self.agent.deplacerVers(x-1,y)
        print("Direction : gauche")

    def onDroiteClicked(self):
        x,y = self.agent.x, self.agent.y
        self.agent.deplacerVers(x+1,y)
        print("Direction : droite")

    def onBasClicked(self):
        x,y = self.agent.x, self.agent.y
        self.agent.deplacerVers(x,y+1)
        print("Direction : bas")
    
    def onTirClicked(self):
        self.agent.tirer(True)
    
    def onNonTirClicked(self):
        self.agent.tirer(False)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()