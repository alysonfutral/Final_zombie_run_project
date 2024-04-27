"""
The instructions call for 3 enemies/obstacles.
All enemies have similar positions and collision towards the sprite (player)
https://www.pygame.org/docs/ref/surface.html
https://www.pygame.org/docs/ref/sprite.html
https://www.techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-collision
"""
import pygame
import random


class EnemyTwo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() # call super constructor for pygame.sprite.Sprite
        self.x = x
        self.y = y
        self.speed = 3 # speed of enemy (same for all)
        self.score = 0 # enemies have no score
        self.sprites = [] # array of sprites (enemies) for generating
        for i in range(1, 5): # loop through enemy images during game play
            self.sprites.append(pygame.transform.scale(
                pygame.image.load("zombie2.png"), (75, 75))) # load and size image of sprite
        self.image = random.choice(self.sprites) # random selection for sprite image (looks the same, but spawns in different positions)
        self.rect = self.image.get_rect() # get rectangular area of sprite for collision detection purposes
        self.rect.center = (x, y) # center of enemy rectangular position
        # create hitbox for collision detection
        self.hitbox = pygame.rect.Rect((0, 0), (50, 50)) # hitbox size for collision
        self.hitbox.midbottom = self.rect.midbottom # location of hitbox

    def update(self):
        # obstacle moves to the left and off the screen
        self.x -= self.speed
        # update hitbox position to move with obstacle
        self.hitbox.midbottom = self.rect.midbottom
        self.rect = self.image.get_rect() # get rectangular area of sprite for collision detection purposes
        self.rect.center = (self.x,  self.y) # center of enemy rectangular position
        if self.rect.x <= -10: # if enemy is off the screen, remove sprite from all groups
            self.kill()