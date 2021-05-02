#Imports
import pygame
from data import Engine
from pygame.locals import *

#Class Joueur
class Well(Engine.Entity) :
    def __init__(self, name, moteur, pos) :
        #Permet d'appeler la fonction __init__() d'Objet
        super().__init__(name, moteur)

        self.points = 75
        self.sucked = False

        self.InitSprite("data/WellFond.png")

        self.fond = pygame.image.load("data/WellFond.png")
        self.cadre = pygame.image.load("data/WellCadre.png")
        self.liquide = pygame.image.load("data/WellWater.png")

        self.Sprite.blit(self.liquide, (0,0))
        self.Sprite.blit(self.cadre, (0,0))

        self.InitRect(pos, [16, 16])

    def Update(self):

        if self.sucked and self.engine.manager.player.points < 150:
            self.points -= 4
            self.engine.manager.player.points += 4
            self.engine.manager.gui[0].Redraw(self.engine.manager.player.points)

            self.Redraw()

            if self.points <= 0:
                self.sucked = False

        super().Update()

    def Redraw(self):

        self.Sprite.fill((0,0,0))

        displacement = int((75 - self.points) * 12 / 75)

        self.Sprite.blit(self.fond, (0,0))
        self.Sprite.blit(self.liquide, (0,displacement))
        self.Sprite.blit(self.cadre, (0,0))