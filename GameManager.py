import pygame
from pygame.locals import *
import Engine
import Player
import Graine
import Root

class Manager():
  def __init__(self, engine):

    self.engine = engine

    self.engine.Init(self)

    self.transition = False

  def Setup(self):
    #On crée un joueur
    joueur = Player.Player("Player", self.engine)

    graine = Graine.Graine("Graine", self.engine)

    self.plante = []

    #enemy = Enemy.Enemy("Zoubida", joueur, self.engine)
    #enemy2 = Enemy.Enemy("zoubida2leretour", joueur, self.engine)

  
  #C'est ici que se trouve la boucle principale
  def Run(self):
    continuer = True
    while continuer :
      self.engine.Update()

      if self.player.createCircle:
        #print(self.player.circlePos)
        self.plante.append(Root.Root("Plant", self.engine, self.player.circlePos))

      #On remplit self.keystrokes une seule fois par frame
      for event in pygame.event.get() :
            if event.type == QUIT :
              pygame.quit()
              continuer = False
            if event.type == KEYDOWN : 
              if event.key == pygame.K_p :
                self.engine.pause = not self.engine.pause
                
              else : 
                self.engine.keystrokes.append(event.key)
            if event.type == KEYUP :
              if event.key in self.engine.keystrokes:
                self.engine.keystrokes.remove(event.key)