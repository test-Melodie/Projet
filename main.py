import sys
from PyQt5 import uic, QtWidgets, QtCore
import j2l.pytactx.agent as pytactx
import automatique

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
        self.auto=False
        self.tir=True

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
        automatique.setAgent(self.agent)
        self.timer.start()

    def onLoginIdChanged(self, name):
        """
        Permet d'entrer le nom du robot et affiche dans la console ce qui est marqué.
        """
        self.name=name
        print("Login Id changed:", name)

    def onPasswordChanged(self, password):
        """
        Permet d'entrer le mot de passe de manière sécurisée.
        """
        self.password=password

    def onTimerUpdate(self):   
        """
        On y retrouve l'actualisation de l'agent et les barres de progression de vie et du stock de munitions. Cela permet de remplacer la boucle while true.
        """     
        if ( self.agent != None ):
            self.agent.actualiser()
            if ( self.agent.vie > self.ui.LifeBar.maximum() ):
                self.ui.LifeBar.setMaximum(self.agent.vie)
            self.ui.LifeBar.setValue(self.agent.vie)
            if ( self.agent.vie > self.ui.MunitionsBar.maximum() ):
                self.ui.MunitionsBar.setMaximum(self.agent.munitions)
            self.ui.MunitionsBar.setValue(self.agent.munitions)
            if self.auto==True:
                automatique.actualiserFSM()

    def onAutoChecked(self,isChecked):
        """
        Active le mode automatique lorsque la case est cochée 
        """
        self.auto=isChecked

    def onHautClicked(self):
        """
        Déplacement en vers le haut
        """
        x,y = self.agent.x, self.agent.y
        self.agent.deplacerVers(x,y-1)
        print("Direction : haut")

    def onGaucheClicked(self):
        """
        Déplacement en vers la gauche.
        """
        x,y = self.agent.x, self.agent.y
        self.agent.deplacerVers(x-1,y)
        print("Direction : gauche")

    def onDroiteClicked(self):
        """
        Déplacement en vers la droite.
        """
        x,y = self.agent.x, self.agent.y
        self.agent.deplacerVers(x+1,y)
        print("Direction : droite")

    def onBasClicked(self):
        """
        Déplacement en vers le bas.
        """
        x,y = self.agent.x, self.agent.y
        self.agent.deplacerVers(x,y+1)
        print("Direction : bas")
    
    def onTirChecked(self,isChecked):
        """
        Lorsque la case est cochée, le tir est activé sinon le tir est désactivé.
        """
        if self.tir==isChecked:
            self.agent.tirer(True)
        else:
            self.agent.tirer(False)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()