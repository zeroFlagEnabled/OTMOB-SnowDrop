#Imports
import Engine
import GameManager

#Main
if __name__ == "__main__" :

    #Dimensions de la fenêtre
    largeur = 600 #1024
    longueur = 600 #768

    #Initialise le moteur
    moteur = Engine.Moteur(longueur, largeur)

    #On crée et initialise un manger qui va gérer le flow du jeu
    manager = GameManager.Manager(moteur)
    manager.Setup()

    #On fait tourner le manager
    manager.Run()
    #moteur.Run()