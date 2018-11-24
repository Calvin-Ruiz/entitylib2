from entitylib2 import *
mur = Static("default", (128, 16), "bmp")
class obs(Obstacle):
    live=100
    size=(32, 32)

class ent(Entity):
    size=(32, 32)

class ia(IA):
    delay = 1200
    size=(32, 32)

mur.append((-63, -200))
obs((54, 80))
ent((-100, 200))
ia((600, 0))

init((Player, obs, ent, ia), (768, 512))

while True:
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
        elif event.type == pygame.QUIT:
            pygame.display.quit()
    Refresh()
