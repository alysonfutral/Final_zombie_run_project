"""
Score Board for Zombie Game
https://www.pygame.org/docs/ref/font.html#pygame.font.Font.render
https://www.pygame.org/docs/ref/rect.html
"""

import pygame

class Score():
    def __init__(self, surface, text, size, color, x, y):
        font_name = pygame.font.match_font('dejavusans-regular.ttf') # use python default font
        self.surface = surface
        self.text = text
        self.size = size
        self.font = pygame.font.Font(font_name, self.size) # specify font and size
        self.color = color
        self.x = x
        self.y = y

    def write(self):
        text_surface = self.font.render(self.text, True, self.color) # render font, use antialias to clear up pixeled font, and update color
        text_rect = text_surface.get_rect() # get rectangular area of text surface
        text_rect.midtop = (self.x, self.y) # align text with midtop of page
        self.surface.blit(text_surface, text_rect) # blit the text onto the screen