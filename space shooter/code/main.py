from os.path import join
from random import randint
import pygame
from pygame.mixer_music import play

#general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()

#player stuff
player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
player_direction = pygame.Vector2(0, 0)
player_speed = 300

#star stuff
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
stars = []

#meteor stuff
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
meteor_direction = pygame.Vector2(1, -1)
meteor_speed = 20


#laser stuff
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20, WINDOW_HEIGHT - 20))

for i in range(20):
    x = randint(0, WINDOW_WIDTH)
    y = randint(0, WINDOW_HEIGHT)
    stars.append(pygame.Vector2(x, y))

while running:
    #event loop
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #i'm gonna put game logic here

    #this is gonna be where i get input
    keys = pygame.key.get_pressed()
    player_direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
    player_direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
    #normalize speed up and down
    player_direction = player_direction.normalize() if player_direction else player_direction

    if pygame.key.get_just_pressed()[pygame.K_SPACE]:
        print("fire laser")


    player_rect.center += player_direction * player_speed * dt

    #meteor movement logic
    meteor_rect.center += meteor_direction * meteor_speed
    if meteor_rect.right >= WINDOW_WIDTH or meteor_rect.left <= 0:
        meteor_direction.x *= -1
    elif meteor_rect.top <= 0 or meteor_rect.bottom >= WINDOW_HEIGHT:
        meteor_direction.y *= -1


    #draw the game
    display_surface.fill('darkgray')
    for star in stars:
        display_surface.blit(star_surf, star)
    display_surface.blit(meteor_surf, meteor_rect)
    display_surface.blit(laser_surf, laser_rect)
    display_surface.blit(player_surf, player_rect)

    pygame.display.update()



pygame.quit()

# left off at 1 hr 54 min 28 seconds
