"""
Final Project for CPSC 4970.
This project was similar to a past project created for my coding students in pygame.
Some resources used for this project are provided by coding minds academy.
https://learn.codingminds.academy/apps/academy/courses/63ac6f23db03ad381223a44a
https://www.pygame.org/docs/ref/time.html#pygame.time.Clock
https://www.pygame.org/docs/ref/sprite.html
https://www.techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-collision
https://www.pygame.org/docs/ref/event.html#pygame.event.get
"""
import pygame
from start_game import StartGame 
from player import Player
from enemy_one import EnemyOne
from enemy_two import EnemyTwo
from enemy_three import EnemyThree
from score_board import Score
import random

pygame.init() # initialize pygame
clock = pygame.time.Clock() # create a clock to hold time of game

# create game screen large enough to enjoy game play
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
# initialze a window for display
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# create a main screen transition, the user must press 'start' to begin the game
def start_game():
    menu = StartGame(SCREEN) # create menu instance using startgame class
    while True:
        pressed = menu.game_buttons() 
        if pressed == "start": # if start button is pressed, begin the game
            return
        menu.draw() # draw the screen for the main menu

# display the main menu and begin game play
start_game()

# load wallpaper for game play 
wallpaper = pygame.transform.scale(pygame.image.load("duskysky.jpg"),
                                   (SCREEN_WIDTH, SCREEN_HEIGHT))
wallpaper_init = 0 # initilize position of wallpaper for scrolling purposes

player_group = pygame.sprite.GroupSingle() # group container that holds single sprite (player)
enemy_group = pygame.sprite.Group() # container to hold and manage multiple sprites (enemies)

# objects
player = Player(50, 400) # sprite (player) begins at these coordinates
player_group.add(player) # add in the player sprite
score_text = Score(SCREEN, "000", 50, (0, 0, 0), 500, 25) # holds score for player

# variables for game play
enemy_one_timer = 0 # timer for enemy one
other_enemy_timer = 0 # timer for enemy two and three
# enemy flags set to false for spawning
spawn_Enemy_One = False
# last spawn of enemy time
lastspawn_Enemy_One = 0
spawn_Enemy_Two = False
lastspawn_Enemy_Two = 0
spawn_Enemy_Three = False
lastspawn_Enemy_Three = 0

enemy_one_interval = 1000  # interval for spawning enemy one
other_enemy_interval = 3000 # interval for spawning other enemies 

score = 0 # initlaize a score
passed_enemies = False # set flag to false for passing enemies


# collsion detection using colliderect to detect rectangles colliding
def collided(sprite, other):
    return sprite.hitbox.colliderect(other.hitbox)

# if game over, print message, and quit game
def game_over():
    print("The zombies are stuffed, try again?")
    pygame.quit()
    quit()

# if game won, print message, and quit game
def win():
    print("You escaped!")
    pygame.quit()
    quit()

# https://github.com/search?q=pygame.event.get+language%3APython&type=Code&l=Python
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # if quitting the game
            pygame.display.quit() # close display
            pygame.quit() # quit game
            quit()

    # screen scroll
    scroll_wallpaper = wallpaper_init % wallpaper.get_rect().width # coordinate for scrolling
    SCREEN.blit(wallpaper, (scroll_wallpaper - wallpaper.get_rect().width, 0)) # blit the wallpaper to the screen
    if scroll_wallpaper < SCREEN_WIDTH: # while moving, if there is more space for the wallpaper
        SCREEN.blit(wallpaper, (scroll_wallpaper, 0)) # place the wallpaper to the right to fill in as the screen scrolls
    wallpaper_init -= 1 # scroll left

    # increment score every time player jumps over enemy_obstacle
    if len(enemy_group) > 0:
        if enemy_group.sprites()[0].rect.left >= player_group.sprite.rect.left \
                and enemy_group.sprites()[0].rect.right <= player_group.sprite.rect.right \
                and not passed_enemies: # if player is jumping over enemies without collision, update score
            passed_enemies = True # update
        if passed_enemies: # after passing enemies without collsions, increment score
            score += 1
            score_text.text = str(score) # convert to string for proper text
            passed_enemies = False

    # update score text
    score_text.write()

    # check for collisions using spritecollide()
    if pygame.sprite.spritecollide(player_group.sprite, enemy_group, False, collided):
        score -= 1 # after colliding with enemies, decrement score
        score_text.text = str(score)  # convert to string for proper text
        passed_enemies = False

    # if score is >= to 300, you win, if -100, you lose
    if score >= 300:
        win()
    if score == -100:
        game_over()

    # spawn enemies every 0.3-3 seconds using get_ticks()
    if pygame.time.get_ticks() - enemy_one_timer >= enemy_one_interval and pygame.time.get_ticks() - lastspawn_Enemy_Two >= 1000:
        spawn_Enemy_One = True
        enemy_one_interval = random.randint(300, 3000)

    # spawn enemies every 0.5-3 seconds
    if pygame.time.get_ticks() - other_enemy_timer >= other_enemy_interval and pygame.time.get_ticks() - lastspawn_Enemy_One >= 1000:
        spawn_Enemy_Two = True
        other_enemy_interval = random.randint(500, 3000)

    # spawn enemies every 0.7-3 seconds
    if pygame.time.get_ticks() - other_enemy_timer >= other_enemy_interval and pygame.time.get_ticks() - lastspawn_Enemy_Three >= 1000:
        spawn_Enemy_Three = True
        other_enemy_interval = random.randint(700, 3000)


    # all spawned enemies are position at the same y axis to help with collision and successful jumping
    if spawn_Enemy_One:
        enemy_obstacle = EnemyOne(SCREEN_WIDTH, 415)
        enemy_group.add(enemy_obstacle) # add enemy to group of enemies
        enemy_one_timer = pygame.time.get_ticks() # get the time for each enemy
        lastspawn_Enemy_One = enemy_one_timer
        spawn_Enemy_One = False

    if spawn_Enemy_Two:
        enemy_obstacle = EnemyTwo(SCREEN_WIDTH, 415)
        enemy_group.add(enemy_obstacle) # add enemy to group of enemies
        other_enemy_timer = pygame.time.get_ticks() # get the time for each enemy 
        lastspawn_Enemy_Two = other_enemy_timer
        spawn_Enemy_Two = False

    if spawn_Enemy_Three:
        enemy_obstacle = EnemyThree(SCREEN_WIDTH, 415)
        enemy_group.add(enemy_obstacle) # add enemy to group of enemies
        other_enemy_timer = pygame.time.get_ticks() # get the time for each enemy
        lastspawn_Enemy_Three = other_enemy_timer
        spawn_Enemy_Three = False

    # https://docs.python.org/3/library/stdtypes.html#dict.update
    # draw player on the screen
    player_group.draw(SCREEN)
    player.animated() # animate character as game plays
    player_group.update(0.5) # adjusting/updating sprite speed

    # draw enemy_obstacles on the screen
    enemy_group.draw(SCREEN)
    enemy_group.update() # adjusting/updating sprite speed

    clock.tick(60) # run the display at 60 frames per second for smooth performance
    pygame.display.update() # update display
