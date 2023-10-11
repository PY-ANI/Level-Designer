from level_designer_dtype import *

def drawwin(pipe):
    pygame.init()

    win = pygame.display.set_mode((500,600))

    f = pygame.font.SysFont("comicsans",20,True)

    coords = pipe.recv()

    while not pygame.event.get(pygame.QUIT):
        
        win.fill((0,0,0))

        if coords.__len__() >= 2: pygame.draw.lines(win, (200,200,200), False, coords, 2)

        win.blit(f.render(f"{coords.__len__()}",True,(200,200,255)),(0,0))

        pygame.display.update()

    pygame.quit()