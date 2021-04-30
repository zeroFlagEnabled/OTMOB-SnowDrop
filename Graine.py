#Imports
import pygame
import Engine
from pygame.locals import *

#Class Joueur
class Graine(Engine.Entity) :
  def __init__(self, name, moteur) :
    #Permet d'appeler la fonction __init__() d'Objet
    super().__init__(name, moteur)

    self.InitSprite("Assets/Graine.png")
    self.InitRect([moteur.Rlongueur//2 - 8, moteur.Rlargeur//2 - 8], [16, 16])