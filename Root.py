#Imports
import pygame
import Engine
from pygame.locals import *

#Class Joueur
class Root(Engine.Entity) :
  def __init__(self, name, moteur, pos) :
    #Permet d'appeler la fonction __init__() d'Objet
    super().__init__(name, moteur)

    self.pos = pos
    
    self.InitSprite("Assets/Root.png")
    self.InitRect(self.pos, [16, 16])