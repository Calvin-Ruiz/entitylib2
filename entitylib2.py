from random import randint
from time import time, sleep
from multiprocessing import Value, Array, Process
try:
    import pygame
    from os import listdir
except:
    import os
    print("ImportError : Pygame wasn't installed !")
    print("Should I install pygame right now ?")
    if input().upper() in ["OUI", "O", "YE", "YES", "INSTALL", "INSTALLER", "TRUE", "1", "CMD", "PIP", "OK"]:
        print("Python folder detected in '"+os.__file__[0:-10]+"'")
        file = open("supprime_moi.bat", "w")
        file.write("cd /d "+os.__file__[0:-10]+"""
python -m pip install --upgrade pip
python -m pip install pygame""")
        file.close()
        os.startfile("supprime_moi.bat")
        input("Please, relaunch it after complete installation of pygame.")

pygame.init()
print("Warning : Refresh doesn't work with latest python version. (work with 3.5.2)")
print("If Refresh doesn't work with your python version, use SRefresh instead")
print("Released on https://github.com/Calvin-Ruiz/entitylib2")

class BaseEntity:
    def apply(self, effect, delay, level):
        self.effect.append(effect(delay, level))
        self.effect[-1].init_effect(self)
    def apply_all(self, liste):
        for a in liste:
            self.effect.append(a[0](a[1], a[2]))
            self.effect[-1].init_effect(self)

def write(text):
    global letters
    # créer une image
    b = text.split("\n")
    s = pygame.Surface((len(max(b))*8, len(b)*12), pygame.SRCALPHA, 32).convert_alpha()
    x=0
    y=0
    for a in text:
        if a == "\n":
            x = 0
            y += 12
        elif a == " ":
            x+=8
        elif a == "	":
            x = x//64*64+64
        else:
            s.blit(letters[a], (x, y))
            x+=8
    return s

def to_str(number, force_size=True, symbol = {0:"", 1:"k", 2:"M", 3:"G", 4:"T"}):
    exposant = 0
    lenght = 5
    while number >= 10000:
        number = number//1000
        exposant += 1
        lenght = 4
    number = str(number)
    if len(number) > lenght:
        number = number[0:lenght]
    elif force_size:
        number=" "*(lenght-len(number))+number
    # longueur de 40 pixels max !
    return number+symbol[exposant]

def fullscreen():
    global core
    if core.fmode:
        pygame.display.set_mode(core.size)
    else:pygame.display.set_mode(core.size, pygame.FULLSCREEN)
    core.fmode = not core.fmode

class core:
    __doc__ = "Content all variables used on this library. Use with caution !"
    __init__ = None
    score=0
    fmode = False
    size = None
    fen = None
    tic=0 # reset when tic == 360
    timer=0 # nombre de 0,3 minutes écoulées depuis le début de la partie (si aucun lags)
    timexe = time()
    lags = -1
    images = []
    jauges = []
    def refresh():pass
    try:
        img = pygame.image.load("textures/background.bmp")
    except:
        img = pygame.image.load("textures/default.bmp")
    Bsize=img.get_size()
    Bnum=None

letters=dict()

def init(MobTypes, fen_size=(1536, 1024)):
    "MobTypes : tuple of all created class\nInitializing all class in tuple"
    global core, Fired, Player, letters
    print("Initialisation...")
    core.size=fen_size
    core.fen = pygame.display.set_mode(fen_size)
    core.Bnum = (core.size[0]//core.Bsize[0]+2, core.size[1]//core.Bsize[1]+2)
    files = listdir("textures")
    for a in MobTypes + (Player,):
        a.name = a.__name__
        if a.sound != None:a.sounded=True;a.sound=pygame.mixer.Sound("sounds/"+a.sound)
        if type(a.img_format) is str:
            if a.name + "." + a.img_format in files:
                a.img = pygame.transform.scale(pygame.image.load("textures/" + a.name + "."+a.img_format), a.size)
            else:
                a.img = pygame.transform.scale(pygame.image.load("textures/default.bmp"), a.size)
            continue
        try:
            imgs = pygame.image.load("textures/" + a.name + "."+a.img_format[-1])
        except:
            imgs = pygame.image.load("textures/default.bmp")
        a.img = list()
        b=0
        size = imgs.get_size()
        if len(a.img_format) == 3:
            size = (size[0]//img_format[0], size[1]//img_format[1])
            while b < a.img_format[1]:
                c=0
                a.img.append(list())
                while c < a.img_format[0]:
                    c+=1
                    img=pygame.Surface(size, pygame.SRCALPHA, 32).convert_alpha()
                    img.blit(imgs, (size[0]*c, size[1]*b))
                    a.img[b].append(pygame.transform.scale(img, size))
                b+=1
        elif a.__class__ is Fired:
            c=0
            while c < a.img_format[0]:
                img=pygame.Surface(size, pygame.SRCALPHA, 32).convert_alpha()
                img.blit(imgs, (-size[0]*c, 0))
                a.img.append(pygame.transform.scale(img, a.size))
                c+=1
        else:
            size = (size[0]//a.img_format[0], size[1])
            while b < 4:
                c=0
                a.img.append(list())
                while c < a.img_format[0]:
                    img=pygame.Surface(size, pygame.SRCALPHA, 32).convert_alpha()
                    img.blit(imgs, (-size[0]*c, 0))
                    a.img[b].append(pygame.transform.scale(pygame.transform.rotate(img, b*90), a.size))
                    c+=1
                b+=1
    for image in listdir("textures/letter"):
        letters.__setitem__(image[0:-4], pygame.image.load("textures/letter/"+image))
    for image in listdir("textures/letters"):
        letters.__setitem__(image[0:-4], pygame.image.load("textures/letters/"+image))
    print("Librairie et entités initialisées")

def NoWeapon(a, b):pass

class player(BaseEntity):
    __doc__="""Contiend tout ce qui est en rapport avec le joueur.
Utiliser Player.effect.append(effect) pour ajouter un effet au joueur
Utiliser MyEffect = effect(*args) pour créer un nouvel effet."""
    __name__="Player"
    def __init__(self):
        global Player
        self.effect=list()
        self.pos = Array("f", self.pos, lock=False)
        self.live = Value("i", self.live)
        self.atk_delay = Value("i", 0, lock=False)
        self.speed = Value("f", self.speed, lock=False)
        self.react = Process(target=self.collide)
        self.react.start()
    pos = [0, 0]
    move = [0, 0]
    size = (32, 32)
    live = 100
    dir = 0
    img = None
    atk_delay = 0
    atk_freq = 0
    weapon = NoWeapon
    img_format=(1, "png")
    frame = 0
    speed = 3
    react = None
    sound = None
    sounded=False
    effects = []
    def collide(self):
        global IA, IA_D, Static, Obstacle, Entity
        cond = False
        for e in Entity.entities:
            if e.pos[0] + e.size[0] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[1] + e.size[1] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    if e is self:continue
                    # collision
                    coll=True
                    if self.move[0] == 1 and self.pos[0] + self.size[0] <= e.pos[0] + self.speed.value + e.speed:
                        # droite
                        self.pos[0] += -self.speed.value
                    elif self.move[0] == -1 and e.pos[0] + e.size[0] <= self.pos[0] + self.speed.value + e.speed:
                        # gauche
                        self.pos[0] += self.speed.value
                    elif self.move[1] == 1 and self.pos[1] + self.size[1] <= e.pos[1] + self.speed.value + e.speed:
                        # bas
                        self.pos[1] += -self.speed.value
                    elif self.move[1] == -1 and e.pos[1] + e.size[1] <= self.pos[1] + self.speed.value + e.speed:
                        # haut
                        self.pos[1] += self.speed.value
        for e in IA.entities:
            if e.pos[0] + e.size[0] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[1] + e.size[1] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    # collision
                    coll=True
                    if self.move[0] == 1 and self.pos[0] + self.size[0] <= e.pos[0] + self.speed.value + e.speed:
                        # droite
                        self.pos[0] += -self.speed.value
                    elif self.move[0] == -1 and e.pos[0] + e.size[0] <= self.pos[0] + self.speed.value + e.speed:
                        # gauche
                        self.pos[0] += self.speed.value
                    elif self.move[1] == 1 and self.pos[1] + self.size[1] <= e.pos[1] + self.speed.value + e.speed:
                        # bas
                        self.pos[1] += -self.speed.value
                    elif self.move[1] == -1 and e.pos[1] + e.size[1] <= self.pos[1] + self.speed.value + e.speed:
                        # haut
                        self.pos[1] += self.speed.value
        for e in IA_D.entities:
            if e.pos[0] + e.size[0] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[1] + e.size[1] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    # collision
                    coll=True
                    if self.move[0] == 1 and self.pos[0] + self.size[0] <= e.pos[0] + self.speed.value + e.speed:
                        # droite
                        self.pos[0] += -self.speed.value
                    elif self.move[0] == -1 and e.pos[0] + e.size[0] <= self.pos[0] + self.speed.value + e.speed:
                        # gauche
                        self.pos[0] += self.speed.value
                    elif self.move[1] == 1 and self.pos[1] + self.size[1] <= e.pos[1] + self.speed.value + e.speed:
                        # bas
                        self.pos[1] += -self.speed.value
                    elif self.move[1] == -1 and e.pos[1] + e.size[1] <= self.pos[1] + self.speed.value + e.speed:
                        # haut
                        self.pos[1] += self.speed.value
        for e in Obstacle.entities:
            if e.pos[2] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[3] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    # collision
                    coll=True
                    if self.move[0] == 1 and self.pos[0] + self.size[0] <= e.pos[0] + self.speed.value:
                        # droite
                        self.pos[0] = e.pos[0] - self.size[0]
                    elif self.move[0] == -1 and e.pos[2] <= self.pos[0] + self.speed.value:
                        # gauche
                        self.pos[0] = e.pos[0] + e.size[0]
                    elif self.move[1] == 1 and self.pos[1] + self.size[1] <= e.pos[1] + self.speed.value:
                        # bas
                        self.pos[1] = e.pos[1] - self.size[1]
                    elif self.move[1] == -1 and e.pos[3] <= self.pos[1] + self.speed.value:
                        # haut
                        self.pos[1] = e.pos[1] + e.size[1]
        for e in Static.entities:
            if e[2][0] > self.pos[0] and self.pos[0] + self.size[0] > e[1][0]:
                if e[2][1] > self.pos[1] and self.pos[1] + self.size[1] > e[1][1]:
                    # collision
                    coll=True
                    if self.move[0] == 1 and self.pos[0] + self.size[0] <= e[1][0] + self.speed.value:
                        # droite
                        self.pos[0] = e[1][0] - self.size[0]
                    elif self.move[0] == -1 and e[2][0] <= self.pos[0] + self.speed.value:
                        # gauche
                        self.pos[0] = e[2][0]
                    elif self.move[1] == 1 and self.pos[1] + self.size[1] <= e[1][1] + self.speed.value:
                        # bas
                        self.pos[1] = e[1][1] - self.size[1]
                    elif self.move[1] == -1 and e[2][1] <= self.pos[1] + self.speed.value:
                        # haut
                        self.pos[1] = e[2][1]
        if self.atk_delay.value > 0:
            self.atk_delay.value+=-1

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
        self.live = Value("i", self.live)
        self.entities.append(self)
    img_format="png"
    img=None
    sounded = False
    sound = None
    def clean():
        global Obstacle
        a=0;b=len(Obstacle.entities)
        while a < b:
            if Obstacle.entities[a].live.value <= 0:
                del Obstacle.entities[a]
                b+=-1
            else:a+=1

def Rien(self):pass
conversion = {(1, 0) : 0,(1, 1) : 45,(0, 1) : 90,(-1, 1) : 135,(-1, 0) : 180,(-1, -1): 225,(0, -1) : 270,(1, -1) : 315}

class Fired:
    __doc__ = """Utiliser 'class <nom>(Fired):' pour créer un projectile.
Entités mobiles (exemple : flèche)
Attributs de ce type de classe :
speed : vitesse de déplacement (0 par défaut)
pcoll : activer la collision avec le joueur (True par défaut)
ecoll : activer la collision avec les entités (True par défaut)
action : action supplémentaire quand contact avec le joueur (renvoie le projectile comme argument)
--> action agit uniquement sur des 'Value' ou 'Array'. Exemple :
a = Value("i", 0) # créé un Value qui contient 'i' pour un int et 'f' pour un float
a.value --> valeur de a
b = Array("i", longueur) # créé une liste contenant UNIQUEMENT des int ou des float ('i' pour int et 'f' pour float)
b[2] --> valeur en position 2 dans b
dmg : dégâts infligés à l'objet/entité touché (0 par défaut)
delay : durée de vie du projectile (en tic) (-1 par défaut)
img_format : format du "tableau d'image" ((1, 'png') par défaut)
effects : effets appliqués à l'entité touché.
effects = ((effet1, temps, niveau), etc...)
Peut être sous la forme (nbr_frames, nbr_directions, format)
Ou avec une rotation automatique si sous la forme (nbr_frames, format)
Ce type d'entité se détruit au contact en infligeant des dégats"""
    entities = []
    actives = []
    speed = 0
    pcoll = True
    ecoll = False
    action = Rien
    sounded = False
    sound = None
    frame = 0
    dmg = 0
    delay = -1
    effects = tuple()
    img_format = (1, "png")
    img=None
    def __init__(self, pos, move):
        """pos : position du projectile (exemple : (367, -23) )
move : mouvement du projectile en x et en y.
1 : mouvement positif, 0 : immobile et -1 : mouvement négatif
(exemple : (-1, 1) )"""
        global conversion
        self.frame = randint(1-self.img_format[0], 0)
        self.pos = Array("f", pos, lock=False)
        self.move = Array("i", move, lock=False)
        self.delay = Array("i", self.delay, lock=False)
        for a in self.img:
            a = pygame.transform.rotate(a, conversion[tuple(move)])
        self.entities.append(self)
        self.actives.append(Process(target=self.react))
        self.actives[-1].start()

    def clean():
        global Fired
        a=0;b=len(Fired.entities)
        while a < b:
            if Fired.entities[a].delay.value == 0:
                if Fired.entities[a].sounded:Fired.entities[a].sound.play()
                del Fired.entities[a]
                del Fired.actives[a]
                b+=-1
            else:
                Fired.entities[a].delay.value += -1
                Fired.entities[a].pos[0] += Fired.entities[a].move[0] * (Fired.entities[a].speed * (1 - 0.3 * abs(Fired.entities[a].move[1])))
                Fired.entities[a].pos[1] += Fired.entities[a].move[1] * (Fired.entities[a].speed * (1 - 0.3 * abs(Fired.entities[a].move[0])))
                a+=1
    def react(self):
        global Entity, IA, IA_D, Obstacle, Static
        if self.pcoll and Player.pos[0] + Player.size[0] > self.pos[0] and self.pos[0] + self.size[0] > Player.pos[0]:
            if Player.pos[1] + Player.size[1] > self.pos[1] and self.pos[1] + self.size[1] > Player.pos[1]:
                # collision
                Player.live.acquire()
                self.action()
                self.delay.value = 0
                Player.live.value += -self.dmg
                Player.live.release()
                e.apply_all(self.give_effect)
                if Player.sounded:Player.sound.play()
        if self.ecoll:
            for e in Entity.entities:
                if e.pos[0] + e.size[0] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                    if e.pos[1] + e.size[1] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                        # collision
                        self.delay.value = 0
                        e.live.acquire()
                        e.live.value += -self.dmg
                        e.live.release()
                        e.apply_all(self.give_effect)
                        if e.sounded:e.sound.play()
            for e in IA.entities:
                if e.pos[0] + e.size[0] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                    if e.pos[1] + e.size[1] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                        # collision
                        self.delay.value = 0
                        e.live.acquire()
                        e.live.value += -self.dmg
                        e.live.release()
                        e.apply_all(self.give_effect)
                        if e.sounded:e.sound.play()
            for e in IA_D.entities:
                if e.pos[0] + e.size[0] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                    if e.pos[1] + e.size[1] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                        # collision
                        self.delay.value = 0
                        e.live.acquire()
                        e.live.value += -self.dmg
                        e.live.release()
                        e.apply_all(self.give_effect)
                        if e.sounded:e.sound.play()
        for e in Obstacle.entities:
            if e.pos[2] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[3] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    # collision
                    self.delay.value = 0
                    if e.sounded:e.sound.play()
        for e in Static.entities:
            if e[2][0] > self.pos[0] and self.pos[0] + self.size[0] > e[1][0]:
                if e[2][1] > self.pos[1] and self.pos[1] + self.size[1] > e[1][1]:
                    # collision
                    self.delay.value = 0

def Suivre(self):
    b = abs(self.pos[0] - Player.pos[0]) > abs(self.pos[1] - Player.pos[1])
    if self.pos[0] < Player.pos[0]:
        if b:
            self.move[0] = 1
            self.dir.value=0
        else:
            if self.pos[0] == Player.pos[0]:pass
            elif abs(self.pos[0] - Player.pos[0]) > self.speed:self.move[0] = 1
            else:
                self.move[0] = 0
                self.pos[0] = Player.pos[0]
    else:
        if b:
            self.move[0] = -1
            self.dir.value=2
        else:
            if self.pos[0] == Player.pos[0]:pass
            elif abs(self.pos[0] - Player.pos[0]) > self.speed:self.move[0] = -1
            else:
                self.move[0] = 0
                self.pos[0] = Player.pos[0]
    if self.pos[1] < Player.pos[1]:
        if b:
            if self.pos[1] == Player.pos[1]:pass
            elif abs(self.pos[1] - Player.pos[1]) > self.speed:self.move[1] = 1
            else:
                self.move[1] = 0
                self.pos[1] = Player.pos[1]
        else:
            self.move[1] = 1
            self.dir.value=1
    else:
        if b:
            if self.pos[1] == Player.pos[1]:pass
            elif abs(self.pos[1] - Player.pos[1]) > self.speed:self.move[1] = -1
            else:
                self.move[1] = 0
                self.pos[1] = Player.pos[1]
        else:
            self.move[1] = -1
            self.dir.value=3

class Entity(BaseEntity):
    __doc__ = """Utiliser 'class <nom>(Fired):' pour créer une entité.
Entités simples (trajectoire aléatoire) sauf si joueur à proximité
Attributs de ce type de classe :
live : vie de l'entité (100 par défaut)
img_format : format du "tableau d'image" ((1, 'png') par défaut)
Peut être sous la forme (nbr_frames, nbr_directions, format)
Ou avec une rotation automatique si sous la forme (nbr_frames, format)
dmg : dégats infligés à la cible (5 par défaut)
atk_freq : temps (en tic) entre 2 attaques de l'IA (20 par défaut)
speed : vitesse de déplacement de l'entité
range : distance de vue de l'entité
killscore : nombre de points gagnés lorsque l'entité est tuée"""
    live=100
    img_format=(1, "png")
    dmg=5
    atk_freq=20
    atk_delay=0
    killscore=0
    dir=0
    speed = 2
    img=None
    range = 500
    entities = []
    actives = []
    sounded = False
    sound = None
    def __init__(self, pos):
        self.effect = list()
        self.frame = randint(1-self.img_format[0], 0)
        self.pos = Array("f", pos, lock=False)
        self.live = Value("i", self.live)
        self.move = Array("i", 2, lock=False)   # mouvement
        self.dir = Value("i", 0, lock=False)    # direction
        self.atk_delay = Value("i", 0, lock=False)
        self.entities.append(self)
        self.actives.append(Process(target=self.react))
        self.actives[-1].start()
    def clean():
        global Entity, core
        a=0;b=len(Entity.entities)
        while a < b:
            if Entity.entities[a].live.value <= 0:
                core.score+=Entity.entities[a].killscore
                del Entity.entities[a]
                del Entity.actives[a]
                b+=-1
            else:a+=1
    suivre = Suivre
    def react(self):
        if abs(self.pos[0] - Player.pos[0]) < self.range and abs(self.pos[1] - Player.pos[1]) < self.range:self.suivre()
        self.pos[0] += self.move[0] * self.speed * (1-abs(self.move[1]) * 0.3)
        self.pos[1] += self.move[1] * self.speed * (1-abs(self.move[0]) * 0.3)
        self.collide()
    def collide(self):
        global Player, IA, IA_D, Static, Obstacle, Entity
        cond = False
        for e in Entity.entities:
            if e.pos[0] + e.size[0] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[1] + e.size[1] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    if e is self:continue
                    # collision
                    coll=True
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
        for e in IA.entities:
            if e.pos[0] + e.size[0] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[1] + e.size[1] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    # collision
                    coll=True
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
        for e in IA_D.entities:
            if e.pos[0] + e.size[0] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[1] + e.size[1] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    # collision
                    coll=True
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
        for e in Obstacle.entities:
            if e.pos[2] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[3] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    # collision
                    coll=True
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
        for e in Static.entities:
            if e[2][0] > self.pos[0] and self.pos[0] + self.size[0] > e[1][0]:
                if e[2][1] > self.pos[1] and self.pos[1] + self.size[1] > e[1][1]:
                    # collision
                    coll=True
                    if self.move[0] == 1 and self.pos[0] + self.size[0] <= e[1][0] + self.speed:
                        # droite
                        self.pos[0] = e[1][0] - self.size[0]
                    elif self.move[0] == -1 and e[2][0] <= self.pos[0] + self.speed:
                        # gauche
                        self.pos[0] = e[2][0]
                    elif self.move[1] == 1 and self.pos[1] + self.size[1] <= e[1][1] + self.speed:
                        # bas
                        self.pos[1] = e[1][1] - self.size[1]
                    elif self.move[1] == -1 and e[2][1] <= self.pos[1] + self.speed:
                        # haut
                        self.pos[1] = e[2][1]
        if self.atk_delay.value > 0:
            self.atk_delay.value+=-1
        if cond:
            self.move[0] = randint(-1, 1)
            self.move[1] = randint(-1, 1)
        if Player.pos[0] + Player.size[0] > self.pos[0] and self.pos[0] + self.size[0] > Player.pos[0]:
            if Player.pos[1] + Player.size[1] > self.pos[1] and self.pos[1] + self.size[1] > Player.pos[1]:
                # collision
                if self.move[0] == 1 and self.pos[0] + self.size[0] <= Player.pos[0] + self.speed + Player.speed.value:
                    # droite
                    self.pos[0] += -self.speed
                elif self.move[0] == -1 and Player.pos[0] + Player.size[0] <= self.pos[0] + self.speed + Player.speed.value:
                    # gauche
                    self.pos[0] += self.speed
                elif self.move[1] == 1 and self.pos[1] + self.size[1] <= Player.pos[1] + self.speed + Player.speed.value:
                    # bas
                    self.pos[1] += -self.speed
                elif self.move[1] == -1 and Player.pos[1] + Player.size[1] <= self.pos[1] + self.speed + Player.speed.value:
                    # haut
                    self.pos[1] += self.speed
                if self.atk_delay.value == 0:
                    self.atk_delay.value = self.atk_freq
                    Player.live.acquire()
                    Player.live.value+=-self.dmg
                    Player.live.release()
                    if Player.sounded:Player.sound.play()

class IA(BaseEntity):
    __doc__ = """Utiliser 'class <nom>(IA):' pour créer une IA.
Entités intelligentes ! (exemple : monstre)
Attributs de ce type de classe :
live : vie de l'entité (100 par défaut)
img_format : format du "tableau d'image" ((1, 'png') par défaut)
Peut être sous la forme (nbr_frames, nbr_directions, format)
Ou avec une rotation automatique si sous la forme (nbr_frames, format)
dmg : dégats infligés à la cible (5 par défaut)
atk_freq : temps (en tic) entre 2 attaques de l'IA (20 par défaut)
delay : temps de vie (en tic) de l'IA (-1 par défaut)
speed : vitesse de déplacement de l'IA
killscore : nombre de points gagnés lorsque l'IA est tuée"""
    live=100
    img_format=(1, "png")
    dmg=5
    delay = 0
    atk_freq=20
    atk_delay=0
    killscore=0
    dir=0
    speed = 2
    indirect=0
    img=None
    sounded = False
    sound = None
    entities = []
    actives = []
    def clean():
        global IA, core
        a=0;b=len(IA.entities)
        while a < b:
            if IA.entities[a].delay == 0 or IA.entities[a].live.value <= 0:
                if IA.entities[a].delay != 0:core.score+=IA.entities[a].killscore
                del IA.entities[a]
                del IA.actives[a]
                b+=-1
            else:
                a+=1
    def __init__(self, pos):
        self.effect = list()
        self.frame = randint(1-self.img_format[0], 0)
        self.pos = Array("f", pos, lock=False)
        self.live = Value("i", self.live)
        self.move = Array("i", 2, lock=False)   # mouvement
        self.dir = Value("i", 0, lock=False)    # direction
        self.DIR = Value("i", 0, lock=False)    # direction initiale
        self.atk_delay = Value("i", 0, lock=False)
        self.indirect = Value("i", 0, lock=False)
        self.entities.append(self)
        self.actives.append(Process(target=self.react))
        self.actives[-1].start()
    suivre = Suivre
    def react(self):
        global Player
        if not self.indirect.value:self.suivre()
        self.pos[0] += self.move[0] * self.speed * (1-abs(self.move[1]) * 0.3)
        self.pos[1] += self.move[1] * self.speed * (1-abs(self.move[0]) * 0.3)
        self.collide()
    def collide(self):
        global Player, IA, IA_D, Static, Obstacle, Entity
        self.delay+=-1
        cond = True
        for e in Entity.entities:
            if e.pos[0] + e.size[0] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[1] + e.size[1] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    # collision
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
        for e in IA.entities:
            if e.pos[0] + e.size[0] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[1] + e.size[1] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    if e is self:continue
                    # collision
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
        for e in IA_D.entities:
            if e.pos[0] + e.size[0] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[1] + e.size[1] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    if e is self:continue
                    # collision
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
        for e in Obstacle.entities:
            if e.pos[2] > self.pos[0] and self.pos[0] + self.size[0] > e.pos[0]:
                if e.pos[3] > self.pos[1] and self.pos[1] + self.size[1] > e.pos[1]:
                    # collision
                    if self.move[0] == 1 and self.pos[0] + self.size[0] <= e.pos[0] + self.speed:
                        # droite
                        self.pos[0] = e.pos[0] - self.size[0]
                        if self.indirect.value == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir.value == 1:cond = False
                            elif self.dir.value == 0:
                                self.dir.value = 1
                                self.move[1] = 1
                                cond = False
                        elif self.dir.value == 0:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir.value = 1
                            self.move[1] = 1
                            self.indirect.value = 1
                            self.DIR.value = 0
                            cond = False
                    elif self.move[0] == -1 and e.pos[2] <= self.pos[0] + self.speed:
                        # gauche
                        self.pos[0] = e.pos[0] + e.size[0]
                        if self.indirect.value == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir.value == 3:cond = False
                            elif self.dir.value == 2:
                                self.dir.value = 3
                                self.move[1] = -1
                                cond = False
                        elif self.dir.value == 2:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir.value = 3
                            self.move[1] = -1
                            self.indirect.value = 1
                            self.DIR.value = 2
                            cond = False
                    elif self.move[1] == 1 and self.pos[1] + self.size[1] <= e.pos[1] + self.speed:
                        # bas
                        self.pos[1] = e.pos[1] - self.size[1]
                        if self.indirect.value == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir.value == 2:cond = False
                            elif self.dir.value == 1:
                                self.dir.value = 2
                                self.move[0] = -1
                                cond = False
                        elif self.dir.value == 1:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir.value = 2
                            self.move[0] = -1
                            self.indirect.value = 1
                            self.DIR.value = 1
                            cond = False
                    elif self.move[1] == -1 and e.pos[3] <= self.pos[1] + self.speed:
                        # haut
                        self.pos[1] = e.pos[1] + e.size[1]
                        if self.indirect.value == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir.value == 0:cond = False
                            elif self.dir.value == 3:
                                self.dir.value = 0
                                self.move[0] = 1
                                cond = False
                        elif self.dir.value == 3:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir.value = 0
                            self.move[0] = 1
                            self.indirect.value = 1
                            self.DIR.value = 3
                            cond = False
                    if Player.sounded:Player.sound.play()

        for e in Static.entities:
            if e[2][0] > self.pos[0] and self.pos[0] + self.size[0] > e[1][0]:
                if e[2][1] > self.pos[1] and self.pos[1] + self.size[1] > e[1][1]:
                    # collision
                    if self.move[0] == 1 and self.pos[0] + self.size[0] <= e[1][0] + self.speed:
                        # droite
                        self.pos[0] = e[1][0] - self.size[0]
                        if self.indirect.value == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir.value == 1:cond = False
                            elif self.dir.value == 0:
                                self.dir.value = 1
                                self.move[1] = 1
                                cond = False
                        elif self.dir.value == 0:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir.value = 1
                            self.move[1] = 1
                            self.indirect.value = 1
                            self.DIR.value = 0
                            cond = False
                    elif self.move[0] == -1 and e[2][0] <= self.pos[0] + self.speed:
                        # gauche
                        self.pos[0] = e[2][0]
                        if self.indirect.value == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir.value == 3:cond = False
                            elif self.dir.value == 2:
                                self.dir.value = 3
                                self.move[1] = -1
                                cond = False
                        elif self.dir.value == 2:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir.value = 3
                            self.move[1] = -1
                            self.indirect.value = 1
                            self.DIR.value = 2
                            cond = False
                    elif self.move[1] == 1 and self.pos[1] + self.size[1] <= e[1][1] + self.speed:
                        # bas
                        self.pos[1] = e[1][1] - self.size[1]
                        if self.indirect.value == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir.value == 2:cond = False
                            elif self.dir.value == 1:
                                self.dir.value = 2
                                self.move[0] = -1
                                cond = False
                        elif self.dir.value == 1:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir.value = 2
                            self.move[0] = -1
                            self.indirect.value = 1
                            self.DIR.value = 1
                            cond = False
                    elif self.move[1] == -1 and e[2][1] <= self.pos[1] + self.speed:
                        # haut
                        self.pos[1] = e[2][1]
                        if self.indirect.value == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir.value == 0:cond = False
                            elif self.dir.value == 3:
                                self.dir.value = 0
                                self.move[0] = 1
                                cond = False
                        elif self.dir.value == 3:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir.value = 0
                            self.move[0] = 1
                            self.indirect.value = 1
                            self.DIR.value = 3
                            cond = False
        if self.indirect.value == 1 and cond:
            self.dir.value = (self.dir.value - 1)%4
            self.move[self.dir.value%2] = -self.move[self.dir.value%2]
            if self.dir.value == self.DIR.value:
                self.indirect.value = 0
        if self.atk_delay.value > 0:
            self.atk_delay.value+=-1
        if Player.pos[0] + Player.size[0] > self.pos[0] and self.pos[0] + self.size[0] > Player.pos[0]:
            if Player.pos[1] + Player.size[1] > self.pos[1] and self.pos[1] + self.size[1] > Player.pos[1]:
                # collision
                if self.move[0] == 1 and self.pos[0] + self.size[0] <= Player.pos[0] + self.speed + Player.speed.value:
                    # droite
                    self.pos[0] += -self.speed
                elif self.move[0] == -1 and Player.pos[0] + Player.size[0] <= self.pos[0] + self.speed + Player.speed.value:
                    # gauche
                    self.pos[0] += self.speed
                elif self.move[1] == 1 and self.pos[1] + self.size[1] <= Player.pos[1] + self.speed + Player.speed.value:
                    # bas
                    self.pos[1] += -self.speed
                elif self.move[1] == -1 and Player.pos[1] + Player.size[1] <= self.pos[1] + self.speed + Player.speed.value:
                    # haut
                    self.pos[1] += self.speed
                if self.atk_delay.value == 0:
                    self.atk_delay.value = self.atk_freq
                    Player.live.acquire()
                    Player.live.value+=-self.dmg
                    Player.live.release()
                    if Player.sounded:Player.sound.play()

class IA_D(IA):
    __doc__ = """Utiliser 'class <nom>(IA_D):' pour créer une IA lançant des projectiles sur le joueur.
Entités intelligentes ! (exemple : archer)
Attributs de ce type de classe :
Tous les attributs de IA
weapon : projectile lancé par l'IA"""
    entities = []
    actives = []
    def __init__(self, pos=None):raise NotImplementedError("IA_D hasn't been implemented yet.")
    def clean():
        global IA_D, core
        a=0;b=len(IA_D.entities)
        while a < b:
            if IA_D.entities[a].delay == 0 or IA_D.entities[a].live.value <= 0:
                if IA.entities[a].delay != 0:core.score+=IA.entities[a].killscore
                del IA_D.entities[a]
                del IA_D.actives[a]
                b+=-1
            else:
                IA_D.entities[a].delay += -1
                a+=1

def tir():
    global Player
    if Player.atk_delay == 0:
        Player.atk_delay = Player.atk_freq
        M = [Player.pos[0], Player.pos[1]]
        d = Player.dir%4
        M[0]+=(Player.size[0]-Player.weapon.size[0])//2 * (Player.move[0]+1)
        M[1]+=(Player.size[1]-Player.weapon.size[1])//2 * (Player.move[1]+1)
        Player.weapon(M, Player.move)

def UpdateEntities():
    global Static, Obstacle, Fired, IA, IA_D, Player, Entity, core
    Obstacle.clean()
    Fired.clean()
    Entity.clean()
    IA.clean()
    IA_D.clean()
    # ----- SCREEN ----- #
    x = (core.size[0] - Player.size[0])//2 - Player.pos[0]
    y = (core.size[1] - Player.size[1])//2 - Player.pos[1]
    X = x%core.Bsize[0]-core.Bsize[0]
    Y = y%core.Bsize[1]-core.Bsize[1]
    a=0
    while a < core.Bnum[0]:
        b=0
        while b < core.Bnum[1]:
            core.fen.blit(core.img, (X+core.Bsize[0]*a, Y+core.Bsize[1]*b))
            b+=1
        a+=1
    frame=core.tic//6
    for a in Fired.entities:
        core.fen.blit(a.img[frame%a.img_format[0]+a.frame], (x+a.pos[0], y+a.pos[1]))
    for a in Entity.entities:
        core.fen.blit(a.img[a.dir.value][frame%a.img_format[0]+a.frame], (x+a.pos[0], y+a.pos[1]))
    for a in IA.entities:
        core.fen.blit(a.img[a.dir.value][frame%a.img_format[0]+a.frame], (x+a.pos[0], y+a.pos[1]))
    for a in IA_D.entities:
        core.fen.blit(a.img[a.dir.value][frame%a.img_format[0]+a.frame], (x+a.pos[0], y+a.pos[1]))
    core.fen.blit(Player.img[Player.dir][Player.frame],
                  ((core.size[0] - Player.size[0])//2, (core.size[1] - Player.size[1])//2))
    for a in Obstacle.entities:
        core.fen.blit(a.img, (x+a.pos[0], y+a.pos[1]))
    for a in Static.entities:
        core.fen.blit(a[0], (x+a[1][0], y+a[1][1]))
    for a in core.images:
        core.fen.blit(a[0], (x+a[1], y+a[2]))
    core.refresh()
    pygame.display.flip()
    # ------------------ #
    Player.pos[0] += Player.move[0] * (Player.speed.value * (1 - 0.3 * abs(Player.move[1])))
    Player.pos[1] += Player.move[1] * (Player.speed.value * (1 - 0.3 * abs(Player.move[0])))
    core.timexe += 0.05
    T = core.timexe - time()
    if T > 0:sleep(T)
    core.tic+=1
    if core.tic == 360:
        core.tic = 0
        core.timer+=1
    elif T < -1:
        core.lags+=1
        core.timexe=time()+0.05

def Refresh():
    global Static, Obstacle, Fired, IA, IA_D, Player, Entity
    UpdateEntities()
    for a in Fired.actives:
        a.run()
    for a in Entity.actives:
        a.run()
    for a in IA.actives:
        a.run()
    for a in IA_D.actives:
        a.run()
    Player.react.run()
    for a in Player.effect:
        a.delay+=-1
        if a.delay == 0:a.end_effect(Player)
        else:a.active_effect(Player)

def SRefresh():
    "Slower alternative of Refresh"
    global Static, Obstacle, Fired, IA, IA_D, Player, Entity
    UpdateEntities()
    for a in Fired.entities:
        a.react()
    for a in Entity.entities:
        a.react()
    for a in IA.entities:
        a.react()
    for a in IA_D.entities:
        a.react()
    Player.collide()
    for a in Player.effect:
        a.delay+=-1
        if a.delay == 0:a.end_effect()
        else:a.active_effect()

levelist = {0:" :(", 1:" I", 2:" II", 3:" III", 4:" IV", 5:" V", 6:" VI", 7:" VII", 8:" VIII", 9:" IX", 10:" X"}

class effect:
    def __init__(self, delay, level):
        global levelist
        if level < 11:
            self.name+=levelist[level]
        else:self.name+=" ##"
        self.level=level
        self.delay=delay

Player = player()
