#import modules
import pygame
import sys
import random



#initialise board
from pygame.locals import *
pygame.init()# initialising the python modules
pygame.display.set_caption("Tactical Battleships")#Changes the window title to "Tactical Battleships"
screen = pygame.display.set_mode((800,600),0,0) #creates a display surface with the dimensions 800 by 600
square_size = 30 #The size of each cell in the board
h_margin = square_size * 4 # the horizontal borders of the game table
v_margin = square_size * 4 # vertical borders of the game table
brown = (222,184,135) #Hexadecimal for the brown colour
def get_font(font,size):#function that takes allows me to set the font without longer lines of code
    return pygame.font.Font(font,size)# sets font
def get_background(background): #function that sets the background of a rect or screen without longer lines of code
    return pygame.image.load(background)# sets background

class Button():
    def __init__(self,image,pos, button_text, font, base_colour, over_colour):#constructor that initialises parameters that are the characteristics of the button
        self.image = image
        self.font = font
        self.base_colour = base_colour #normal colour of button text
        self.over_colour = over_colour # colour of text when hovered over
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.button_text = button_text
        self.text = self.font.render(self.button_text, True, self.base_colour)
        self.image_rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):# function checks if an image is taken in or not
        if self.image is None:
            self.image = self.text
            screen.blit(self.text,self.text_rect) # displays text if there is not image
        elif self.image is not None:
            screen.blit(self.image,self.image_rect) #displays image onto button
            screen.blit(self.text,self.text_rect) # displays text onto button
    def checkForInput(self, position):#checks if mouse has hovered over text
        if position[0] in range(self.image_rect.left, self.image_rect.right) and position[1] in range(self.image_rect.top, self.image_rect.bottom):#checks if mouse position is within button position
            return True
        else:
            return False
    def hoverchange(self, position):
        if self.checkForInput(position):#Calls previous function to check if mouse position in withing button position
            self.text = self.font.render(self.button_text, True, self.over_colour)#Changes text colour
        else:
            self.text = self.font.render(self.button_text, True, self.base_colour)#text colour stays the same
class level_of_difficulty():#display loop for level of difficulty screen
    def __init__(self):
        self.back_button = Button(pygame.transform.scale(get_background("button.png"),(70,50)),(35,20),"Exit",get_font("prstart.ttf",15),(240, 255, 255), "red") # object of button that allows you to exit to main menu
        self.easy_button = Button(pygame.transform.scale(get_background("easy.png"),(250,50)),(400,200),"easy",get_font("prstart.ttf",25),(240, 255, 255), "red")# Object that will move to play screen
        self.regular_button = Button(pygame.transform.scale(get_background("regular.png"),(250,50)),(400,300),"regular",get_font("prstart.ttf",25),(240, 255, 255), "red")# Object that will move to play screen
        self.difficult_button = Button(pygame.transform.scale(get_background("difficult.png"),(250,50)),(400,400),"difficult)",get_font("prstart.ttf",25),(240, 255, 255), "red")# Object that will move to play screen

    def screen(self):
        while True:
            screen.fill((240, 255, 255))#sets the colour of the display to light blue
            difficult_mousepos = pygame.mouse.get_pos() #return both y and x coordinated of your mouse cursor

            difficulty_title = get_font("prstart.ttf", 25).render("Choose your difficulty!", True,(0, 0, 0) )#text with desired font
            title_rect = difficulty_title.get_rect(center =(400,100))#creates a rectangle for the text

            screen.blit(difficulty_title,title_rect) # displays the text onto the screen
            for button in [self.back_button,self.regular_button,self.easy_button,self.difficult_button]:#loops through button objects
                button.hoverchange(difficult_mousepos)#allows text inside button to change colour when you hover
                button.update(screen)#checks for image and text


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() # allows the game to stop running without any problems
                if event.type == pygame.MOUSEBUTTONDOWN:#checks for when you hold down on your mouse
                    if self.back_button.checkForInput(difficult_mousepos):
                        start.menuscreen()#runs main menu screen when back button clicked
                    elif self.easy_button.checkForInput(difficult_mousepos):
                        play.playscreen()#runs game screen when easy button clicked
                    elif self.regular_button.checkForInput(difficult_mousepos):
                        pass
                    elif self.difficult_button.checkForInput(difficult_mousepos):
                        pass
            pygame.display.update()#allows display to refresh

difficulty = level_of_difficulty()#create object of level of difficulty class


class Play_easy():
    def __init__(self):
        self.back_button = Button(pygame.transform.scale(get_background("button.png"),(70,50)),(35,20),"Exit",get_font("prstart.ttf",15),(240, 255, 255), "red")#button object that allows you to go back from game screen

    


    def playscreen(self):
        while True:
            screen.blit(pygame.transform.scale(get_background("playbackground.png"),(800,600)),(0,0))#sets background to the display
            #self.draw_grid()

            play_mouse_pos = pygame.mouse.get_pos()#holds x, y coordinates of mouse cursor
            self.back_button.hoverchange(play_mouse_pos)# changes colour of button text when hovered on
            self.back_button.update(screen)#checks whether button has image or not


            for event in pygame.event.get():#goes through every event in pygame
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()# allows the game to stop running without any problems
                if event.type == pygame.MOUSEBUTTONDOWN:#checks for when you hold down on your mouse
                    if self.back_button.checkForInput(play_mouse_pos):#if mouse cursor is on button
                        start.menuscreen()#runs main menu screen if back button clicked
            pygame.display.update()#allows display to refresh

play = Play_easy()#creates object of play class
class settings():#class for settings screen
    def __init__(self):
        self.back_button = Button(pygame.transform.scale(get_background("button.png"),(70,50)),(35,20),"Exit",get_font("prstart.ttf",15),(240, 255, 255), "red")#button object that allows you to go back from game screen

    def settingscreen(self):
        while True:
            screen.fill((167, 199, 231))#sets colour of the screen to light blue

            setting_mouse_pos = pygame.mouse.get_pos()#return both y and x coordinated of your mouse cursor
            self.back_button.hoverchange(setting_mouse_pos)# changes colour of button text when hovered on
            self.back_button.update(screen)#checks whether button has image or not


            for event in pygame.event.get():#goes through every event in pygame
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()# allows the game to stop running without any problems
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.checkForInput(setting_mouse_pos):#if mouse cursor is on button
                        start.menuscreen()#runs main menu screen if back button clicked
            pygame.display.update()#allows display to refresh

setting = settings()#creates object of settings class

class Mainmenu():
    def __init__(self):
        self.play_buttons = Button(get_background("button.png"),(400,250),"Play",get_font("prstart.ttf",25),(240, 255, 255), "red")#object of button class that allows you to move to choose difficulty screen

        self.setting_button = Button(get_background("button.png"), (400, 350), "Settings", get_font("prstart.ttf",25), (240, 255, 255), "red")#object of button class that move you to settings screen
        self.leaderboard_button = Button(get_background("button.png"), (400, 450), "Leaderboard",get_font("prstart.ttf",25), (240, 255, 255), "red")#object of button class that move you to the leaderboard screen
    def menuscreen(self):
        pygame.display.set_caption("menu")#sets caption of the window to menu
        while True:#will always run
            screen.blit(get_background("background.png"),(0,0) )#sets the background of screen to picture

            MOUSEPOS = pygame.mouse.get_pos()#return both y and x coordinated of your mouse cursor

            menu_title = get_font("prstart.ttf",30).render("Tactical Battleships", True, (240, 255, 255))#Sets the font of the text and colour
            menu_rect = menu_title.get_rect(center=(400,50))#creates a rect to put the text into with specified size

            screen.blit(menu_title,menu_rect)#displays rect with text onto screen

            for button in [self.play_buttons,self.setting_button,self.leaderboard_button,]:#loops through button objects
                button.hoverchange(MOUSEPOS)#allows all object to change colour when hovered on
                button.update(screen)#check if all object have images and displays button onto screen

            for event in pygame.event.get():#goes through every event in pygame
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()# allows the game to stop running without any problems
                if event.type == pygame.MOUSEBUTTONDOWN:#checks for when you hold down on your mouse
                    if self.play_buttons.checkForInput(MOUSEPOS):#if mouse position is on play button
                        difficulty.screen()#show difficulty screen
                    elif self.setting_button.checkForInput(MOUSEPOS):#if mouse position is on settings button
                        setting.settingscreen()#show settings screen
                    elif self.leaderboard_button.checkForInput(MOUSEPOS):#if mouse position is on leaderboard button
                        pass
            pygame.display.update()#allows display to refresh

start = Mainmenu()#creates object of main menu
start.menuscreen()#calls menu screen function of start object which creates a display
