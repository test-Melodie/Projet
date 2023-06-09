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
        colors = [
        (255, 0, 0, 3000),  #rouge
        (0, 255, 0, 5000),  #vert
        (0, 0, 255, 7000)   #bleu
        ]
        self.agent.tirer(True)
        self.agent.robot.setLedAnimation(colors)
    
    def onNonTirClicked(self):
        self.agent.tirer(False)

    def onAutomatiqueClicked(self):
       """
       Lorsque le bouton est cliqué, cela lance le programme automatique
       """
       self.changerEtatFSM1()
       self.changerEtatFSM1Recherche()
       self.rechercheMin()
       self.eval()
       self.evaluer()
       self.AllerGauche()
       self.AllerDroite()
       self.AllerBas()
       self.AllerHaut()
       self.rechercher()
       self.poursuivre()
       if (etatFSM1 == "recherche"):
                    rechercher()
       elif (etatFSM1 == "poursuite"):
                    poursuivre()
       elif (etatFSM1 == "evaluation"):
                    evaluer()

def changerEtatFSM1(nouvelEtat):
  """
  Passe à un nouvel état dans la machine à état FSM1
  :param nouvelEtat: 	Prochaine état souhaité parmi les valeurs suivantes : "recherche", "poursuite", "veille"
  :type nouvelEtat: 	str
  """
  global etatFSM1
  print("Changement d'état FSM1 de", etatFSM1, "vers", nouvelEtat)
  etatFSM1 = nouvelEtat


def changerEtatFSMRecherche(nouvelEtat):
  global etatFSMRecherche
  print("Changement d'état FSM Recherche de", etatFSMRecherche, "vers",
        nouvelEtat)
  etatFSMRecherche = nouvelEtat


def rechercheMin(dictionnaire):
  """
  Renvoie la valeur et la clé minimale
  :param dictionnaire: où trouver le minimum
  :type dictionnaire: la clé est juste renvoyée, la valeur est un nombre entier
  :return: renvoie un Tuple d'abord la clé puis la valeur entière
  """
  minimum = None
  min_cle = None
  for cle, valeur in dictionnaire.items():
    if minimum is None or valeur < minimum:
      minimum = valeur
      min_cle = cle
  return (min_cle, minimum)


def eval(agentRef, voisin):
  """
  Permet de retourner un nombre qui est le coût de déplacement
  :param agent: notre agent 
  :type agent: est un dictionnaire, clés : attributs agent (vie, munitions, distance), valeurs correspondant aux clés
  :param voisin: le voisin à évaluer
  :type voisin: est un dictionnaire, clés : attributs voisin (vie, munitions, distance), valeurs correspondant aux clés
  :return: coût en nombre float ou int
  """
  dx = (agentRef["x"] - voisin["x"])**2
  dy = (agentRef["y"] - voisin["y"])**2
  #ajout libre pour d'autres critères
  return dx + dy


def evaluer():
  agent.changerCouleur(255, 0, 255)
  global voisinCibleInfos
  # Evalue toutes les possibilités : pour chaque agent ennemi dont l'id est mis en clé, on associe en valeur son coût calculé par l'heuristique eval
  possibilites = {}
  for voisinId, voisinInfos in agent.voisins.items():
    agentInfo = {"x": agent.x, "y": agent.y}
    possibilites[voisinId] = eval(agentInfo, voisinInfos)
  # Si des ennemis sont dans le dico possibilités ...
  if (len(possibilites) > 0):
    # Trouver celui qui à le score minimum
    voisinCibleId, voisinCibleCout = rechercheMin(possibilites)
    # Puis se déplacer à sa position en la récupérant dans le dico agent voisin
    voisinCibleInfos = agent.voisins[voisinCibleId]
    changerEtatFSM1("poursuite")
  else:
    changerEtatFSM1("recherche")


def allerGauche():
  if (agent.x == 0 and agent.y == 29):
    changerEtatFSMRecherche("haut")
  else:
    agent.deplacerVers(0, 29)


def allerHaut():
  if (agent.x == 0 and agent.y == 0):
    changerEtatFSMRecherche("droite")
  else:
    agent.deplacerVers(0, 0)


def allerDroite():
  if (agent.x == 39 and agent.y == 0):
    changerEtatFSMRecherche("bas")
  else:
    agent.deplacerVers(39, 0)


def allerBas():
  if (agent.x == 39 and agent.y == 29):
    changerEtatFSMRecherche("gauche")
  else:
    agent.deplacerVers(39, 29)


def rechercher():
  if (len(agent.voisins) != 0):
    # Ajouter la condition pour appeler la fonction de poursuite
    changerEtatFSM1("evaluation")
  else:
    agent.changerCouleur(0, 255, 0)
    # Appel de la fonction d'état de notre FSM recherche
    if (etatFSMRecherche == "gauche"):
      allerGauche()
    elif (etatFSMRecherche == "haut"):
      allerHaut()
    elif (etatFSMRecherche == "droite"):
      allerDroite()
    elif (etatFSMRecherche == "bas"):
      allerBas()

    agent.orienter((agent.orientation + 1) % 4)


def poursuivre():
  global voisinCibleInfos
  if (agent.x == voisinCibleInfos["x"] and agent.y == voisinCibleInfos["y"]):
    changerEtatFSM1("recherche")
  else:
    agent.changerCouleur(255, 0, 0)
    agent.deplacerVers(voisinCibleInfos["x"], voisinCibleInfos["y"])
    agent.tirer(True)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()