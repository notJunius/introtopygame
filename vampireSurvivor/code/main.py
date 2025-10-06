from settings import *
import pygame as pg
from player import Player
from sprites import *
from random import randint

class Game():
    def __init__(self):
        # setup
        pg.init()
        self.display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption("survivor")
        self.clock = pg.time.Clock()
        self.running = True

        # groups
        self.all_sprites = pg.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # sprites
        self.player = Player((400, 300), self.all_sprites, self.collision_sprites)
        for i in range(6):
            CollisionSprite((randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)), (100, 100), (self.all_sprites, self.collision_sprites))

    def run(self):
        while self.running:
            #dt
            dt = self.clock.tick() / 1000

            # event loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            #update
            self.all_sprites.update(dt)

            #draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.display_surface)
            pg.display.update()

        pg.quit()



if __name__ == "__main__":
    game = Game()
    game.run()

# left off at 4 14 min 22 seconds, but i went ahead and finished all directions of player collision
