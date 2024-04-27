"""
StartGame creates a main menu window for the player to have the option to play or quit
https://www.pygame.org/docs/ref/mouse.html
https://www.geeksforgeeks.org/creating-start-menu-in-pygame/
https://www.pygame.org/docs/ref/surface.html
https://www.pygame.org/docs/ref/rect.html#pygame.Rect.collidepoint
https://www.pygame.org/docs/ref/font.html#pygame.font.Font.render

"""
import pygame

class StartGame:
    def __init__(self, screen):
        self.screen = screen
        font_name = pygame.font.match_font('dejavusans-regular.ttf') # default font for python
        self.font = pygame.font.Font(font_name, 50) # specific params for font
        self.start_text = self.font.render("Start Game", True, (0, 0, 0)) # render 'start game' text for main menu
        self.quit_text = self.font.render("Quit", True, (0, 0, 0)) # render 'quit' text for main menu
        self.start_rect = self.start_text.get_rect(x=400, y=400) # place text at the location x,y
        self.quit_rect = self.quit_text.get_rect(x=400, y=450) # place text at the location x,y

    def draw(self): # draw() places the elements of the main menu on the screen
        wallpaper = pygame.transform.scale(pygame.image.load("duskysky.jpg"), (1000, 800)) # load and scale the wallpaper
        # blit can draw one image onto another
        self.screen.blit(wallpaper, (0, 0)) # blit wallpaper onto main menu
        self.screen.blit(self.start_text, self.start_rect) # blit 'start' onto main menu
        self.screen.blit(self.quit_text, self.quit_rect) # blit 'quit' onto main menu
        pygame.display.flip() # update the full display surface to the screen

    def game_buttons(self):
        for event in pygame.event.get(): # loop through button options
            if event.type == pygame.QUIT:
                pygame.quit() # quit game if 'quit' is pressed
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN: # check for mouse click for either 'start' or 'quit'
                if self.start_rect.collidepoint(event.pos): # if 'start' is inside the rectangle
                    return "start"
                elif self.quit_rect.collidepoint(event.pos): # if 'quit' is inside the rectangle
                    pygame.quit()
                    quit()
        return None
