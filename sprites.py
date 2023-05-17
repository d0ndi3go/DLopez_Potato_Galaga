import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import randint
from random import randrange

vec = pg.math.Vector2

# player class
class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # these are the properties
        self.game = game
        self.image_orig = pg.transform.scale(game.player_img, (128, 128))
        self.image_orig.set_colorkey(WHITE)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.pos = vec(0, 0)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.cofric = 0.1
        self.canjump = False
        self.last_update = pg.time.get_ticks()
        self.left_key = pg.K_a

    def input(self):
        keystate = pg.key.get_pressed()
        if keystate[pg.K_a]:
            self.acc.y = -PLAYER_ACC
        if keystate[pg.K_d]:
            self.acc.y = PLAYER_ACC

    def update(self):
        self.input()
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos


class Mob(Sprite):
    def __init__(self, width, height, color):
        Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width, self.height))
        self.color = DARK_RED
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(randint(1, 5), 0)
        self.acc = vec(1, 1)

    def inbounds(self):
        if self.rect.x > WIDTH:
            self.vel.x *= -1

    def update(self):
        self.inbounds()
        self.pos.x += self.vel.x
        self.rect.centerx = self.pos.x
        # Limit the mob's movement to the top half of the screen
        if self.rect.bottom > HEIGHT // 2:
            self.rect.bottom = HEIGHT // 2


class Bullet(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load("bullet.png")
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.x -= 5
        if self.rect.bottom < 0:
            self.kill()
    def collide_with_mob(self, mob):
        if pg.sprite.collide_rect(self, mob):
            mob.kill()
            self.kill()


class Scoreboard(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.font = pg.font.Font(None, 50)
        self.color = BLACK
        self.score = 100  # initialize the score to 100
        self.image = self.font.render("Score: {}".format(self.score), True, self.color)
        self.rect = self.image.get_rect()
        self.rect.topright = (WIDTH-10, 10)

    def update(self):
        hits = pg.sprite.spritecollide(self.game.player, self.game.enemies, False) # check for collisions
        if hits:
            self.score -= 1  # decrease the score by 1 if there's a collision
        if self.score < 0:
            self.score = 0 # prevent the score from becoming negative
            self.game.playing = False
            self.game.show_go_screen()
        if self.score != self.game.score: # update the score if it has changed
            self.game.score = self.score
            self.image = self.font.render("Score: {}".format(self.score), True, self.color)
        self.rect.topright = (WIDTH-10, 10)
