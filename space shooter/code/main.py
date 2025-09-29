from os.path import join
from random import randint
import pygame

#general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True

player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
player_pos = pygame.Vector2(50, 100)
player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
stars = []

meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20, WINDOW_HEIGHT - 20))

player_speed = 0.2
for i in range(20):
    x = randint(0, WINDOW_WIDTH)
    y = randint(0, WINDOW_HEIGHT)
    stars.append(pygame.Vector2(x, y))

while running:
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #i'm gonna put game logic here
    player_rect.centerx += player_speed
    if player_rect.right >= WINDOW_WIDTH:
        player_speed *= -1
    elif player_rect.left <= 0:
        player_speed *= -1


    #draw the game
    display_surface.fill('darkgray')
    for star in stars:
        display_surface.blit(star_surf, star)
    display_surface.blit(meteor_surf, meteor_rect)
    display_surface.blit(laser_surf, laser_rect)
    display_surface.blit(player_surf, player_rect)

    pygame.display.update()



pygame.quit()

# left off at 1 hr 4 min 18 seconds
