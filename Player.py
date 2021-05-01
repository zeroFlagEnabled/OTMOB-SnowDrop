#Imports
import pygame
import Engine
from pygame.locals import *

#Class Joueur
class Player(Engine.Entity) :
  def __init__(self, name, moteur) :
    #Permet d'appeler la fonction __init__() d'Objet
    super().__init__(name, moteur)

    self.engine.manager.player = self

    self.InitSprite("Assets/Bourgeon.png")
    self.InitRect([moteur.Rlongueur//2 - 8, moteur.Rlargeur//2 - 8], [16, 16])

    self.layer = 1000

    self.shown = False

    self.createCircle = False
    self.circlePos = [0,0]

  def Update(self) :

    self.Sprite = self.SpriteCopy.copy()

    if pygame.mouse.get_pressed(num_buttons = 3)[0] :
      self.shown = True
    else:
      self.shown = False
      
    if self.shown :
      #Mouvements Joueur
      self.deltaPos = [0,0]
      self.deplacement = 1

      #Mouvements Latéraux et horizontaux 
      if K_q in self.engine.keystrokes :
          self.deltaPos[0] -= self.deplacement
      if K_d in self.engine.keystrokes :
          self.deltaPos[0] += self.deplacement
      if K_z in self.engine.keystrokes :
          self.deltaPos[1] -= self.deplacement
      if K_s in self.engine.keystrokes :
          self.deltaPos[1] += self.deplacement

      if self.deltaPos[0] != 0 or self.deltaPos[1] != 0:
        self.createCircle = True
        self.circlePos = [self.Rect.left, self.Rect.top]
      else : 
        self.createCircle = False

      #Application du mouvement
      self.Rect = pygame.Rect.move(self.Rect, (self.deltaPos[0], self.deltaPos[1]))
        
    #Update
    super().Update()

  def Draw(self, rendu):
    if self.shown :
      return super().Draw(rendu)
    else :
      return 0