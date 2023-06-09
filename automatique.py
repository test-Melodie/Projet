import sys
from PyQt5 import uic, QtWidgets, QtCore
import j2l.pytactx.agent as pytactx

agent=None
# État initial de la machine à états FSM1
etatFSM1 = "recherche"  # valeurs possibles : "recherche", "evaluation", "poursuite", "attaque"
# État initial de la recherche
etatFSMRecherche = "gauche"  # valeurs possibles : "gauche", "haut", "droite", "bas"
voisinCibleInfos = None

def setAgent(nouvelagent):
   """
   Permet de rendre fonctionnel ce code sans boucle while true.
   """
   global agent
   agent= nouvelagent

def actualiserFSM():
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
  """
  Permet d'évaluer les ennemis à proximité.
  """
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
  """
  Déplacement en vers la gauche.
  """
  if (agent.x == 0 and agent.y == 29):
    changerEtatFSMRecherche("haut")
  else:
    agent.deplacerVers(0, 29)


def allerHaut():
  """
  Déplacement en vers le haut.
  """  
  if (agent.x == 0 and agent.y == 0):
    changerEtatFSMRecherche("droite")
  else:
    agent.deplacerVers(0, 0)


def allerDroite():
  """
  Déplacement en vers la droite.
  """  
  if (agent.x == 39 and agent.y == 0):
    changerEtatFSMRecherche("bas")
  else:
    agent.deplacerVers(39, 0)


def allerBas():
  """
  Déplacement en vers le bas.
  """
  if (agent.x == 39 and agent.y == 29):
    changerEtatFSMRecherche("gauche")
  else:
    agent.deplacerVers(39, 29)


def rechercher():
  """
  Permet de rechercher les agents ennemis.
  """
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
  """
  Permet de poursuivre l'ennemi évalué pour l'attaquer et l'éliminer.
  """
  global voisinCibleInfos
  if (agent.x == voisinCibleInfos["x"] and agent.y == voisinCibleInfos["y"]):
    changerEtatFSM1("recherche")
  else:
    agent.changerCouleur(255, 0, 0)
    agent.deplacerVers(voisinCibleInfos["x"], voisinCibleInfos["y"])
    agent.tirer(True)
