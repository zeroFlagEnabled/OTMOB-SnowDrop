#Imports
import pygame
from data import Engine
from pygame.locals import *

#Class Joueur
class Stone(Engine.Entity) :
  def __init__(self, name, moteur, pos) :
    #Permet d'appeler la fonction __init__() d'Objet
    super().__init__(name, moteur)

    self.InitSprite("data/StoneTile.png")
    self.InitRect(pos, [16, 16])