import pygame
import os


class Game:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.keys = pygame.key.get_pressed()

    def run(self,state):
        while True:
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            state.update(self.screen, events, mouse_pos)
            
            pygame.display.update()
            self.clock.tick(60)

def load_graphics(path,accept=('.jpg','.png','.gif','.bmp')):
    graphics={}
    for pic in os.listdir(path):
        name,ext=os.path.splitext(pic)
        if ext.lower() in accept:
            img=pygame.image.load(os.path.join(path,pic))
            graphics[name]=img
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
            graphics[name]=img
    return graphics

def get_image(sheet,x,y,width,height,colorkey,scale):
    image=pygame.Surface((width,height))
    image.blit(sheet,(0,0),(x,y,width,height))
    image.set_colorkey(colorkey)
    image=pygame.transform.scale(image,(int(width*scale),int(height*scale)))
    return image
