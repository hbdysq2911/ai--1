import pygame
from .. import constants as C
pygame.font.init()

class Info:
    def __init__(self, state):
        self.state = state
        self.creat_state_label()

    def creat_state_label(self):
        self.state_label = []
        if self.state == True:
            self.state_label.append((self.create_label('少女聆听中',size=50), (240, 480)))
            
        elif self.state == False:
            self.state_label.append((self.create_label('苏半夏',size=50), (240, 480)))

    def create_label(self, label, size=10, width_scale=1.25, height_scale=1):
        font = pygame.font.SysFont(C.FONT,size)
        label_image = font.render(label, 1, (255,255,255))

        return label_image
    


    def update(self):
        pass

    def draw(self, surface):
        for label in self.state_label:
            surface.blit(label[0], label[1])