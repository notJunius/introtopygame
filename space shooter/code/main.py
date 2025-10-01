from os.path import join
from random import randint
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, groups) -> None:
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 500

        #cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 2000

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True



    def update(self, dt) -> None:
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        if pygame.key.get_just_pressed()[pygame.K_SPACE] and self.can_shoot:
            print("fire laser")
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        
        self.laser_timer()


class Star(pygame.sprite.Sprite):
    def __init__(self, groups, window_width, window_height, image) -> None:
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(center = (randint(0, window_width), randint(0, window_height)))


#general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()

#group stuff
all_sprites = pygame.sprite.Group()

star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
for i in range(20):
    Star(all_sprites, WINDOW_WIDTH, WINDOW_HEIGHT, star_surf)

player = Player(all_sprites)


# custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    #event loop
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            print('meteorrrrr')

    #i'm gonna put game logic here

    all_sprites.update(dt)

    #draw the game
    display_surface.fill('darkgray')
    all_sprites.draw(display_surface)
    pygame.display.update()



pygame.quit()

# left off at 2 hr 23 min 18 seconds
