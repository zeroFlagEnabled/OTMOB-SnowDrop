#Imports
import pygame
from pygame.locals import *

def FirstElementFunc(ls):
  return ls[0]

#Un entity est l'élément fondamental du moteur : un joueur, ennemi, environnement, etc.
class Entity()  :
  def __init__(self, name, engine, bounded = True, toDraw = True)  :
    self.name = name
    self.engine = engine

    #Permet de savoir si l'entity peut sortir de l'écran
    self.bounded = bounded
    self.toDraw = toDraw

    self.hasRect = False
    self.hasSprite = False

    self.renderPriorities = []

    #Permet de garder toutes les entitys dans la liste scene.contenu
    self.engine.scene.contenu.append(self)

  def InitRect(self, pos, size)  :
    self.Rect = pygame.Rect(tuple(pos), tuple(size))

    self.PreviousRects = [0,0]
    self.deltaPos = [0,0]
    
    self.hasRect = True
  
  def InitSprite(self, image) :
    self.Sprite = pygame.image.load(image)
    #On fournit directement une copie du Sprite pour garder un original après les transformations
    self.SpriteCopy = self.Sprite.copy()

    #Dès qu'un Sprite est attribué, la possibilté d'une animation est envisagée
    self.AnimList = {}
    self.playingAnim = False
    self.playedAnim = 0

    self.hasSprite = True

    self.layer = 0

  def AddAnim(self, name, ImageList):
    if self.hasSprite:
      
      #On charge chaque frame de l'animation
      frameList = []
      for image in ImageList:
        frameList.append([pygame.image.load(image[0]), image[1]])

      #Stocke toutes les animations sous forme d'un dictionnaire
      #"nom de l'anim" : [[Frame1, duréeFrame1], [Frame2, durée,Frame2]...]
      self.AnimList[name] = frameList

  def StartAnim(self, name):
    #On vérifie si l'animation existe
    if name in self.AnimList:
      self.playingAnim = True
      self.playedAnim = name
      #La frame que l'animation est actuellement en train de jouer
      self.AnimFrame = 1
      #On détermine la longeur totale de l'animation
      AnimLength = 0
      for frame in self.AnimList[name]:
        AnimLength += frame[1]
      self.AnimLength = AnimLength

    else :
      print("Cette animation n'a pas été attribuée à cette entité")

  def PlayAnim(self):
    if self.AnimFrame <= self.AnimLength:
      AnimFrame = self.AnimFrame
      AnimNotFound = True
      AnimList = self.AnimList[self.playedAnim].copy()
      #On détermine dans quelle étape de l'animation on se trouve
      while AnimNotFound:
        if AnimFrame > AnimList[0][1] :
          AnimFrame -= AnimList[0][1]
          AnimList.pop(0)
        else :
          AnimNotFound = False
          AnimToPlay = AnimList[0][0]
    else:
      #Pour l'instant, l'animation est jouée en boucle
      self.AnimFrame = 1
      AnimToPlay = self.AnimList[self.playedAnim][0][0]
    
    self.AnimFrame += 1
    return AnimToPlay

  def Draw(self) :
    if self.hasRect and self.hasSprite :
      #Si on joue une animation, on va déterminer quelle frame de l'animation
      if self.playingAnim:
        return [self.PlayAnim(), self.Rect, self]
      else:
        return [self.Sprite, self.Rect, self]
    
  def Update(self) :
    #Protocole par défaut d'un entity bounded
    #On s'assure qu'il ne sorte pas de l'écran
    if self.bounded:
      if self.hasRect:
        if self.Rect.topleft[0] < 0:
          self.Rect = pygame.Rect.move(self.Rect, (-self.Rect.topleft[0], 0))
        if self.Rect.topright[0] > self.engine.Rlongueur:
          self.Rect = pygame.Rect.move(self.Rect, ( self.engine.Rlongueur - self.Rect.topright[0], 0))
        if self.Rect.topleft[1] < 0:
          self.Rect = pygame.Rect.move(self.Rect, (0, -self.Rect.topleft[1]))
        if self.Rect.bottomleft[1] > self.engine.Rlargeur:
          self.Rect = pygame.Rect.move(self.Rect, (0, self.engine.Rlargeur-self.Rect.bottomleft[1]))
    
  def Move(self, deltaPos, tiles):
    self.Rect.x += deltaPos[0]

    walls = self.engine.manager.CollTest(tiles, self)

    for wall in walls:
      if deltaPos[0] > 0:
        self.Rect.right = wall.Rect.left
      if deltaPos[0] < 0:
        self.Rect.left = wall.Rect.right
    
    self.Rect.y += deltaPos[1]

    walls = self.engine.manager.CollTest(tiles, self)

    for wall in walls:
      if deltaPos[1] > 0:
        self.Rect.bottom = wall.Rect.top
      if deltaPos[1] < 0:
        self.Rect.top = wall.Rect.bottom

#La scène est l'élément intermédiaire du moteur, elle permet de garder une trace de chaque entity qui s'y trouve
class Scene() :
  def __init__(self, moteur) :
    #La fameuse liste avec tout les entitys
    self.contenu = []

    self.moteur = moteur

    #On charge une salle à partir d'un fichier json fourni
    #self.level = [[0] * 16 for i in range(12)]
    #niveau = Salles.ChargerSalle("niveauTest.json", self.moteur)
    #self.levelSurf = Salles.RenderSalle(niveau, self.moteur)

  def Draw(self, rendu)  :

    #On affiche le sol de la salle
    #rendu.blit(self.levelSurf, (0,0))

    surfaces = []

    for entity in self.contenu :
      if entity.toDraw:
        result = entity.Draw()
        if result != 0:
          surfaces.append(result)
    
    surfacesSorted = sorted(surfaces, key=lambda surface : surface[2].layer)
    #print(surfacesSorted)

    for index, surface in enumerate(surfacesSorted):
      """
      if surface[2].renderPriorities != []:
        priorite = surface[2].renderPriorities
        cible = priorite[0]
        del surfacesSorted[index]
        cibleIndex = 0
        for i in range(len(surfacesSorted)):
          if surfacesSorted[i][2] == cible:
            cibleIndex = i
        #print(surface, cibleIndex, priorite[1])
        surfacesSorted.insert(cibleIndex + priorite[1], surface)
      """
      rendu.blit(surface[0], surface[1])

  def Update(self) :
    for entity in self.contenu :
      entity.Update()


#L'élément le plus grand du système, il englobe le tout
class Moteur() :
  def __init__(self) :
    #self.longueur = longueur
    #self.largeur = largeur

    pygame.init()

    self.largeur = pygame.display.Info().current_h
    self.longueur = pygame.display.Info().current_w

    self.player = 0

    #Vu qu'on a un système de rendu intermédaire (adapté à la taille des sprites)
    #On définit les caractéristiques de ce rendu
    #self.rapport = 4
    #self.Rlongueur = self.longueur//self.rapport
    #elf.Rlargeur = self.largeur//self.rapport

    self.Rlongueur = 256
    self.Rlargeur = 192
    self.rapport = max(self.largeur/self.Rlargeur, self.largeur/self.Rlongueur)
    #print(self.rapport)
    
    self.frame = 0
    self.pause = False

  def Init(self, manager) :

    self.manager = manager

    #pygame.init()
    
    self.fenetre = pygame.display.set_mode((self.longueur, self.largeur), pygame.FULLSCREEN)
    self.rendu = pygame.Surface((self.Rlongueur, self.Rlargeur))

    self.bg = pygame.Surface((self.rendu.get_size()))
    self.bg.fill((255,0,0))
    self.Tempsurface = pygame.Surface((self.rendu.get_size()))

    self.bgImage = pygame.image.load("data/DirtBG.png")

    #On remplace le curseur par le viseur, on prépare le curseur pour les menus
    pygame.mouse.set_visible(False)
    self.cursor = pygame.image.load("data/Cursor.png").convert_alpha()
    
    self.scene = Scene(self)

    self.clock = pygame.time.Clock()

    #Cette liste contient toutes les touches appuyées lors d'une frame
    #Elle permet à tout les entitys subordonnés d'accéder à l'input de l'utilisateur
    self.keystrokes = []

    self.collisions = []

  def Update(self) :

    #On commence par tout recouvrir d'un écran de couleur unie
    self.fenetre.fill((0,0,0))
    self.rendu.fill((139,69,19))
    self.rendu.blit(self.bgImage, (0,0))
    #self.rendu.set_colorkey((39,39,68))
      
    if (not self.manager.gameOver) and (not self.manager.gameWon) and (not self.manager.gameStart):
      self.scene.Update()

    self.scene.Draw(self.rendu)
    
    self.Tempsurface.fill((0,0,0))
    #self.Tempsurface.blit(self.bg, (0,0))
    self.Tempsurface.blit(self.rendu, (0,0))
    self.rendu.fill((39,39,68))
    self.Tempsurface.blit(self.manager.mask, (0,25), special_flags=pygame.BLEND_MULT)
    self.Tempsurface.set_colorkey((0,0,0))

    self.rendu.blit(self.Tempsurface, (0,0))

    for guiElement in self.manager.gui:
      render = guiElement.Draw()
      self.rendu.blit(render[0], render[1])

    if self.manager.gameOver:
      self.rendu.blit(self.manager.gOScreen, (0,0))
    if self.manager.gameWon:
      self.rendu.blit(self.manager.gWScreen, (0,0))
    if self.manager.gameStart:
      self.rendu.blit(self.manager.SplashScreen, (0,0))

    self.rendu.blit(self.cursor, (pygame.mouse.get_pos()[0]//self.rapport, pygame.mouse.get_pos()[1]//self.rapport))

    #Le passage du rendu intérmédiare à la fenêtre finale
    #print(int(self.Rlargeur* self.rapport))
    surface = pygame.transform.scale(self.rendu, (int(self.Rlongueur * self.rapport), int(self.Rlargeur * self.rapport)))
    self.fenetre.blit(surface, ((self.longueur - surface.get_width())//2,(self.largeur - surface.get_height())//2))

    self.frame += 1
    pygame.display.flip()
    self.clock.tick(60)