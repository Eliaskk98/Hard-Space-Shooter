import pygame
from os import path
import random

img_dir = path.join(path.dirname(__file__), "img_p2")
sound_dir = path.join(path.dirname(__file__), "sound_p2")
WIDTH = 480
HEIGHT = 600
FPS = 60

#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)


# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Shooter Game")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Space Shooter", 30, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "A - D move, Space to fire", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen,"Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, percent):
    if percent < 0:
        percent = 0
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (percent / 100) * BAR_LENGHT
    outline_rect = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, BLUE, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (60, 55))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 10
        
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = - 8

    def update(self):
        self.rect.y += self.speedy
        # kill if moves off the screen
        if self.rect.bottom < 0:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (60, 55))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 20
        
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT  - 10
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -5
        if keystate[pygame.K_d]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mob_img, (60, 55))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 12
        
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-90, -30)
        self.speedy = random.randrange(6, 7)
        self.rect.y = random.randrange(-90, -30)
        self.speedy = random.randrange(6, 7)
        self.speedx = random.randrange(-2, 2)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -20 or self.rect.right > WIDTH:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-90, -30)
            self.speedy = random.randrange(6, 7)

class Expl(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anime[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anime[self.size]):
                 self.kill()
            else:
                center = self.rect.center
                self.image = expl_anime[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
# load game graphis
background = pygame.image.load(path.join(img_dir, "stars.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "Ship6.png")).convert()
player_min_img = pygame.transform.scale(player_img, (29, 20))
player_min_img.set_colorkey(WHITE)
mob_img = pygame.image.load(path.join(img_dir, "Ship2.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "shot6_2.png")).convert()
expl_anime = {}
expl_anime['big'] = []
expl_anime['small'] = []
expl_anime['player'] = []
for i in range(11):
    filename =  'Explosion1_{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(WHITE)
    img_bg = pygame.transform.scale(img, (75, 75))
    expl_anime['big'].append(img_bg)
    img_sm = pygame.transform.scale(img, (32, 32))
    expl_anime['small'].append(img_sm)
    filename = 'Ship6_Explosion_0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(WHITE)
    img_pl = pygame.transform.scale(img, (80, 70))
    expl_anime['player'].append(img_pl)


# GAME sound
shoot_sound = pygame.mixer.Sound(path.join(sound_dir, "Laser_Shoot8.wav"))
shoot_sound.set_volume(0.2)
expl_sound = pygame.mixer.Sound(path.join(sound_dir, "Explosion12.wav"))
expl_sound.set_volume(0.2)
pygame.mixer.music.load(path.join(sound_dir, "through space.ogg"))
pygame.mixer.music.set_volume(1)



pygame.mixer.music.play(loops=-1)

# Game Loop
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(7):
            newmob()

        score = 0
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input(events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()
    # check to see if bullet hit mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True, pygame.sprite.collide_circle)
    for hit in hits:
        score += 1
        expl_sound.play()
        expl = Expl(hit.rect.center, 'big')
        all_sprites.add(expl)
        newmob()

    # check if mob hit Player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 50
        expl = Expl(hit.rect.center, 'small')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0 :
          expl_sound.play()
          death_explosion = Expl(player.rect.center, 'player')
          all_sprites.add(death_explosion)
          player.hide()
          player.lives -= 1
          player.shield = 100

    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    # Draw
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 30 , WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 90, 5, player.lives, player_min_img)

    # flip after draw everything
    pygame.display.flip()

pygame.quit()
