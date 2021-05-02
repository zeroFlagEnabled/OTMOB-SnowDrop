#Imports
import pygame
from data import Engine
from pygame.locals import *

#Class Joueur
class Graine(Engine.Entity) :
  def __init__(self, name, moteur) :
    #Permet d'appeler la fonction __init__() d'Objet
    super().__init__(name, moteur)

    self.InitSprite("data/Graine.png")
    self.InitRect([moteur.Rlongueur//2 - 4, moteur.Rlargeur - 34], [8, 8])