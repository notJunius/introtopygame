from pygame.image import load
from settings import *
import pygame as pg
from player import Player
from sprites import *
from random import randint
from pytmx.util_pygame import load_pygame
from groups import AllSprites

class Game():
    def __init__(self):
        # setup
        pg.init()
        self.display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption("survivor")
        self.clock = pg.time.Clock()
        self.running = True

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()

        # sprites


    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))

        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pg.Surface((obj.width, obj.height)), (self.all_sprites, self.collision_sprites))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * 64,y * 64), image, self.all_sprites)

        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for marker in map.get_layer_by_name('Entities'):
            if marker.name == "Player":
                self.player = Player((marker.x, marker.y), self.all_sprites, self.collision_sprites)


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
            self.all_sprites.draw(self.player.rect.center)
            pg.display.update()

        pg.quit()





if __name__ == "__main__":
    game = Game()
    game.run()

# left off at 5 01 min 54 seconds, in groups i added a lambda for ysorting, it isn't complete yet.
