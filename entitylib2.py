from random import randint
from time import time, sleep
from multiprocessing import Value, Array, Process
import pygame
pygame.init()
class core:
    __doc__ = """Content all variables used on this library ! Use with caution !
Attributes : 'fen', 'tic', 'timer', 'jauges'"""
    __init__ = None

def init(MobTypes):
    "MobTypes : tuple of all created class\nInitializing all class in tuple"
    for a in MobTypes:
        a.name = a.__name__
        a.img = pygame.transform.scale(pygame.image.load("textures/" + a.name + "."+a.img_format), a.size)

class Player:
    pos = Array("i", 2)

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
        self.pos = pos + (pos[0]+self.size[0], pos[1]+self.size[1])
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
        self.pos = Array("i", pos)
        self.move = Array("i", move)
        self.entities.append(self)
    def clean():
        global Fired
        while a < b:
            if Fired.entities[a].delay == 0:
                del Fired.entities[a]
                del Fired.actives[a]
                b+=-1
            else:
                Fired.entities[a].delay += -1
                Fired.entities[a].pos[0] += Fired.entities[a].move[0] * (Fired.entities[a].speed * (1 - 0.3 * abs(Fired.entities[a].move[1])))
                Fired.entities[a].pos[1] += Fired.entities[a].move[1] * (Fired.entities[a].speed * (1 - 0.3 * abs(Fired.entities[a].move[0])))
                a+=1

class Entity:
    __doc__ = """Utiliser 'class <nom>(Fired):' pour créer une entité.
Entités simples (trajectoire aléatoire)
Attributs de ce type de classe :"""
    def collide(self):
        global Player, IA, IA_D, Static, Obstacle, Entity
        cond = True
        for e in Entity.entities:
            if e.pos[0] + e.size[0] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[1] + e.size[1] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    if e is self:continue
                    # collision
                    self.pos.acquire()
                    if self.move[0] == 1 and self.pos[0] + self.size[0] <= e.pos[0] + self.speed + e.speed:
                        # droite
                        self.pos[0] += -self.speed
                    elif self.move[0] == -1 and e.pos[0] + e.size[0] <= self.pos[0] + self.speed + e.speed:
                        # gauche
                        self.pos[0] += self.speed
                    elif self.move[1] == 1 and self.pos[1] + self.size[1] <= e.pos[1] + self.speed + e.speed:
                        # bas
                        self.pos[1] += -self.speed
                    elif self.move[1] == -1 and e.pos[1] + e.size[1] <= self.pos[1] + self.speed + e.speed:
                        # haut
                        self.pos[1] += self.speed
                    self.pos.release()
        for e in IA.entities:
            if e.pos[0] + e.size[0] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[1] + e.size[1] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    # collision
                    self.pos.acquire()
                    if self.move[0] == 1 and self.pos[0] + self.size[0] <= e.pos[0] + self.speed + e.speed:
                        # droite
                        self.pos[0] += -self.speed
                    elif self.move[0] == -1 and e.pos[0] + e.size[0] <= self.pos[0] + self.speed + e.speed:
                        # gauche
                        self.pos[0] += self.speed
                    elif self.move[1] == 1 and self.pos[1] + self.size[1] <= e.pos[1] + self.speed + e.speed:
                        # bas
                        self.pos[1] += -self.speed
                    elif self.move[1] == -1 and e.pos[1] + e.size[1] <= self.pos[1] + self.speed + e.speed:
                        # haut
                        self.pos[1] += self.speed
                    self.pos.release()
        for e in IA_D.entities:
            if e.pos[0] + e.size[0] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[1] + e.size[1] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    # collision
                    self.pos.acquire()
                    if self.move[0] == 1 and self.pos[0] + self.size[0] <= e.pos[0] + self.speed + e.speed:
                        # droite
                        self.pos[0] += -self.speed
                    elif self.move[0] == -1 and e.pos[0] + e.size[0] <= self.pos[0] + self.speed + e.speed:
                        # gauche
                        self.pos[0] += self.speed
                    elif self.move[1] == 1 and self.pos[1] + self.size[1] <= e.pos[1] + self.speed + e.speed:
                        # bas
                        self.pos[1] += -self.speed
                    elif self.move[1] == -1 and e.pos[1] + e.size[1] <= self.pos[1] + self.speed + e.speed:
                        # haut
                        self.pos[1] += self.speed
                    self.pos.release()
        for e in Obstacle.entities:
            if e.pos[2] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[3] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    # collision
                    self.pos.acquire()
                    if self.move[0] == 1 and self.pos[0] + self.size[0] <= e.pos[0] + self.speed:
                        # droite
                        self.pos[0] = e.pos[0] - self.size[0]
                    elif self.move[0] == -1 and e.pos[2] <= self.pos[0] + self.speed:
                        # gauche
                        self.pos[0] = e.pos[0] + e.size[0]
                    elif self.move[1] == 1 and self.pos[1] + self.size[1] <= e.pos[1] + self.speed:
                        # bas
                        self.pos[1] = e.pos[1] - self.size[1]
                    elif self.move[1] == -1 and e.pos[3] <= self.pos[1] + self.speed:
                        # haut
                        self.pos[1] = e.pos[1] + e.size[1]
                    self.pos.release()
        for e in Static.entities:
            if e.pos[0] + e.size[0] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[1] + e.size[1] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    # collision
                    self.pos.acquire()
                    if self.move[0] == 1 and self.pos[0] + self.size[0] <= e.pos[0] + self.speed:
                        # droite
                        self.pos[0] = e.pos[0] - self.size[0]
                    elif self.move[0] == -1 and e.pos[2] <= self.pos[0] + self.speed:
                        # gauche
                        self.pos[0] = e.pos[0] + e.size[0]
                    elif self.move[1] == 1 and self.pos[1] + self.size[1] <= e.pos[1] + self.speed:
                        # bas
                        self.pos[1] = e.pos[1] - self.size[1]
                    elif self.move[1] == -1 and e.pos[2] <= self.pos[1] + self.speed:
                        # haut
                        self.pos[1] = e.pos[1] + e.size[1]
                    self.pos.release()

class IA:
    __doc__ = """Utiliser 'class <nom>(IA):' pour créer une IA.
Entités intelligentes ! (exemple : monstre)
Attributs de ce type de classe :
target : cible de l'IA (None pour aucune cible)
live : vie de l'entité (100 par défaut)
img_format : format de l'image ('png' par défaut)
dmg : dégats infligés à la cible (5 par défaut)
atk_freq : temps (en tic) entre 2 attaques de l'IA (20 par défaut)
delay : temps de vie (en tic) de l'IA (-1 par défaut)"""
    live=100
    img_format="png"
    dmg=5
    delay = 0
    atk_freq=20
    atk_delay=0
    dir=0
    indirect=0
    entities = []
    actives = []
    def clean():
        global IA
        while a < b:
            if IA.entities[a].delay == 0 or IA.entities[a].live.value <= 0:
                del IA.entities[a]
                del IA.actives[a]
                b+=-1
            else:
                IA.entities[a].delay += -1
                a+=1
    def __init__(self, pos):
        self.pos = Array("f", pos)
        self.live = Value("i", live)
        self.move = Array("i", 2)   # mouvement
        self.dir = Value("i", 0)    # direction
        self.DIR = Value("i", 0)    # direction initiale
        self.atk_delay = Value("i", 0)
        self.indirect = Value("i", 0)
        self.entities.append(self)
        self.actives.append(Process(target=self.react))
        self.actives[-1].start()
    def react(self):
        global Player
        if not self.indirect.value:
            self.move.acquire()
            self.dir.acquire()
            b = abs(self.pos[0] - Player.pos[0]) > abs(self.pos[1] - Player.pos[1])
            if self.pos[0] < Player.pos[0]:
                self.move[0] = 1
                if b:self.dir.value=0
            else:
                self.move[0] = -1
                if b:self.dir.value=2
            if self.pos[1] < Player.pos[1]:
                self.move[1] = 1
                if not b:self.dir.value=1
            else:
                self.move[1] = -1
                if not b:self.dir.value=3
            self.move.release()
            self.dir.release()
        self.pos[0] += self.move[0] * self.speed * (1-abs(self.move[1]) * 0.3)
        self.pos[1] += self.move[1] * self.speed * (1-abs(self.move[0]) * 0.3)
        self.collide()
    def collide(self):
        global Player, IA, IA_D, Static, Obstacle, Entity
        cond = True
        for e in Entity.entities:
            if e.pos[0] + e.size[0] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[1] + e.size[1] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    # collision
                    self.pos.acquire()
                    if self.move[0] == 1 and self.pos[0] + self.size[0] <= e.pos[0] + self.speed + e.speed:
                        # droite
                        self.pos[0] += -self.speed
                    elif self.move[0] == -1 and e.pos[0] + e.size[0] <= self.pos[0] + self.speed + e.speed:
                        # gauche
                        self.pos[0] += self.speed
                    elif self.move[1] == 1 and self.pos[1] + self.size[1] <= e.pos[1] + self.speed + e.speed:
                        # bas
                        self.pos[1] += -self.speed
                    elif self.move[1] == -1 and e.pos[1] + e.size[1] <= self.pos[1] + self.speed + e.speed:
                        # haut
                        self.pos[1] += self.speed
                    self.pos.release()
        for e in IA.entities:
            if e.pos[0] + e.size[0] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[1] + e.size[1] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    if e is self:continue
                    # collision
                    self.pos.acquire()
                    if self.move[0] == 1 and self.pos[0] + self.size[0] <= e.pos[0] + self.speed + e.speed:
                        # droite
                        self.pos[0] += -self.speed
                    elif self.move[0] == -1 and e.pos[0] + e.size[0] <= self.pos[0] + self.speed + e.speed:
                        # gauche
                        self.pos[0] += self.speed
                    elif self.move[1] == 1 and self.pos[1] + self.size[1] <= e.pos[1] + self.speed + e.speed:
                        # bas
                        self.pos[1] += -self.speed
                    elif self.move[1] == -1 and e.pos[1] + e.size[1] <= self.pos[1] + self.speed + e.speed:
                        # haut
                        self.pos[1] += self.speed
                    self.pos.release()
        for e in IA_D.entities:
            if e.pos[0] + e.size[0] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[1] + e.size[1] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    if e is self:continue
                    # collision
                    self.pos.acquire()
                    if self.move[0] == 1 and self.pos[0] + self.size[0] <= e.pos[0] + self.speed + e.speed:
                        # droite
                        self.pos[0] += -self.speed
                    elif self.move[0] == -1 and e.pos[0] + e.size[0] <= self.pos[0] + self.speed + e.speed:
                        # gauche
                        self.pos[0] += self.speed
                    elif self.move[1] == 1 and self.pos[1] + self.size[1] <= e.pos[1] + self.speed + e.speed:
                        # bas
                        self.pos[1] += -self.speed
                    elif self.move[1] == -1 and e.pos[1] + e.size[1] <= self.pos[1] + self.speed + e.speed:
                        # haut
                        self.pos[1] += self.speed
                    self.pos.release()
        for e in Obstacle.entities:
            if e.pos[2] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[3] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    # collision
                    self.pos.acquire()
                    if self.move[0] == 1 and self.pos[0] + self.size[0] <= e.pos[0] + self.speed:
                        # droite
                        self.pos[0] = e.pos[0] - self.size[0]
                        self.pos.release()
                        if self.indirect.value == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir.value == 1:cond = False
                            elif self.dir.value == 0:
                                self.dir.acquire()
                                self.dir.value = 1
                                self.dir.release()
                                self.move.acquire()
                                self.move[1] = 1
                                self.move.release()
                                cond = False
                        elif self.dir.value == 0:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir.acquire()
                            self.dir.value = 1
                            self.dir.release()
                            self.move.acquire()
                            self.move[1] = 1
                            self.move.release()
                            self.indirect.acquire()
                            self.indirect.value = 1
                            self.indirect.release()
                            self.DIR.acquire()
                            self.DIR.value = 0
                            self.DIR.release()
                    elif self.move[0] == -1 and e.pos[2] <= self.pos[0] + self.speed:
                        # gauche
                        self.pos[0] = e.pos[0] + e.size[0]
                        self.pos.release()
                        if self.indirect.value == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir.value == 3:cond = False
                            elif self.dir.value == 2:
                                self.dir.acquire()
                                self.dir.value = 3
                                self.dir.release()
                                self.move.acquire()
                                self.move[1] = -1
                                self.move.release()
                                cond = False
                        elif self.dir.value == 2:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir.acquire()
                            self.dir.value = 3
                            self.dir.release()
                            self.move.acquire()
                            self.move[1] = -1
                            self.move.release()
                            self.indirect.acquire()
                            self.indirect.value = 1
                            self.indirect.release()
                            self.DIR.acquire()
                            self.DIR.value = 2
                            self.DIR.release()
                            
                    elif self.move[1] == 1 and self.pos[1] + self.size[1] <= e.pos[1] + self.speed:
                        # bas
                        self.pos[1] = e.pos[1] - self.size[1]
                        self.pos.release()
                        if self.indirect.value == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir.value == 2:cond = False
                            elif self.dir.value == 1:
                                self.dir.acquire()
                                self.dir.value = 2
                                self.dir.release()
                                self.move.acquire()
                                self.move[0] = -1
                                self.move.release()
                                cond = False
                        elif self.dir.value == 1:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir.acquire()
                            self.dir.value = 2
                            self.dir.release()
                            self.move.acquire()
                            self.move[0] = -1
                            self.move.release()
                            self.indirect.acquire()
                            self.indirect.value = 1
                            self.indirect.release()
                            self.DIR.acquire()
                            self.DIR.value = 1
                            self.DIR.release()
                            
                    elif self.move[1] == -1 and e.pos[3] <= self.pos[1] + self.speed:
                        # haut
                        self.pos[1] = e.pos[1] + e.size[1]
                        self.pos.release()
                        if self.indirect.value == 0:
                            # On est déja en train de contourner un obstacle
                            if self.dir.value == 0:cond = False
                            elif self.dir.value == 3:
                                self.dir.acquire()
                                self.dir.value = 0
                                self.dir.release()
                                self.move.acquire()
                                self.move[0] = 1
                                self.move.release()
                                cond = False
                        elif self.dir.value == 3:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir.acquire()
                            self.dir.value = 0
                            self.dir.release()
                            self.move.acquire()
                            self.move[0] = 1
                            self.move.release()
                            self.indirect.acquire()
                            self.indirect.value = 1
                            self.indirect.release()
                            self.DIR.acquire()
                            self.DIR.value = 3
                            self.DIR.release()

        for e in Static.entities:
            if e.pos[2] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[3] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    # collision
                    self.pos.acquire()
                    if self.move[0] == 1 and self.pos[0] + self.size[0] <= e.pos[0] + self.speed:
                        # droite
                        self.pos[0] = e.pos[0] - self.size[0]
                        self.pos.release()
                        if self.indirect.value == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir.value == 1:cond = False
                            elif self.dir.value == 0:
                                self.dir.acquire()
                                self.dir.value = 1
                                self.dir.release()
                                self.move.acquire()
                                self.move[1] = 1
                                self.move.release()
                                cond = False
                        elif self.dir.value == 0:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir.acquire()
                            self.dir.value = 1
                            self.move.acquire()
                            self.move[1] = 1
                            self.move.release()
                            self.indirect.acquire()
                            self.indirect.value = 1
                            self.indirect.release()
                            self.DIR.acquire()
                            self.DIR.value = 0
                            self.DIR.release()
                    elif self.move[0] == -1 and e.pos[2] <= self.pos[0] + self.speed:
                        # gauche
                        self.pos[0] = e.pos[2]
                        self.pos.release()
                        if self.indirect.value == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir.value == 3:cond = False
                            elif self.dir.value == 2:
                                self.dir.acquire()
                                self.dir.value = 3
                                self.dir.release()
                                self.move.acquire()
                                self.move[1] = -1
                                self.move.release()
                                cond = False
                        elif self.dir.value == 2:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir.acquire()
                            self.dir.value = 3
                            self.dir.release()
                            self.move.acquire()
                            self.move[1] = -1
                            self.move.release()
                            self.indirect.acquire()
                            self.indirect.value = 1
                            self.indirect.release()
                            self.DIR.acquire()
                            self.DIR.value = 2
                            self.DIR.release()
                            
                    elif self.move[1] == 1 and self.pos[1] + self.size[1] <= e.pos[1] + self.speed:
                        # bas
                        self.pos[1] = e.pos[1] - self.size[1]
                        self.pos.release()
                        if self.indirect.value == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir.value == 2:cond = False
                            elif self.dir.value == 1:
                                self.dir.acquire()
                                self.dir.value = 2
                                self.dir.release()
                                self.move.acquire()
                                self.move[0] = -1
                                self.move.release()
                                cond = False
                        elif self.dir.value == 1:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir.acquire()
                            self.dir.value = 2
                            self.dir.release()
                            self.move.acquire()
                            self.move[0] = -1
                            self.move.release()
                            self.indirect.acquire()
                            self.indirect.value = 1
                            self.indirect.release()
                            self.DIR.acquire()
                            self.DIR.value = 1
                            self.DIR.release()
                            
                    elif self.move[1] == -1 and e.pos[3] <= self.pos[1] + self.speed:
                        # haut
                        self.pos[1] = e.pos[3]
                        self.pos.release()
                        if self.indirect.value == 0:
                            # On est déja en train de contourner un obstacle
                            if self.dir.value == 0:cond = False
                            elif self.dir.value == 3:
                                self.dir.acquire()
                                self.dir.value = 0
                                self.dir.release()
                                self.move.acquire()
                                self.move[0] = 1
                                self.move.release()
                                cond = False
                        elif self.dir.value == 3:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir.acquire()
                            self.dir.value = 0
                            self.dir.release()
                            self.move.acquire()
                            self.move[0] = 1
                            self.move.release()
                            self.indirect.acquire()
                            self.indirect.value = 1
                            self.indirect.release()
                            self.DIR.acquire()
                            self.DIR.value = 3
                            self.DIR.release()
        if self.indirect.value == 1 and cond:
            self.dir.acquire()
            self.dir.value = (self.dir.value - 1)%4
            self.dir.release()
            self.move.acquire()
            self.move[self.dir.value%2] = -self.move[self.dir.value%2]
            if self.dir.value == self.DIR.value:
                self.indirect.acquire()
                self.indirect.value = 0
                self.indirect.release()

class IA_D(IA):
    __doc__ = """Utiliser 'class <nom>(IA_D):' pour créer une IA lançant des projectiles sur le joueur.
Entités intelligentes ! (exemple : archer)
Attributs de ce type de classe :
live : vie de l'entité
img_format : format de l'image ('png' par défaut)
atk_delay : temps (en tic) entre 2 attaques de l'IA
weapon : projectile lancé par l'IA"""
    entities = []
    actives = []
    def clean():
        global IA_D
        while a < b:
            if IA_D.entities[a].delay == 0 or IA_D.entities[a].live.value <= 0:
                del IA_D.entities[a]
                del IA_D.actives[a]
                b+=-1
            else:
                IA_D.entities[a].delay += -1
                a+=1

def Refresh():
    global Static, Obstacle, Fired, IA, IA_D, Player, Entity, core
    Obstacle.clean()
    Fired.clean()
    IA.clean()
    IA_D.clean()
    Entity.clean()
    # ----- SCREEN ----- #
    
    # ------------------ #
    Player.pos.acquire()
    Player.pos[0] += Player.move[0] * (Player.speed.value * (1 - 0.3 * abs(Player.move[1])))
    Player.pos[1] += Player.move[1] * (Player.speed.value * (1 - 0.3 * abs(Player.move[0])))
    Player.pos.release()
    for a in Fired.actives:
        a.run()
    for a in IA.actives:
        a.run()
    for a in IA_D.actives:
        a.run()
