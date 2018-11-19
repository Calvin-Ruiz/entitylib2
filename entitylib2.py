from random import randint
from time import time, sleep
from multiprocessing import Value, Array, Process
import pygame
pygame.init()

def init(MobTypes):
    "tuple of all class"
    for a in MobTypes:
        a.img = pygame.transform.scale(pygame.image.load("textures/" + a.name + "."+a.img_format), a.size)

class Static:
    __doc__ = """Utiliser 'nom = Static(*args)' pour créer un mur.
Renvoie un type d'objet indestructible et immobile.
Tout objet Static ne pourra jamais être traversé, il sera toujours 'solide'.
img_format : format de l'image ('png' par défaut)
size : tuple de la hauteur et de la largeur de l'entité désiré
Utiliser nom.append(pos) pour ajouter une entité"""
    entities = []
    def __init__(self, name, size, img_format="png"):
        global Static
        self.img = pygame.transform.scale(pygame.image.load("textures/"+name + "."+img_format), size)
        self.size = size
    def append(self, pos):
        "pos : position du mur (exemple : (367, -23) )"
        self.entities.append((self.img, pos, (pos[0]+self.size[0], pos[1]+self.size[1]) ))

class Obstacle:
    __doc__ = """Utiliser 'class <nom>(Obstacle):' pour créer un obstacle.
Attributs de ce type de classe :
live : points de vie de l'obstacle
img_format : format de l'image ('png' par défaut)
size : tuple de la hauteur et de la largeur de l'entité désiré
Ce type d'objet est statique mais destructible."""
    entities = []
    def __init__(self, pos):
        self.pos = pos
        self.entities.append(self)
    img_format="png"
    def clean():
        global Obstacle
        while a < b:
            if obs.entities[a].live.value <= 0:
                del obs.entities[a]
                b+=-1
            else:a+=1

def Rien():pass

class Fired:
    __doc__ = """Utiliser 'class <nom>(Fired):' pour créer un projectile.
Entités mobiles (exemple : flèche)
Attributs de ce type de classe :
speed : vitesse de déplacement (0 par défaut)
pcoll : activer la collision avec le joueur (True par défaut)
ecoll : activer la collision avec les entités (True par défaut)
action : action supplémentaire quand contact avec le joueur (def Rien():pass par défaut)
dmg : dégâts infligés à l'objet touché (0 par défaut)
delay : durée de vie du projectile (en tic) (-1 par défaut)
img_format : format de l'image ('png' par défaut)
Ce type d'entité se détruit au contact en infligeant des dégats"""
    entities = []
    actives = []
    speed = 0
    pcoll = True
    ecoll = True
    action = Rien
    dmg = 0
    delay = -1
    img_format = "png"
    def __init__(self, pos, move):
        """pos : position du projectile (exemple : (367, -23) )
move : mouvement du projectile en x et en y.
1 : mouvement positif, 0 : immobile et -1 : mouvement négatif
(exemple : (-1, 1) )"""
        self.pos = pos
        self.move = move
        self.entities.append(self)
    def clean():
        global Fired
        while a < b:
            if Fired.entities[a].delay.value == 0:
                del Fired.entities[a]
                del Fired.actives[a]
                b+=-1
            else:
                Fired.entities[a].delay.acquire()
                Fired.entities[a].delay.value += -1
                Fired.entities[a].delay.release()
                movement
                a+=1

class IA:
    __doc__ = """Utiliser 'class <nom>(IA):' pour créer une IA.
Entités intelligentes ! (exemple : monstre)
Attributs de ce type de classe :
target : cible de l'IA (None pour aucune cible)
live : vie de l'entité (100 par défaut)
img_format : format de l'image ('png' par défaut)
dmg : dégats infligés à la cible (5 par défaut)
atk_delay : temps (en tic) entre 2 attaques de l'IA (20 par défaut)
"""
    live=100
    img_format="png"
    dmg=5
    atk_delay=20
    def clean():
        global IA
        while a < b:
            if IA.entities[a].delay.value == 0 or IA.entities[a].live.value <= 0:
                del IA.entities[a]
                del IA.actives[a]
                b+=-1
            else:
                IA.entities[a].delay.acquire()
                IA.entities[a].delay.value += -1
                IA.entities[a].delay.release()
                a+=1

class IA_D(IA):
    __doc__ = """Utiliser 'class <nom>(IA_D):' pour créer une IA lançant des projectiles sur le joueur.
Entités intelligentes ! (exemple : archer)
Attributs de ce type de classe :
live : vie de l'entité
img_format : format de l'image ('png' par défaut)
atk_delay : temps (en tic) entre 2 attaques de l'IA
weapon : projectile lancé par l'IA
"""
    def clean():
        global IA_D
        while a < b:
            if IA_D.entities[a].delay.value == 0 or IA_D.entities[a].live.value <= 0:
                del IA_D.entities[a]
                del IA_D.actives[a]
                b+=-1
            else:
                IA_D.entities[a].delay.acquire()
                IA_D.entities[a].delay.value += -1
                IA_D.entities[a].delay.release()
                a+=1
    

def Refresh():
    global Static, Obstacle, Fired, IA, IA_D
    Obstacle.clean()
    Fired.clean()
    IA.clean()
    IA_D.clean()
    for a in Fired.actives:
        a.run()
    for a in IA.actives:
        a.run()
    for a in IA_D.actives:
        a.run()

if __name__ == "__main__":
    import py_compile
    py_compile.compile("entity lib 2.py", "entitylib2.py", optimize=2)
    print("Librairie compilée.")
