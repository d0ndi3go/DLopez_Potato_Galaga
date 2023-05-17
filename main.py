# this file was created by diego 

import pygame as pg
import os
from settings import *
from sprites import *
from math import *
from math import ceil
from os import path

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "images")
snd_folder = os.path.join(game_folder, "sounds")

# create game class in order to pass properties to the sprites file

class Game:
    def __init__(self):
        # init game window etc.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Potato Galaga")
        self.clock = pg.time.Clock()
        self.running = True
        print(self.screen)
    
    def load_data(self):
        self.player_img = pg.image.load(path.join(img_folder, "potato.jpg")).convert()

    def new(self):
        # starting a new game
        self.score = 0
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        
        self.scoreboard = Scoreboard(self)
        self.all_sprites.add(self.scoreboard)


    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                # Space key is pressed, create a bullet and add it to the game
                bullet = Bullet()
                self.bullets.append(bullet)


    def draw(self):
        self.screen.fill(BLACK)
        self.draw_text("a and d to move space to shoot.", 24, WHITE, WIDTH/2, HEIGHT/2)
        self.all_sprites.draw(self.screen)

        # is this a method or a function?
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def get_mouse_now(self):
        x,y = pg.mouse.get_pos()
        return (x,y)

# instantiate the game class...
g = Game()

# kick off the game loop
while g.running:
    g.new()

pg.quit()