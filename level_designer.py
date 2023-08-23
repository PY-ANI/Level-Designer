from designer_app import *

if __name__ == "__main__":
    pygame.init()

    width,height = 1200,650

    win = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Level Designer")
    pygame.display.set_icon(pygame.image.load("icon.ico").convert_alpha())

    clock = pygame.time.Clock()

    app = Designer_App(win,width,height)

    fps = 200

    while not pygame.event.get(pygame.QUIT):

        clock.tick(fps)

        app.draw()

        pygame.display.flip()

    pygame.quit()