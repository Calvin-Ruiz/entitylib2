from random import randint
from time import time, sleep
try:
    import pygame
except:
    import os
    print("ImportError : Pygame wasn't installed !")
    print("Should I install pygame right now ?")
    if input().upper() in ["OUI", "O", "Y", "YES", "INSTALL", "INSTALLER", "TRUE", "1", "CMD", "PIP", "OK"]:
        print("Python folder detected in '"+os.__file__[0:-10]+"'")
        file = open("supprime_moi.bat", "w")
        file.write("cd /d "+os.__file__[0:-10]+"""
python -m pip install --upgrade pip
python -m pip install pygame""")
        file.close()
        os.startfile("supprime_moi.bat")
        input("Press <Entry> after complete installation of pygame")
        import pygame

try:
    import numpy
    from os import listdir
except:
    import os
    print("ImportError : Numpy wasn't installed !\nFunctions 'save' and 'load' need numpy.")
    print("Should I install pygame right now ?")
    if input().upper() in ["OUI", "O", "Y", "YES", "INSTALL", "INSTALLER", "TRUE", "1", "CMD", "PIP", "OK"]:
        print("Python folder detected in '"+os.__file__[0:-10]+"'")
        file = open("supprime_moi.bat", "w")
        file.write("cd /d "+os.__file__[0:-10]+"""
python -m pip install --upgrade pip
python -m pip install numpy""")
        file.close()
        os.startfile("supprime_moi.bat")
        input("Press <Entry> after complete installation of numpy")
        import numpy

pygame.init()
print("Hello from entitylib2 too        https://github.com/Calvin-Ruiz/entitylib2")

def save(filename):
    print("NotImplementedError : save hasn't been implemented yet.");return None
    global Player, Obstacle, Fired, Entity, IA, IA_D
    numpy.save("saves/"+filename, (Player.__dict__, Obstacle.entities, Fired.entities, Entity.entities, IA.entities, IA_D.entities))

def load(filename):
    "return True if save doesn't exist"
    print("NotImplementedError : save hasn't been implemented yet.");return None
    global core, Player, Obstacle, Fired, Entity, IA, IA_D
    if filename in listdir("saves"):
        N = numpy.load("saves/"+filename).tolist()
        Player.__dict__, Obstacle.entities, Fired.entities, Entity.entities, IA.entities, IA_D.entities = N
        return False
    else:return True

class BaseEntity:
    def __repr__(self):
        text = "--------- "+self.name+" ----------\nlive : "+str(self.live)+"\n--- effects ---\n"
        for a in self.effect:text+=str(a)
        return text+"---------------------"+"-"*len(self.name)
    img_format=(1, "png")
    live=20
    atk_freq=20
    atk_delay=0
    Size=None
    def chunking(self):
        global core
        "Test if entity exit chunk"
        if self.pos[0] + self.Size[0] < 0:
            # sortie à gauche
            if self.chunk[0] > core.border[0]:
                core.area["entity"][self.chunk[0]][self.chunk[1]].remove(self)
                self.chunk[0]-=1
                core.area["entity"][self.chunk[0]][self.chunk[1]].append(self)
                self.pos[0]+=256
            else:
                self.pos[0]=-self.Size[0]
        elif self.pos[0] + self.Size[0] > 256:
            # sortie à droite
            if self.chunk[0] < core.border[1]:
                core.area["entity"][self.chunk[0]][self.chunk[1]].remove(self)
                self.chunk[0]+=1
                core.area["entity"][self.chunk[0]][self.chunk[1]].append(self)
                self.pos[0]-=256
            else:
                self.pos[0]=256-self.Size[0]
        if self.pos[1] + self.Size[1] < 0:
            # sortie en haut
            if self.chunk[1] > core.border[2]:
                core.area["entity"][self.chunk[0]][self.chunk[1]].remove(self)
                self.chunk[1]-=1
                core.area["entity"][self.chunk[0]][self.chunk[1]].append(self)
                self.pos[1]+=256
            else:
                self.pos[1]=-self.Size[1]
        elif self.pos[1] + self.Size[1] > 256:
            # sortie en bas
            if self.chunk[1] < core.border[3]:
                core.area["entity"][self.chunk[0]][self.chunk[1]].remove(self)
                self.chunk[1]+=1
                core.area["entity"][self.chunk[0]][self.chunk[1]].append(self)
                self.pos[1]-=256
            else:
                self.pos[1]=256-self.Size[1]
    def apply(self, effect, delay, level):
        for a in self.effect:
            if a.name == effect.name:
                if a.level >= level:
                    a.delay=delay
                    a.level=level
                return None
        self.effect.append(effect(delay, level))
        self.effect[-1].init_effect(self)
    def apply_all(self, liste):
        # deprecated
        l=list()
        for a in self.effect:
            l.append(a.name)
        for a in liste:
            self.effect.append(a[0](a[1], a[2]))
            self.effect[-1].init_effect(self)
    def apply_all(self, liste):
        for e in liste:
            self.apply(e[0], e[1], e[2])

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

def screenshoot():
    global core
    t=int(time())
    date = str(t%60) + "s"
    t//=60
    date = str(t%60) + "m" + date
    t//=60
    t+=2
    date = str(t%24) + "h" + date
    t//=24
    date = str(t) + " on " + date
    pygame.image.save(core.fen, "screenshoots/screenshoot of day " + date +".bmp")
    print("screenshoot saved as 'screenshoot of day "+date+"'")

class core:
    __doc__ = "Content all variables used on this library. Use with caution !"
    __init__ = None
    area={"entity":[], "obs":[], "static":[]}
    model = list()
    while len(model) < 64:
        model.append([])
    model = str(tuple(model))
    a=0
    while a < 64:
        area["entity"].append(eval(model))
        a+=1
    area["entity"] = tuple(area["entity"])
    a=0
    while a < 64:
        area["obs"].append(eval(model))
        a+=1
    area["obs"] = tuple(area["obs"])
    a=0
    while a < 64:
        area["static"].append(eval(model))
        a+=1
    area["static"] = tuple(area["static"])
    score=0
    border = None
    fmode = False
    size = None # fen size
    fen = None
    S = None # chunk size
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
imgeff = dict()

def init(MobTypes, fen_size=(1536, 1024)):
    "MobTypes : tuple of all created class\nInitializing all class in tuple"
    global core, Fired, Player, letters, imgeff
    print("Initialisation...")
    core.S=(fen_size[0]//256+1, fen_size[1]//256+1)
    core.size = ((core.S[0]-1)*256, (core.S[1]-1)*256)
    core.fen = pygame.display.set_mode(core.size)
    core.Bnum = (core.size[0]//core.Bsize[0]+2, core.size[1]//core.Bsize[1]+2)
    core.border = (core.S[0]-2, 65-core.S[0], core.S[1]-2, 65-core.S[1])
    files = listdir("textures")
    for a in MobTypes + (Player,):
        if max(a.size) > 128:print("Warning : maximal size is 128 and "+str(max(a.size))+" > 128")
        a.name = a.__name__
        if a.sound != None:a.sounded=True;a.sound=pygame.mixer.Sound("sounds/"+a.sound)
        if type(a.img_format) is str:
            if a.name + "." + a.img_format in files:
                a.img = pygame.transform.scale(pygame.image.load("textures/" + a.name + "."+a.img_format), a.size)
            else:
                a.img = pygame.transform.scale(pygame.image.load("textures/default.bmp"), a.size)
            continue
        a.Size = (a.size[0]//2, a.size[1]//2)
        try:
            imgs = pygame.image.load("textures/" + a.name + "."+a.img_format[-1])
        except:
            imgs = pygame.image.load("textures/default.bmp")
        a.img = list()
        b=0
        size = imgs.get_size()
        if len(a.img_format) == 3:
            size = (size[0]//a.img_format[0], size[1]//a.img_format[1])
            while b < a.img_format[1]:
                c=0
                a.img.append(list())
                while c < a.img_format[0]:
                    c+=1
                    img=pygame.Surface(size, pygame.SRCALPHA, 32).convert_alpha()
                    img.blit(imgs, ((c - a.img_format[0])*size[0], (1+b - a.img_format[1])*size[1]))
                    a.img[b].append(pygame.transform.scale(img, a.size))
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
                    a.img[b].append(pygame.transform.scale(pygame.transform.rotate(img, (4-b)*90), a.size))
                    c+=1
                b+=1
    for image in listdir("textures/letter"):
        letters.__setitem__(image[0:-4], pygame.image.load("textures/letter/"+image))
    for image in listdir("textures/letters"):
        letters.__setitem__(image[0:-4], pygame.image.load("textures/letters/"+image))
    for image in listdir("textures/effect"):
        imgeff.__setitem__(image[0:-4], pygame.image.load("textures/effect/"+image))
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
        self.atk_delay = 0
    pos = [48, 48]
    move = [0, 0]
    chunk = [31,31]
    size = (32, 32)
    live = 20
    dir = 0
    img = None
    atk_delay = 0
    atk_freq = 10
    weapon = NoWeapon
    frame = 0
    speed = 3
    react = None
    sound = None
    sounded=False
    def chunking(self):
        global core
        "Test if entity exit chunk"
        if self.pos[0] + self.Size[0] < 0:
            # sortie à gauche
            if self.chunk[0] > core.border[0]:
                self.chunk[0]-=1
                self.pos[0]+=256
            else:
                self.pos[0]=-self.Size[0]
        elif self.pos[0] + self.Size[0] > 256:
            # sortie à droite
            if self.chunk[0] < core.border[1]:
                self.chunk[0]+=1
                self.pos[0]-=256
            else:
                self.pos[0]=256-self.Size[0]
        if self.pos[1] + self.Size[1] < 0:
            # sortie en haut
            if self.chunk[1] > core.border[2]:
                self.chunk[1]-=1
                self.pos[1]+=256
            else:
                self.pos[1]=-self.Size[1]
        elif self.pos[1] + self.Size[1] > 256:
            # sortie en bas
            if self.chunk[1] < core.border[3]:
                self.chunk[1]+=1
                self.pos[1]-=256
            else:
                self.pos[1]=256-self.Size[0]
    def collide(self):
        global core, IA, IA_D, Static, Obstacle, Entity
        cond = False
        x, y = self.pos
        a=0
        x+=256
        y+=256
        while a < 9:
            if a%3:
                x-=256
            elif a//3:
                x+=512
                y-=256
            for e in core.area["entity"][self.chunk[0]+a%3-1][self.chunk[1]+a//3-1]:
                if e.pos[0] + e.size[0] > x and x + self.size[0] > e.pos[0] and e.pos[1] + e.size[1] > y and y + self.size[1] > e.pos[1]:
                    # collision
                    coll=True
                    if x + self.size[0] + e.move[0]*e.speed <= e.pos[0] + self.move[0]*self.speed + 0.4*(e.speed+self.speed):
                        # droite
                        if self.move[0]==1:x -= self.speed * (1 - 0.3 * abs(self.move[1]))
                        if e.move[0]==-1:e.pos[0] += e.speed * (1 - 0.3 * abs(e.move[1]))
                    elif x + e.move[0]*e.speed + 0.4*(e.speed+self.speed) >= e.pos[0] + e.size[0] + self.move[0]*self.speed:
                        # gauche
                        if self.move[0]==-1:x += self.speed * (1 - 0.3 * abs(self.move[1]))
                        if e.move[0]==1:e.pos[0] -= e.speed * (1 - 0.3 * abs(e.move[1]))
                    if y + self.size[1] + e.move[1]*e.speed <= e.pos[1] + self.move[1]*self.speed + 0.4*(e.speed+self.speed):
                        # bas
                        if self.move[1]==1:y -= self.speed * (1 - 0.3 * abs(self.move[0]))
                        if e.move[1]==-1:e.pos[1] += e.speed * (1 - 0.3 * abs(e.move[0]))
                    elif y + e.move[1]*e.speed + 0.4*(e.speed+self.speed) >= e.pos[1] + e.size[1] + self.move[1]*self.speed:
                        # haut
                        if self.move[1]==-1:y += self.speed * (1 - 0.3 * abs(self.move[0]))
                        if e.move[1]==1:e.pos[1] -= e.speed * (1 - 0.3 * abs(e.move[0]))
                    if e.atk_delay == 0:
                        e.atk_delay = e.atk_freq
                        self.live+=-e.dmg
                        if self.sounded:self.sound.play()
            a+=1
        a=0
        x+=512
        y+=512
        while a < 4:
            if a%2:
                x-=256
            elif a//2:
                x+=256
                y-=256
            for e in core.area["obs"][self.chunk[0]+a%2-1][self.chunk[1]+a//2-1]:
                if e.pos[2] > x and x + self.size[0] > e.pos[0] and e.pos[3] > y and y + self.size[1] > e.pos[1]:
                    # collision
                    coll=True
                    if self.move[0] == 1 and x + self.size[0] <= e.pos[0] + self.speed:
                        # droite
                        x = e.pos[0] - self.size[0]
                    elif self.move[0] == -1 and e.pos[2] <= x + self.speed:
                        # gauche
                        x = e.pos[0] + e.size[0]
                    elif self.move[1] == 1 and y + self.size[1] <= e.pos[1] + self.speed:
                        # bas
                        y = e.pos[1] - self.size[1]
                    elif self.move[1] == -1 and e.pos[3] <= y + self.speed:
                        # haut
                        y = e.pos[1] + e.size[1]
            for e in core.area["static"][self.chunk[0]+a%2-1][self.chunk[1]+a//2-1]:
                if e[2][0] > x and x + self.size[0] > e[1][0] and e[2][1] > y and y + self.size[1] > e[1][1]:
                    # collision
                    coll=True
                    if self.move[0] == 1 and x + self.size[0] <= e[1][0] + self.speed:
                        # droite
                        x = e[1][0] - self.size[0]
                    elif self.move[0] == -1 and e[2][0] <= x + self.speed:
                        # gauche
                        x = e[2][0]
                    elif self.move[1] == 1 and y + self.size[1] <= e[1][1] + self.speed:
                        # bas
                        y = e[1][1] - self.size[1]
                    elif self.move[1] == -1 and e[2][1] <= y + self.speed:
                        # haut
                        y = e[2][1]
            a+=1
        if self.atk_delay > 0:
            self.atk_delay+=-1
        self.pos[0]=x
        self.pos[1]=y

class Static:
    __doc__ = """Utiliser 'nom = Static(*args)' pour créer un mur.
Utiliser nom.append(pos, chunk) pour ajouter une mur.
Renvoie un type d'objet indestructible et immobile.
Tout objet Static ne pourra jamais être traversé, il sera toujours 'solide'.
img_format : format de l'image ('png' par défaut)
size : tuple de la hauteur et de la largeur de l'entité désiré"""
    def __init__(self, name, size, img_format="png"):
        global Static
        self.img = pygame.transform.scale(pygame.image.load("textures/"+name + "."+img_format), size)
        self.size = size
    def append(self, pos, chunk):
        "pos : position du mur dans le chunk de 0 à 255 (exemple : (314,159))\nchunk : chunk contenant le mur de -29 à 29 (exemple : (1,-2))"
        global core
        self.pos = pos + (pos[0]+self.size[0], pos[1]+self.size[1])
        a = (pos[0]+self.size[0]//2-128)//256
        b = (pos[1]+self.size[1]//2-128)//256
        chunk = list(chunk)
        pos = list(pos)
        chunk[0] += a+31
        chunk[1] += b+31
        pos[0] += -a*256
        pos[1] += -b*256
        core.area["static"][chunk[0]][chunk[1]].append((self.img, pos, (pos[0]+self.size[0], pos[1]+self.size[1])))

class Obstacle:
    __doc__ = """Utiliser 'class <nom>(Obstacle):' pour créer un obstacle (similaire à mur).
Attributs de ce type de classe :
live : points de vie de l'obstacle
img_format : format de l'image ('png' par défaut)
size : tuple de la hauteur et de la largeur de l'entité désiré
Ce type d'objet est statique mais destructible."""
    entities = []
    def __init__(self, pos, chunk):
        global core
        self.pos = pos + (pos[0]+self.size[0], pos[1]+self.size[1])
        self.chunk = (chunk[0]+31, chunk[1]+31)
        self.entities.append(self)
        core.area["obs"][self.chunk[0]][self.chunk[1]].append(self)
        
    img_format="png"
    img=None
    sounded = False
    sound = None
    def clean():
        global Obstacle,core
        a=0;b=len(Obstacle.entities)
        while a < b:
            if Obstacle.entities[a].live <= 0:
                core.area["obs"][Obstacle.entities[a].chunk[0]][Obstacle.entities[a].chunk[1]].remove(Obstacle.entities[a])
                del Obstacle.entities[a]
                b+=-1
            else:a+=1

def Rien(self):pass

class Fired:
    __doc__ = """Utiliser 'class <nom>(Fired):' pour créer un projectile.
Entités mobiles (exemple : flèche)
Attributs de ce type de classe :
speed : vitesse de déplacement (0 par défaut)
pcoll : activer la collision avec le joueur (True par défaut)
ecoll : activer la collision avec les entités (True par défaut)
action : action supplémentaire quand contact avec le joueur (renvoie le projectile comme argument)
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
    ecoll = True
    action = Rien
    sounded = False
    sound = None
    frame = 0
    dmg = 0
    delay = -1
    effects = tuple()
    img_format = (1, "png")
    img=None
    def __init__(self, pos, chunk, move):
        """pos : position du projectile (exemple : (367, -23) )
move : mouvement du projectile en x et en y.
1 : mouvement positif, 0 : immobile et -1 : mouvement négatif
(exemple : (-1, 1) )"""
        global Player
        self.frame = randint(1-self.img_format[0], 0)
        self.pos = list(pos)
        self.chunk = list(chunk)
        if move == [0,0]:move=list({0:(1, 0), 1:(0, 1), 2:(-1, 0), 3:(0, -1)}[Player.dir])
        self.move = move
        img=list()
        for a in self.img[0]:
            img.append(pygame.transform.rotate(a, {(1, 0) : 0,(1, 1) : 45,(0, 1) : 90,(-1, 1) : 135,(-1, 0) : 180,(-1, -1): 225,(0, -1) : 270,(1, -1) : 315}[tuple(move)]))
        self.img=img
        self.entities.append(self)
        self.actives.append(self.react)

    def clean():
        global Fired
        a=0;b=len(Fired.entities)
        while a < b:
            if Fired.entities[a].delay == 0:
                if Fired.entities[a].sounded:Fired.entities[a].sound.play()
                del Fired.entities[a]
                del Fired.actives[a]
                b+=-1
            else:a+=1
    def react(self):
        global core
        "Test if entity exit chunk"
        if self.pos[0] + self.Size[0] < 0:
            # sortie à gauche
            if self.chunk[0] > 1:
                self.chunk[0]-=1
                self.pos[0]+=256
            else:
                self.pos[0]=0
        elif self.pos[0] + self.Size[0] > 256:
            # sortie à droite
            if self.chunk[0] < 62:
                self.chunk[0]+=1
                self.pos[0]-=256
            else:
                self.pos[0]=256-self.size[0]
        if self.pos[1] + self.Size[1] < 0:
            # sortie en haut
            if self.chunk[1] > 1:
                self.chunk[1]-=1
                self.pos[1]+=256
            else:
                self.pos[1]=0
        elif self.pos[1] + self.Size[1] > 256:
            # sortie en bas
            if self.chunk[1] < 62:
                self.chunk[1]+=1
                self.pos[1]-=256
            else:
                self.pos[1]=256-self.size[1]
        if self.delay>0:self.delay += -1
        x = self.pos[0] + self.move[0] * (self.speed * (1 - 0.3 * abs(self.move[1])))
        y = self.pos[1] + self.move[1] * (self.speed * (1 - 0.3 * abs(self.move[0])))
        if self.pcoll and Player.pos[0] + Player.size[0] > x and x + self.size[0] > Player.pos[0] and Player.pos[1] + Player.size[1] > y and y + self.size[1] > Player.pos[1]:
            # collision
            self.action()
            self.delay = 0
            Player.live += -self.dmg
            e.apply_all(self.effects)
            if Player.sounded:Player.sound.play()
        x+=256
        y+=256
        for a in range(0,4):
            if a%2:
                x+=-256
            elif a//2:
                x+=256
                y-=256
            if self.ecoll:
                for e in core.area["entity"][self.chunk[0]+a%2-1][self.chunk[1]+a//2-1]:
                    if e.pos[0] + e.size[0] > x and x + self.size[0] > e.pos[0] and e.pos[1] + e.size[1] > y and y + self.size[1] > e.pos[1]:
                        # collision
                        self.delay = 0
                        e.live -= self.dmg
                        e.apply_all(self.effects)
                        if e.sounded:e.sound.play()
            for e in core.area["obs"][self.chunk[0]+a%2-1][self.chunk[1]+a//2-1]:
                if e.pos[2] > x and x + self.size[0] > e.pos[0] and e.pos[3] > y and y + self.size[1] > e.pos[1]:
                    # collision
                    self.delay = 0
                    e.live -= self.dmg
                    if e.sounded:e.sound.play()
            for e in core.area["static"][self.chunk[0]+a%2-1][self.chunk[1]+a//2-1]:
                if e[2][0] > x and x + self.size[0] > e[1][0] and e[2][1] > y and y + self.size[1] > e[1][1]:
                    # collision
                    self.delay = 0
        self.pos[0]=x
        self.pos[1]=y

def Suivre(self):
    global core
    a = self.pos[0] - Player.pos[0] + 256*(self.chunk[0] - Player.chunk[0])
    b = self.pos[1] - Player.pos[1] + 256*(self.chunk[1] - Player.chunk[1])
    c = abs(a) > abs(b)
    if a < 0:
        if c:
            self.move[0] = 1
            self.dir=0
        else:
            if a == 0:pass
            elif abs(a) > self.speed:self.move[0] = 1
            else:
                self.move[0] = 0
                self.pos[0] = Player.pos[0]
                if self.chunk[0] != Player.chunk[0]:
                    core.area["entity"][self.chunk[0]][self.chunk[1]].remove(self)
                    self.chunk[0]=Player.chunk[0]
                    core.area["entity"][self.chunk[0]][self.chunk[1]].append(self)
    else:
        if c:
            self.move[0] = -1
            self.dir=2
        else:
            if a == 0:pass
            elif abs(a) > self.speed:self.move[0] = -1
            else:
                self.move[0] = 0
                self.pos[0] = Player.pos[0]
                if self.chunk[0] != Player.chunk[0]:
                    core.area["entity"][self.chunk[0]][self.chunk[1]].remove(self)
                    self.chunk[0]=Player.chunk[0]
                    core.area["entity"][self.chunk[0]][self.chunk[1]].append(self)
    if b < 0:
        if c:
            if b == 0:pass
            elif abs(b) > self.speed:self.move[1] = 1
            else:
                self.move[1] = 0
                self.pos[1] = Player.pos[1]
                if self.chunk[1] != Player.chunk[1]:
                    core.area["entity"][self.chunk[0]][self.chunk[1]].remove(self)
                    self.chunk[1]=Player.chunk[1]
                    core.area["entity"][self.chunk[0]][self.chunk[1]].append(self)
        else:
            self.move[1] = 1
            self.dir=1
    else:
        if c:
            if b == 0:pass
            elif abs(b) > self.speed:self.move[1] = -1
            else:
                self.move[1] = 0
                self.pos[1] = Player.pos[1]
                if self.chunk[1] != Player.chunk[1]:
                    core.area["entity"][self.chunk[0]][self.chunk[1]].remove(self)
                    self.chunk[1]=Player.chunk[1]
                    core.area["entity"][self.chunk[0]][self.chunk[1]].append(self)
        else:
            self.move[1] = -1
            self.dir=3

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
xp : nombre de points gagnés lorsque l'entité est tuée"""
    dmg=2
    xp=0
    dir=0
    speed = 2
    img=None
    range = 500
    entities = []
    actives = []
    sounded = False
    sound = None
    def __init__(self, pos, chunk):
        global core
        self.effect = list()
        self.frame = randint(1-self.img_format[0], 0)
        self.pos = list(pos)
        self.chunk = [chunk[0]+31, chunk[1]+31]
        self.move = [0, 0]  # mouvement
        self.dir = 0        # direction
        self.atk_delay = 0
        self.entities.append(self)
        self.actives.append(self.react)
        core.area["entity"][self.chunk[0]][self.chunk[1]].append(self)
    def clean():
        global Entity, core
        a=0;b=len(Entity.entities)
        while a < b:
            if Entity.entities[a].live <= 0:
                E = Entity.entities[a]
                core.score+=E.xp
                core.area["entity"][E.chunk[0]][E.chunk[1]].remove(E)
                del Entity.entities[a]
                del Entity.actives[a]
                b+=-1
            else:a+=1
    suivre = Suivre
    def react(self):
        if abs(self.chunk[0] - Player.chunk[0]) + abs(self.chunk[1] - Player.chunk[1]) < self.range:self.suivre()
        self.pos[0] += self.move[0] * self.speed * (1-abs(self.move[1]) * 0.3)
        self.pos[1] += self.move[1] * self.speed * (1-abs(self.move[0]) * 0.3)
        self.chunking()
        self.collide()
    def collide(self):
        global Player, IA, IA_D, Static, Obstacle, Entity
        cond = False
        x, y = self.pos[0:2]
        a=0
        x+=256
        y+=256
        while True:
            if a%2:
                x-=256
            elif a//2:
                x+=256
                y-=256
            for e in core.area["entity"][self.chunk[0]+a%2-1][self.chunk[1]+a//2-1]:
                if e.pos[0] + e.size[0] > x and x + self.size[0] > e.pos[0] and e.pos[1] + e.size[1] > y and y + self.size[1] > e.pos[1]:
                    if e is self:continue
                    # collision
                    coll=True
                    unsolved=True
                    if x + self.size[0] + e.move[0]*e.speed <= e.pos[0] + self.move[0]*self.speed + 0.3*(e.speed+self.speed):
                        # droite
                        if self.move[0]==1:x -= self.speed * (1 - 0.3 * abs(self.move[1]))
                        if e.move[0]==-1:e.pos[0] += e.speed * (1 - 0.3 * abs(e.move[1]))
                        unsolved=False
                    elif x + e.move[0]*e.speed + 0.3*(e.speed+self.speed) >= e.pos[0] + e.size[0] + self.move[0]*self.speed:
                        # gauche
                        if self.move[0]==-1:x += self.speed * (1 - 0.3 * abs(self.move[1]))
                        if e.move[0]==1:e.pos[0] -= e.speed * (1 - 0.3 * abs(e.move[1]))
                        unsolved=False
                    if y + self.size[1] + e.move[1]*e.speed <= e.pos[1] + self.move[1]*self.speed + 0.3*(e.speed+self.speed):
                        # bas
                        if self.move[1]==1:y -= self.speed * (1 - 0.3 * abs(self.move[0]))
                        if e.move[1]==-1:e.pos[1] += e.speed * (1 - 0.3 * abs(e.move[0]))
                        unsolved=False
                    elif y + e.move[1]*e.speed + 0.3*(e.speed+self.speed) >= e.pos[1] + e.size[1] + self.move[1]*self.speed:
                        # haut
                        if self.move[1]==-1:y += self.speed * (1 - 0.3 * abs(self.move[0]))
                        if e.move[1]==1:e.pos[1] -= e.speed * (1 - 0.3 * abs(e.move[0]))
                        unsolved=False
                    if unsolved:
                        # méthode anti-superposition !
                        if self.move[0]==1:x -= self.speed * (2 - 0.6 * abs(self.move[1]))
                        elif self.move[0]==-1:x += self.speed * (2 - 0.6 * abs(self.move[1]))
                        if self.move[1]==1:y -= self.speed * (2 - 0.6 * abs(self.move[0]))
                        elif self.move[1]==-1:y += self.speed * (2 - 0.6 * abs(self.move[0]))
            if a == 4:break
            for e in core.area["obs"][self.chunk[0]+a%2-1][self.chunk[1]+a//2-1]:
                if e.pos[2] > x and x + self.size[0] > e.pos[0] and e.pos[3] > y and y + self.size[1] > e.pos[1]:
                    # collision
                    coll=True
                    if x + self.size[0] <= e.pos[0] + self.speed:
                        # droite
                        x = e.pos[0] - self.size[0]
                    elif e.pos[2] <= x + self.speed:
                        # gauche
                        x = e.pos[2]
                    elif y + self.size[1] <= e.pos[1] + self.speed:
                        # bas
                        y = e.pos[1] - self.size[1]
                    elif e.pos[3] <= y + self.speed:
                        # haut
                        y = e.pos[3]
            for e in core.area["static"][self.chunk[0]+a%2-1][self.chunk[1]+a//2-1]:
                if e[2][0] > x and x + self.size[0] > e[1][0] and e[2][1] > y and y + self.size[1] > e[1][1]:
                    # collision
                    coll=True
                    if x + self.size[0] <= e[1][0] + self.speed:
                        # droite
                        x = e[1][0] - self.size[0]
                    elif e[2][0] <= x + self.speed:
                        # gauche
                        x = e[2][0]
                    elif y + self.size[1] <= e[1][1] + self.speed:
                        # bas
                        y = e[1][1] - self.size[1]
                    elif e[2][1] <= y + self.speed:
                        # haut
                        y = e[2][1]
            a+=1
        if self.atk_delay > 0:
            self.atk_delay+=-1
        if cond:
            self.move[0] = randint(-1, 1)
            self.move[1] = randint(-1, 1)
        self.pos[0]=x-256
        self.pos[1]=y+256

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
xp : nombre de points gagnés lorsque l'IA est tuée"""
    dmg=2
    delay = 0
    xp=0
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
            if IA.entities[a].delay == 0 or IA.entities[a].live <= 0:
                I = IA.entities[a]
                if I.delay != 0:core.score+=I.xp
                core.area["entity"][I.chunk[0]][I.chunk[1]].remove(I)
                del IA.entities[a]
                del IA.actives[a]
                b+=-1
            else:
                a+=1
    def __init__(self, pos, chunk):
        global core
        self.effect = list()
        self.frame = randint(1-self.img_format[0], 0)
        self.pos = list(pos)
        self.chunk = [chunk[0]+31, chunk[1]+31]
        self.move = [0,0]   # mouvement
        self.dir = 0        # direction
        self.DIR = 0        # direction initiale
        self.atk_delay = 0
        self.indirect = 0
        self.entities.append(self)
        self.actives.append(self.react)
        core.area["entity"][self.chunk[0]][self.chunk[1]].append(self)
    suivre = Suivre
    def react(self):
        global Player
        if not self.indirect:self.suivre()
        self.pos[0] += self.move[0] * self.speed * (1-abs(self.move[1]) * 0.3)
        self.pos[1] += self.move[1] * self.speed * (1-abs(self.move[0]) * 0.3)
        self.chunking()
        self.collide()
    def collide(self):
        global Player, IA, IA_D, Static, Obstacle, Entity
        self.delay+=-1
        cond = True
        x, y = self.pos[0:2]
        a=0
        x+=256
        y+=256
        while True:
            if a%2:
                x-=256
            elif a//2:
                x+=256
                y-=256
            for e in core.area["entity"][self.chunk[0]+a%2-1][self.chunk[1]+a//2-1]:
                if e.pos[0] + e.size[0] > x and x + self.size[0] > e.pos[0] and e.pos[1] + e.size[1] > y and y + self.size[1] > e.pos[1]:
                    if e is self:continue
                    # collision
                    coll=True
                    unsolved = True
                    if x + self.size[0] + e.move[0]*e.speed <= e.pos[0] + self.move[0]*self.speed + 0.3*(e.speed+self.speed):
                        # droite
                        if self.move[0]==1:x -= self.speed * (1 - 0.3 * abs(self.move[1]))
                        if e.move[0]==-1:e.pos[0] += e.speed * (1 - 0.3 * abs(e.move[1]))
                        unsolved = False
                    elif x + e.move[0]*e.speed + 0.3*(e.speed+self.speed) >= e.pos[0] + e.size[0] + self.move[0]*self.speed:
                        # gauche
                        if self.move[0]==-1:x += self.speed * (1 - 0.3 * abs(self.move[1]))
                        if e.move[0]==1:e.pos[0] -= e.speed * (1 - 0.3 * abs(e.move[1]))
                        unsolved = False
                    if y + self.size[1] + e.move[1]*e.speed <= e.pos[1] + self.move[1]*self.speed + 0.3*(e.speed+self.speed):
                        # bas
                        if self.move[1]==1:y -= self.speed * (1 - 0.3 * abs(self.move[0]))
                        if e.move[1]==-1:e.pos[1] += e.speed * (1 - 0.3 * abs(e.move[0]))
                        unsolved = False
                    elif y + e.move[1]*e.speed + 0.3*(e.speed+self.speed) >= e.pos[1] + e.size[1] + self.move[1]*self.speed:
                        # haut
                        if self.move[1]==-1:y += self.speed * (1 - 0.3 * abs(self.move[0]))
                        if e.move[1]==1:e.pos[1] -= e.speed * (1 - 0.3 * abs(e.move[0]))
                        unsolved = False
                    if unsolved:
                        # méthode anti-superposition !
                        if self.move[0]==1:x -= self.speed * (2 - 0.6 * abs(self.move[1]))
                        elif self.move[0]==-1:x += self.speed * (2 - 0.6 * abs(self.move[1]))
                        if self.move[1]==1:y -= self.speed * (2 - 0.6 * abs(self.move[0]))
                        elif self.move[1]==-1:y += self.speed * (2 - 0.6 * abs(self.move[0]))
            if a == 4:break
            for e in core.area["obs"][self.chunk[0]+a%2-1][self.chunk[1]+a//2-1]:
                if e.pos[2] > x and x + self.size[0] > e.pos[0] and e.pos[3] > y and y + self.size[1] > e.pos[1]:
                    # collision
                    if x + self.size[0] <= e.pos[0] + self.speed:
                        # droite
                        x = e.pos[0] - self.size[0]
                        if self.indirect == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir == 1:cond = False
                            elif self.dir == 0:
                                self.dir = 1
                                self.move[1] = 1
                                cond = False
                        elif self.dir == 0:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir = 1
                            self.move[1] = 1
                            self.indirect = 1
                            self.DIR = 0
                            cond = False
                    elif e.pos[2] <= x + self.speed:
                        # gauche
                        x = e.pos[2]
                        if self.indirect == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir == 3:cond = False
                            elif self.dir == 2:
                                self.dir = 3
                                self.move[1] = -1
                                cond = False
                        elif self.dir == 2:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir = 3
                            self.move[1] = -1
                            self.indirect = 1
                            self.DIR = 2
                            cond = False
                    elif y + self.size[1] <= e.pos[1] + self.speed:
                        # bas
                        y = e.pos[1] - self.size[1]
                        if self.indirect == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir == 2:cond = False
                            elif self.dir == 1:
                                self.dir = 2
                                self.move[0] = -1
                                cond = False
                        elif self.dir == 1:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir = 2
                            self.move[0] = -1
                            self.indirect = 1
                            self.DIR = 1
                            cond = False
                    elif e.pos[3] <= y + self.speed:
                        # haut
                        y = e.pos[3]
                        if self.indirect == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir == 0:cond = False
                            elif self.dir == 3:
                                self.dir = 0
                                self.move[0] = 1
                                cond = False
                        elif self.dir == 3:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir = 0
                            self.move[0] = 1
                            self.indirect = 1
                            self.DIR = 3
                            cond = False
            for e in core.area["static"][self.chunk[0]+a%2-1][self.chunk[1]+a//2-1]:
                if e[2][0] > x and x + self.size[0] > e[1][0] and e[2][1] > y and y + self.size[1] > e[1][1]:
                    # collision
                    if x + self.size[0] <= e[1][0] + self.speed:
                        # droite
                        x = e[1][0] - self.size[0]
                        if self.indirect == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir == 1:cond = False
                            elif self.dir == 0:
                                self.dir = 1
                                self.move[1] = 1
                                cond = False
                        elif self.dir == 0:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir = 1
                            self.move[1] = 1
                            self.indirect = 1
                            self.DIR = 0
                            cond = False
                    elif e[2][0] <= x + self.speed:
                        # gauche
                        x = e[2][0]
                        if self.indirect == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir == 3:cond = False
                            elif self.dir == 2:
                                self.dir = 3
                                self.move[1] = -1
                                cond = False
                        elif self.dir == 2:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir = 3
                            self.move[1] = -1
                            self.indirect = 1
                            self.DIR = 2
                            cond = False
                    elif y + self.size[1] <= e[1][1] + self.speed:
                        # bas
                        y = e[1][1] - self.size[1]
                        if self.indirect == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir == 2:cond = False
                            elif self.dir == 1:
                                self.dir = 2
                                self.move[0] = -1
                                cond = False
                        elif self.dir == 1:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir = 2
                            self.move[0] = -1
                            self.indirect = 1
                            self.DIR = 1
                            cond = False
                    elif e[2][1] <= y + self.speed:
                        # haut
                        y = e[2][1]
                        if self.indirect == 1:
                            # On est déja en train de contourner un obstacle
                            if self.dir == 0:cond = False
                            elif self.dir == 3:
                                self.dir = 0
                                self.move[0] = 1
                                cond = False
                        elif self.dir == 3:
                            # On se cogne juste contre un mur dans sa direction
                            self.dir = 0
                            self.move[0] = 1
                            self.indirect = 1
                            self.DIR = 3
                            cond = False
            a+=1
        if self.indirect == 1 and cond:
            self.dir = (self.dir - 1)%4
            self.move[self.dir%2] = -self.move[self.dir%2]
            if self.dir == self.DIR:
                self.indirect = 0
        if self.atk_delay > 0:
            self.atk_delay+=-1
        rem = list()
        for a in self.effect:
            a.delay+=-1
            if a.delay == 0:
                a.end_effect(self)
                rem.append(a)
            else:
                a.active_effect(self)
        for a in rem:
            self.effect.remove(a)
        self.pos[0]=x-256
        self.pos[1]=y+256

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
            if IA_D.entities[a].delay == 0 or IA_D.entities[a].live <= 0:
                if IA.entities[a].delay != 0:core.score+=IA.entities[a].xp
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
        if Player.move == (0, 0):
            if Player.dir%2:
                if Player.dir:m=(0,-1)
                else:m=(0,1)
            else:
                if Player.dir==1:m=(1,0)
                else:m=(-1,0)
        else:Player.weapon(M, Player.chunk.copy(), Player.move.copy())

def UpdateEntities():
    global Static, Obstacle, Fired, IA, IA_D, Player, Entity, core, imgeff, player
    Obstacle.clean()
    Fired.clean()
    Entity.clean()
    IA.clean()
    IA_D.clean()
    # ----- SCREEN ----- #
    x = (core.size[0] - Player.size[0])//2 - Player.pos[0] - 512
    y = (core.size[1] - Player.size[1])//2 - Player.pos[1] - 512
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
    # Add Fired to screen
    chunk0 = (Player.chunk[0]-1, Player.chunk[1]-1)
    c = -1
    while c < core.S[1]:
        b = -1
        while b < core.S[0]:
            pos = (chunk0[0]+b, chunk0[1]+c)
            for a in core.area["entity"][pos[0]][pos[1]]:
                core.fen.blit(a.img[a.dir][(frame+a.frame)%a.img_format[0]], (x+a.pos[0], y+a.pos[1]))
            for a in core.area["obs"][pos[0]][pos[1]]:
                core.fen.blit(a.img, (x+a.pos[0], y+a.pos[1]))
            for a in core.area["static"][pos[0]][pos[1]]:
                core.fen.blit(a[0], (x+a[1][0], y+a[1][1]))
            x += 256
            b += 1
        x -= 256*(core.S[0]+1)
        y += 256
        c += 1
    y -= 256*(core.S[1]-1)
    x += 512
    core.fen.blit(Player.img[Player.dir][Player.frame],
                  ((core.size[0] - Player.size[0])//2, (core.size[1] - Player.size[1])//2))
    for a in Fired.entities:
        core.fen.blit(a.img[frame%a.img_format[0]+a.frame], (x+a.pos[0]+256*(a.chunk[0] - Player.chunk[0]), y+a.pos[1]+256*(a.chunk[1] - Player.chunk[1])))
    for a in core.images:
        core.fen.blit(a[0], (a[1], a[2]))
    b=0
    rem = list()
    for a in Player.effect:
        a.delay+=-1
        if a.delay > 1200:core.fen.blit(imgeff["contour green"], (b, 0))
        elif a.delay > 200:core.fen.blit(imgeff["contour orange"], (b, 0))
        elif a.delay == 0:
            a.end_effect(Player)
            rem.append(a)
        else:
            core.fen.blit(imgeff["contour red"], (b, 0))
            a.active_effect(Player)
        core.fen.blit(imgeff[a.name], (b+8, 8))
        b+=64
    for a in rem:
        Player.effect.remove(a)
    core.fen.fill(b'\x00\x00\x00', (0, core.size[1]-16, player.live, core.size[1]))
    core.fen.fill(b'\xff\x00\x00', (0, core.size[1]-16, Player.live*10, core.size[1]))
    core.refresh()
    pygame.display.flip()
    # ------------------ #
    Player.pos[0] += Player.move[0] * (Player.speed * (1 - 0.3 * abs(Player.move[1])))
    Player.pos[1] += Player.move[1] * (Player.speed * (1 - 0.3 * abs(Player.move[0])))
    core.timexe += 0.05
    T = core.timexe - time()
    if T > 0:sleep(T)
    core.tic+=1
    if core.tic == 360:
        core.tic = 0
        core.timer+=1
    elif T < -1:
        core.timexe=time()

def Refresh():
    "Move entities, refresh screen and test collisions"
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
    Player.chunking()
    Player.collide()

class effect:
    def __repr__(self):
        if self.level > 12:return self.name + "  ##\n duration : " + str(self.delay//20)+"s\n"
        if self.level < 0:return self.name + "   ##\n duration : " + str(self.delay//20)+"s\n"
        return self.name + (""," I"," II"," III"," IV"," V"," VI"," VII"," VIII"," IX"," X"," XI"," XII")[self.level] + "\n  duration : " + str(self.delay//20)+"s\n"
    def __init__(self, delay, level):
        self.level=level
        self.delay=delay

Player = player()
