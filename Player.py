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

    self.InitSprite("data/Bourgeon.png")
    self.InitRect([moteur.Rlongueur//2 - 2, moteur.Rlargeur - 32], [4, 4])

    self.layer = 1000

    self.shown = False

    self.createCircle = False
    self.circlePos = [0,0]

    self.points = 150

  def Update(self) :

    self.Sprite = self.SpriteCopy.copy()

    if pygame.mouse.get_pressed(num_buttons = 3)[0] :
      #self.Rect.update((pygame.mouse.get_pos()[0]//self.engine.rapport) - 16, (pygame.mouse.get_pos()[1]//self.engine.rapport) - 16, 16, 16)
      newX, newY = self.engine.manager.RelocatePlayer()
      if newX != -69 and newY != -69:
        self.Rect.update(newX - 2, newY - 2, 4, 4)

    if (self.engine.frame // 10) % 2 == 0:
      self.shown = True
    else:
      self.shown = False
      
    #Mouvements Joueur
    self.deltaPos = [0,0]
    self.deplacement = 3

    if self.Rect.centery < 95:
      self.deplacement = 1

    if self.Rect.top < 24:
      self.engine.manager.gameWon = True

    #Mouvements Latéraux et horizontaux 
    if K_a in self.engine.keystrokes :
        self.deltaPos[0] -= self.deplacement
    if K_d in self.engine.keystrokes :
        self.deltaPos[0] += self.deplacement
    if K_w in self.engine.keystrokes :
        self.deltaPos[1] -= self.deplacement
    if K_s in self.engine.keystrokes :
        self.deltaPos[1] += self.deplacement

    if self.deltaPos[0] != 0 or self.deltaPos[1] != 0:
      self.createCircle = True
      self.circlePos = [self.Rect.left, self.Rect.top]
      self.shown = True
    else:
      self.createCircle = False

    #Application du mouvement
    #self.Rect = pygame.Rect.move(self.Rect, (self.deltaPos[0], self.deltaPos[1]))
    prevPos = self.Rect.topleft
    self.Move(self.deltaPos, self.engine.manager.walls)
    newPos = self.Rect.topleft

    if prevPos[0] != newPos[0] or prevPos[1] != newPos[1]:
      self.points -= 3
      self.engine.manager.gui[0].Redraw(self.points)

    for well in self.engine.manager.wells:
      if self.Rect.colliderect(well.Rect) and well.points > 0:
        well.sucked = True

    #print(self.points)
        
    #Update
    super().Update()

  def Draw(self):
    if self.shown :
      return super().Draw()
    else :
      return 0