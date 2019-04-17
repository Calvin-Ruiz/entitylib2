from entitylib2 import *
mur = Static("default", (128, 16), "bmp")
class obs(Obstacle):
    live=100
    size=(32, 32)

class ent(Entity):
    dmg=2
    xp=10
    size=(32, 32)

class Zombie(IA):
    img_format = (4,4,"png")
    dmg=2
    xp = 10
    delay = 12000
    size=(16, 32)
    sound="blast.wav"

class arrow(Fired):
    size=(16, 16)
    pcoll=False
    speed=10
    delay=50
    dmg=2

class speed(effect):
    name = "speed boost"
    def init_effect(self, entity):
        "action when effect given"
        entity.speed = entity.__class__.speed*(1+self.level/2)
    active_effect=NoWeapon # NoWeapon represent passive function with 2 args
    def end_effect(self, entity):
        "action when effect disappear"
        entity.speed = entity.__class__.speed # règle la vitesse de l'entité sur la vitesse de base de cet entité

init((arrow, obs, ent, Zombie), (256*3, 256*2))

mur.append((12, 52), (0, -1))
obs((54, 80), (1, 0))
#ent((randint(0, 255), randint(0, 255)), (randint(-2, 2), randint(-2, 2)))
for a in range(0, 4): # --> faire 4 fois
    Zombie((randint(0, 255), randint(0, 255)), (randint(-2, 2), randint(-2, 2)))
Player.weapon = arrow # Le joueur lance des projectiles 'arrow'
Player.apply(speed, 300, 1) # applique l'effet 'speed' pour une durée de 300/20 s au niveau 1
Player.atk_freq=5 # 5/20 s de délai d'attaque pour le joueur

continuer=True
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                Player.move[0] = 1
                Player.dir = 0
            elif event.key == pygame.K_LEFT:
                Player.move[0] = -1
                Player.dir = 2
            elif event.key == pygame.K_DOWN:
                Player.move[1] = 1
                Player.dir = 1
            elif event.key == pygame.K_UP:
                Player.move[1] = -1
                Player.dir = 3
            elif event.key == pygame.K_SPACE:tir()
            elif event.key == pygame.K_F11:fullscreen()
            elif event.key == pygame.K_F12:screenshoot()
            elif event.key == pygame.K_c:
                try:exec(input("Command : "))
                except:print("Commande inconnue")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                if Player.move[0] == 1:
                    Player.move[0] = 0
                    if Player.move[1]:
                        Player.dir = Player.move[1]%4
            elif event.key == pygame.K_LEFT:
                if Player.move[0] == -1:
                    Player.move[0] = 0
                    if Player.move[1]:
                        Player.dir = Player.move[1]%4
            elif event.key == pygame.K_DOWN:
                if Player.move[1] == 1:
                    Player.move[1] = 0
                    if Player.move[0]:
                        Player.dir = (Player.move[0]-1)%4
            elif event.key == pygame.K_UP:
                if Player.move[1] == -1:
                    Player.move[1] = 0
                    if Player.move[0]:
                        Player.dir = (Player.move[0]-1)%4
        elif event.type == pygame.QUIT: # On clique sur la croix pour quitter
            continuer=False
    
    Refresh()
    if Player.live <= 0:
        pygame.display.quit() # Ferme la fenêtre pygame
        break

if continuer: # On est mort ou c'est juste que l'on a quitté le jeu ?
    # Actions à effectuer après la mort du joueur :
    print("Game Over")
else:
    # Actions à effectuer après avoir quitté le jeu
    pygame.display.quit()
    print("À bientôt :)")
