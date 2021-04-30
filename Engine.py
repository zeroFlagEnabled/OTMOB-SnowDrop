#Imports
import pygame
from pygame.locals import *

def FirstElementFunc(ls):
  return ls[0]

#Un entity est l'élément fondamental du moteur : un joueur, ennemi, environnement, etc.
class Entity()  :
  def __init__(self, name, engine, bounded = True)  :
    self.name = name
    self.engine = engine

    #Permet de savoir si l'entity peut sortir de l'écran
    self.bounded = bounded

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

  def Draw(self, rendu) :
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
    
      for collision in self.engine.collisions :
        if self in collision :
          collider = collision[(collision.index(self) + 1) % 2]
          if "Wall" == collider.__class__.__name__ :
            if "Wall" != self.__class__.__name__ :
              
              collisionTolerance = 7
              deltaPos = [0,0]
              try : 
                rect1 = self.collideRect
              except AttributeError : 
                rect1 = self.Rect
              try : 
                rect2 = collider.collideRect
              except AttributeError : 
                rect2 = collider.Rect

              if abs(rect1.top - rect2.bottom) < collisionTolerance:
                deltaPos[1] += abs(rect1.top - rect2.bottom)
              if abs(rect1.bottom - rect2.top) < collisionTolerance:
                deltaPos[1] -= abs(rect1.bottom - rect2.top)
              if abs(rect1.left - rect2.right) < collisionTolerance:
                deltaPos[0] += abs(rect1.left - rect2.right)
              if abs(rect1.right - rect2.left) < collisionTolerance:
                deltaPos[0] -= abs(rect1.right - rect2.left)

              try :
                self.collideRect = self.collideRect.move(tuple(deltaPos))
              except AttributeError : pass
              try :
                self.pos[0] += deltaPos[0]
                self.pos[1] += deltaPos[1]
              except AttributeError : pass
              self.Rect = self.Rect.move(tuple(deltaPos))       

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
      result = entity.Draw(rendu)
      if result != 0:
        surfaces.append(result)
    
    surfacesSorted = sorted(surfaces, key=lambda surface : surface[1].bottomleft[1])
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
  def __init__(self, longueur, largeur) :
    self.longueur = longueur
    self.largeur = largeur

    self.player = 0

    #Vu qu'on a un système de rendu intermédaire (adapté à la taille des sprites)
    #On définit les caractéristiques de ce rendu
    self.rapport = 4
    self.Rlongueur = self.longueur//self.rapport
    self.Rlargeur = self.largeur//self.rapport
    
    self.frame = 0
    self.pause = False

  def Init(self, manager) :

    self.manager = manager

    pygame.init()
    
    self.fenetre = pygame.display.set_mode((self.longueur, self.largeur))
    self.rendu = pygame.Surface((self.Rlongueur, self.Rlargeur))

    #On remplace le curseur par le viseur, on prépare le curseur pour les menus
    pygame.mouse.set_visible(False)
    self.cursor = pygame.image.load("Assets/Cursor.png").convert_alpha()
    
    self.scene = Scene(self)

    self.clock = pygame.time.Clock()

    #Cette liste contient toutes les touches appuyées lors d'une frame
    #Elle permet à tout les entitys subordonnés d'accéder à l'input de l'utilisateur
    self.keystrokes = []

    self.collisions = []

  def Update(self) :

    #On commence par tout recouvrir d'un écran de couleur unie
    self.rendu.fill((39,39,68))
      
    self.scene.Update()

    self.scene.Draw(self.rendu)
    
    self.rendu.blit(self.cursor, (pygame.mouse.get_pos()[0]//self.rapport - self.cursor.get_width()//2, pygame.mouse.get_pos()[1]//self.rapport - self.cursor.get_height()//2))

    #Le passage du rendu intérmédiare à la fenêtre finale
    surface = pygame.transform.scale(self.rendu, (self.longueur, self.largeur))
    self.fenetre.blit(surface, (0,0))

    self.frame += 1
    pygame.display.flip()