from os.path import join
from random import randint, uniform
import pygame
from pygame.sprite import collide_mask

class Player(pygame.sprite.Sprite):
    def __init__(self, groups) -> None:
        super().__init__(groups)
        self.original_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.image = self.original_surf
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 500

        #cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 10

        #mask
        self.mask = pygame.mask.from_surface(self.image)

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
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH

        if pygame.key.get_just_pressed()[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()
        
        self.laser_timer()


class Star(pygame.sprite.Sprite):
    def __init__(self, groups, window_width, window_height, image) -> None:
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(center = (randint(0, window_width), randint(0, window_height)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        self.speed = 600
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rect.centery -= self.speed * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, groups, window_width, window_height):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, window_width), -300))
        self.speed = randint(400, 700)
        self.window_height = window_height
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.rotation = 0
        self.rotation_speed = randint(100,300)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if self.rect.top > self.window_height:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)


class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.current_frame += 20 * dt
        if self.current_frame < len(self.frames):
            self.image = self.frames[int(self.current_frame) % len(self.frames)]
        else:
            self.kill()



# collision function
def collision():
    global running
    global score
    global meteors_destroyed
    if pygame.sprite.spritecollide(player, meteor_sprites, False, pygame.sprite.collide_mask):
        player.kill()
        running = False
    for laser in laser_sprites:
        if pygame.sprite.spritecollide(laser, meteor_sprites, True):
            score += 10
            meteors_destroyed += 1
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()

def display_score(score, display_surface):
    score += pygame.time.get_ticks() // 100
    text_surf = font.render(f'{score}', True, (240, 240, 240))
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, (240,240,240), text_rect.inflate(20, 16).move(0, -8), 5, 5)

def display_meteors(meteors_destroyed, display_surface):
    text_surf = font.render(f'Meteors: {meteors_destroyed}', True, (240, 240, 240))
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2 + 250, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)
    

#general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()
score = 0
meteors_destroyed = 0

#group stuff
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()


#imports
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 30)
explosion_frames = [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]

#sounds
laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
game_music = pygame.mixer.Sound(join('audio', 'game_music.wav'))
damage_sound = pygame.mixer.Sound(join('audio', 'damage.ogg'))


for i in range(20):
    Star(all_sprites, WINDOW_WIDTH, WINDOW_HEIGHT, star_surf)

player = Player(all_sprites)


# custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)


game_music.set_volume(0.1)
game_music.play(loops=-1)

while running:
    #event loop
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surf, (all_sprites, meteor_sprites), WINDOW_WIDTH, WINDOW_HEIGHT)

    #i'm gonna put game logic here

    all_sprites.update(dt)
    collision()

    #draw the game
    display_surface.fill('#3a2e3f')
    all_sprites.draw(display_surface)


    display_score(score, display_surface)
    display_meteors(meteors_destroyed, display_surface)
    pygame.display.update()



pygame.quit()

#Finished
