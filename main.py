#Imports
import Engine
import GameManager

#Main
if __name__ == "__main__" :

    continuer = True

    while continuer :
        #Dimensions de la fenêtre
        #largeur = 768
        #longueur = 1024

        #Initialise le moteur
        moteur = Engine.Moteur()

        #On crée et initialise un manager qui va gérer le flow du jeu
        manager = GameManager.Manager(moteur)
        manager.Setup()

        #On fait tourner le manager
        continuer = manager.Run()
        #moteur.Run()