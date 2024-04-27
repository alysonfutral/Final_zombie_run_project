"""
The sprite (player) class is used to position the player, allow actions (jump) and collision
https://www.techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-collision
https://forum.freecodecamp.org/t/hitbox-and-collision-pygame/665791
https://www.pygame.org/docs/ref/rect.html
"""

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # var below determines position and movement of player
        self.x = x
        self.y = y
        self.animate = False # animating is set to false
        self.jumping = False # jumping is set to false
        self.grounded = 315 # player is grounded at this y-axis
        self.gravity = 0.5 # player gravity to have successful jumping
        self.jump_cap = 15 # jump height set to 15 to allow for jumping over enemies
        self.jump_power = self.jump_cap # jump power
        self.sprites = []  # array of sprite (player) images
        # append 8 sprite images into array of sprites
        for i in range(1, 9):
            # load, flip image, and scale to fit screen
            self.sprites.append(pygame.transform.scale(pygame.transform.flip(
                pygame.image.load("rickgrimes.png"), False, False), (100, 150)))
        self.current_sprite = 0 # count for sprites being displayed
        self.image = self.sprites[self.current_sprite] # initial image for sprite
        self.rect = self.image.get_rect() # position holding sprite
        self.rect.center = (self.x, self.y) # center position for holding sprite
        # create hitbox for collision detection
        self.hitbox = pygame.rect.Rect((0, 0), (50, 50))  # hitbox size is relavent to take collision from enemies
        self.hitbox.midbottom = self.rect.midbottom #collision location is in the bottom center location of the sprite

    def animated(self): # allows animation from sprite
        self.animate = True

    def update(self, sprite_animation): # update sprite as the game play continues
        if self.animate:
            # if animation is occureing increment the sprite
            self.current_sprite += sprite_animation
            # if reach end of the array start from first sprite
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0 # after reaching the end of the array for the sprite, start over
                self.animate = False

        # set sprite image
        self.image = self.sprites[int(self.current_sprite)] # update sprite image
        self.jump() # call jump method for jump access for sprite

    def jump(self):
        keystate = pygame.key.get_pressed() # get the state of all keyboard buttons

        if not self.jumping and keystate[pygame.K_SPACE]: # k_space toggles space bar for use in game
            self.jumping = True # A True value means that the button is pressed.

        # avoid player from double jumping, must be touching ground to jump again
        if self.jumping:
            self.rect.y -= self.jump_power # update sprite position with jump_power
            self.hitbox.midbottom = self.rect.midbottom # hitbox (midbottom) will update as the sprite moves
            self.rect.y += self.gravity # gravity allows the sprite to not float off the screen after jumping
            self.jump_power -= self.gravity # decrease the jump power for the next frame
            if self.rect.y >= self.grounded: # if the sprite is on the ground
                self.jumping = False # disable jump
                self.jump_power = self.jump_cap # update jump_power

    def collided(self, enemy_obstacle): # check collision of enemy_obstacle
        return self.hitbox.colliderect(enemy_obstacle.rect) # return collision if either rectangles hitbox intersect