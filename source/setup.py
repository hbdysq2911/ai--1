import pygame
from . import constants as c
from . import tools
import os


pygame.init()
os.environ['SDL_IME_SHOW_UI'] = "1"
SCREEN=pygame.display.set_mode((c.SCREEN_W, c.SCREEN_H))
GRAPHICS=tools.load_graphics('resource\sbx_main')
MUSIC_FILE=os.path.join('resource\\bgm','08. 非日常部.mp3')
pygame.mixer.music.load(MUSIC_FILE)
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)



