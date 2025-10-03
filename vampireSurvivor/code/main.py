from settings import *
import pygame as pg

class Game():
    def __init__(self):
        pg.init()
        self.display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption("survivor")
        self.clock = pg.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            #dt
            dt = self.clock.tick() / 1000

            # event loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            #draw

            #update
            pg.display.update()
            self.display_surface.fill('black')
        pg.quit()



if __name__ == "__main__":
    game = Game()
    game.run()

# left off at 3 hr 51 min 13 seconds
