# Projet 📌
---
## Pour commencer 🚀
Ce projet concerne la création d'un robot avec différentes fonctionnalités dont le tir, l'orientation... et une interface de commande à distance manuel et automatiques. 

## User stories 🎯
Voici les différentes étapes et fonctionnalités à développer.

Affichage du robot dans une application desktop :
- Afficher le robot en vue de dessus avec quatre orientations possibles.
- Adapter automatiquement la taille de l'affichage à la dimension de la fenêtre.
- Varier l'affichage du robot en fonction de son thème, de son état en temps réel et de son environnement.

Contrôle des comportements du robot :
- Adapter l'application à la taille de la fenêtre.
- Offrir deux modes de comportement : manuel et automatique.
Mode manuel : permettre à l'utilisateur de donner des instructions au robot via des boutons.
Mode automatique : exécuter un script prédéfini sans intervention de l'utilisateur.
- Le robot doit tirer, évaluer ses ennemis

Interface desktop :
- Créer une interface desktop pour gérer l'affichage du robot.
- Afficher les attributs du robot dans l'arène.
- Ajouter des boutons pour commander le robot à distance.

Connexion à l'arène :
- Permettre à l'utilisateur de saisir le nom du robot et le mot de passe via une zone de texte.
- Ajouter un bouton de connexion pour établir la connexion avec l'arène.

## Lien maquette 🔗
Le design crée sur Qt Designer est inspiré de ma maquette sur Adobe XD :
- https://xd.adobe.com/embed/8a468f7d-195b-4bd0-898e-96d4b8450e05-df15/

## Diagramme FSM mermaid 🔁
Il sert à montrer les différents états dans lequel le robot passe lors du mode automatique.
[![](https://mermaid.ink/img/pako:eNp1kE1OwzAQha9izRIlVez8e4GE1J6AHYSFSUbUonGCY0eUqAfKOXIxnNKQClFLluyZ9755mgHKpkLg0BlhcCvFmxa137NCEXee716I79-T3dzsxYFwsp3GV2t-2r_lRdM2VndWGnTCnVJYSyKVmUaNXSeUIdPo1HYaCSrSW7xB0VjuUbvrKA-2tMrJb7NWyOr7k_kSRWPr7NeONe9_sy82YYz4OIeehx5kLdXCAA9q1LWQldvgMNcKMHussQDunpXQ7wUU6uR0wprm8ahK4EZb9MC21brwpdgK9dQ011_gA3wCp9GG0TgJwoglWZTEee7BEXi2SSjLaZIymkZRFocnD77OgGCT0ihhjIZ5HgYpi-npGybTphc?type=png)](https://mermaid.live/edit#pako:eNp1kE1OwzAQha9izRIlVez8e4GE1J6AHYSFSUbUonGCY0eUqAfKOXIxnNKQClFLluyZ9755mgHKpkLg0BlhcCvFmxa137NCEXee716I79-T3dzsxYFwsp3GV2t-2r_lRdM2VndWGnTCnVJYSyKVmUaNXSeUIdPo1HYaCSrSW7xB0VjuUbvrKA-2tMrJb7NWyOr7k_kSRWPr7NeONe9_sy82YYz4OIeehx5kLdXCAA9q1LWQldvgMNcKMHussQDunpXQ7wUU6uR0wprm8ahK4EZb9MC21brwpdgK9dQ011_gA3wCp9GG0TgJwoglWZTEee7BEXi2SSjLaZIymkZRFocnD77OgGCT0ihhjIZ5HgYpi-npGybTphc)

## Prérequis ⭐
- Python 3
- Qt5

## Dépendances 💫
- pip install pyqt5
- pip install paho-mqtt
- pip install pillow
- dossier j2l (auteur: jusdeliens)
- images format svg pour Qt designer (vie, munitions, agent et orientation)
Les icônes vecteurs du coeur et de la cible proviennent du site, elles sont open source : https://iconify.design/

## Installation 📂
Qt Designer (pour le fichier .ui)

## Fabriqué avec 🔨

 - Visual Studio Code
 - Qt Designer

## Auteur 👤
- **Bellot Mélodie** _alias_ @test-Melodie

## License 📝
Ce projet est concédé sous licence selon les termes de la licence CC BY-NC-ND 3.0 licence : https://creativecommons.org/licenses/by-nc-nd/3.0/.