#Imports
import pygame
import Engine
from pygame.locals import *

#Class Joueur
class Seve(Engine.Entity) :
    def __init__(self, name, moteur) :
        #Permet d'appeler la fonction __init__() d'Objet
        super().__init__(name, moteur, toDraw=False)

        self.InitSprite("data/SeveFond.png")
        self.fond = pygame.image.load("data/SeveFond.png")
        self.liquide = pygame.image.load("data/SeveLiquide.png")
        self.mask = pygame.image.load("data/SeveMasque.png")
        self.cadre = pygame.image.load("data/SeveCadre.png")

        self.Sprite.blit(self.liquide, (0,0))
        self.Sprite.blit(self.mask, (0,0))
        self.Sprite.set_colorkey((255,0,0))
        self.Sprite.blit(self.cadre, (0,0))


        self.InitRect([moteur.Rlongueur - 16, moteur.Rlargeur//2 - self.Sprite.get_height()//2], [16, 128])
    
    def Redraw(self, points):
        
        displacement = int((150 - points) * 125 / 150)
        
        self.Sprite.fill((0,0,0))
        self.Sprite.blit(self.fond, (0,0))
        self.Sprite.blit(self.liquide, (0,displacement))
        self.Sprite.blit(self.mask, (0,0))
        self.Sprite.set_colorkey((255,0,0))
        self.Sprite.blit(self.cadre, (0,0))
