from entitylib2 import *
mur = Static("default", (128, 16), "bmp")
class obs(Obstacle):
    live=100
    size=(32, 32)

class ent(Entity):
    killscore=10
    size=(32, 32)

class ia(IA):
    killscore = 10
    delay = 1200
    size=(32, 32)

class arrow(Fired):
    size=(16, 16)
    pcoll=False
    speed=5
    delay=50

#mur.append((-63, -200))
#obs((54, 80))
for a in range(0, 5):
    ent((randint(-1000, 1000), randint(-1000, 1000)))
    ia((randint(-1000, 1000), randint(-1000, 1000)))

class speed(effect):
    name = "speed boost"
    def init_effect(self, entity):
        entity.speed.value = entity.speed.value*(1+self.level/2)
    active_effect=NoWeapon # NoWeapon represent passive function with 2 args
    def end_effect(self, entity):
        entity.speed.value = entity.__class__.speed

init((arrow, obs, ent, ia), (768, 512))
Player.weapon = arrow
Player.apply(speed, 200, 2)

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
    if Player.live.value < 1:
        pygame.display.quit() # Ferme la fenêtre pygame
        break

if continuer: # On est mort ou c'est juste que l'on a quitté le jeu ?
    # Actions à effectuer après la mort du joueur :
    print("Game Over")
else:
    # Actions à effectuer après avoir quitté le jeu
    pygame.display.quit()
    print("À bientôt :)")
