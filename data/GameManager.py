import pygame, sys, math, json
from pygame.locals import *
from data import Engine
from data import Player
from data import Graine
from data import Root
from data import Stone
from data import SeveBar
from data import Well

def GenLevel(file, engine):
  with open(file, "r") as content:
    tileList = json.load(content)

  walls = []
  wells = []
  for y in range(len(tileList)):
    for x in range(len(tileList[y])):
      if tileList[y][x] == "Stone":
        walls.append(Stone.Stone("Stone", engine, [x * 16, y * 16]))
      elif tileList[y][x] == "Well":
        wells.append(Well.Well("Well", engine, [x * 16, y * 16]))
  return walls, wells




class Manager():
  def __init__(self, engine):

    self.engine = engine

    self.engine.Init(self)

  def Setup(self):

    self.gameOver = False
    self.gOScreen = pygame.image.load("data/GameOver.png")

    self.gameWon = False
    self.gWScreen = pygame.image.load("data/YouWon.png")

    self.gameStart = True
    self.SplashScreen = pygame.image.load("data/SplashScreen.png")

    self.gui = []

    #On crée un joueur
    joueur = Player.Player("Player", self.engine)

    graine = Graine.Graine("Graine", self.engine)

    file = "data/TestLevel.json"
    self.walls, self.wells = GenLevel(file, self.engine)

    self.gui.append(SeveBar.Seve("Seve", self.engine))

    self.plante = []

    self.mask = pygame.Surface((self.engine.rendu.get_size()))
    pygame.draw.circle(self.mask, (255,255,255), (self.engine.Rlongueur // 2, self.engine.Rlargeur - 24 - 30), 12)

    #enemy = Enemy.Enemy("Zoubida", joueur, self.engine)
    #enemy2 = Enemy.Enemy("zoubida2leretour", joueur, self.engine)

  
  #C'est ici que se trouve la boucle principale
  def Run(self):
    continuer = True
    exitCode = False

    pygame.mixer.music.load("data/GN3.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    while continuer :
      #self.engine.collisions = CollTest(self.walls, self.player)

      if self.player.points <= 0 and self.gameOver == False:
        self.gameOver = True

      self.engine.Update()

      if self.player.createCircle:
        #print(self.player.circlePos)
        self.plante.append(Root.Root("Plant", self.engine, self.player.circlePos))
        pygame.draw.circle(self.mask, (255,255,255), (self.player.circlePos[0] + 2, self.player.circlePos[1] + 2 - 24), 12)

      if pygame.mouse.get_pressed(num_buttons = 3)[0]:
        self.gameStart = False

      #On remplit self.keystrokes une seule fois par frame
      for event in pygame.event.get() :
            if event.type == QUIT or (event.type == KEYDOWN and event.key == pygame.K_ESCAPE):
              pygame.quit()
              continuer = False
            if event.type == KEYDOWN :
              if event.key == pygame.K_r :
                continuer = False
                exitCode = True
              else:
                self.engine.keystrokes.append(event.key)
            if event.type == KEYUP :
              if event.key in self.engine.keystrokes:
                self.engine.keystrokes.remove(event.key)
    return exitCode

  def RelocatePlayer(self):
    possibleLocs = []
    mouse = [pygame.mouse.get_pos()[0]//self.engine.rapport, pygame.mouse.get_pos()[1]//self.engine.rapport]
    for plant in self.plante:
      if plant.Rect.collidepoint(mouse):
        possibleLocs.append(plant)
    if len(possibleLocs) > 0:
      bestLoc = sorted(possibleLocs, key=lambda loc : math.sqrt((loc.Rect.centerx - mouse[0])**2 +
                                                                (loc.Rect.centery - mouse[1])**2))
      return bestLoc[0].Rect.centerx, bestLoc[0].Rect.centery
    else:
      return -69, -69

  def CollTest(self, walls, objet):
    collisions = []
    for wall in walls:
      #print(wall)
      #print(player)
      if wall.Rect.colliderect(objet.Rect):
        collisions.append(wall)
    #print(collisions)
    return collisions