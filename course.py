#coding cassowary
#import modules
#import modules
import pygame
import sys
import random



#initialise board
from pygame.locals import *
pygame.init()# initialising the python modules
pygame.display.set_caption("Tactical Battleships")#Changes the window title to "Tactical Battleships"
screen = pygame.display.set_mode((800,600),0,0) #creates a display surface with the dimensions 800 by 600
cell_size = 50 #The size of each cell in the board
h_margin = cell_size * 4 # the horizontal borders of the game table
v_margin = cell_size * 4 # vertical borders of the game table
brown = (222,184,135) #Hexadecimal for the brown colour
blue = (0, 59, 115)
def get_font(font,size):#function that takes allows me to set the font without longer lines of code
    return pygame.font.Font(font,size)# sets font
def get_background(background): #function that sets the background of a rect or screen without longer lines of code
    return pygame.image.load(background)# sets background
def display_board(player,game, left,up,searching):#displays board onto screen
        pos = 0
        while pos <= 99:#loops through each cell of the board
            x_pos = left + pos % 10 * cell_size# x position each cell will be in
            y_pos = up + pos // 10 * cell_size# y pos each cell will be in
            cell = pygame.Rect(x_pos,y_pos,cell_size,cell_size)# creates a rect for each cell
            pygame.draw.rect(screen,blue,cell,width=5)#displays rect onto screen
            search = False
            while  searching:


            pos += 1

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
class Ship():
    def __init__(self,size_of_ship):
        self.row = random.randrange(0,9)#random y position ship is placed in
        self.col = random.randrange(0, 9)#random x position ship is placed in
        self.size = size_of_ship #the number of cells each ship will take
        self.orientation = random.choice(["h","v"])#whether the ship is placed horizontlly or vertically
        self.indexes = self.calc_indexes()#coordinates of where to place ships on the board depending on orientation and start position

    def calc_indexes(self):
        start_index = self.row * 10 + self.col #where the random board coordinate starts from
        if self.orientation == "h":
            return  [start_index + i for i in range(self.size)]#return coordinates of cells depending on size that goes horizontal
        elif self.orientation == "v":
            return [start_index + i * 10 for i in range(self.size)]#return coordinates of cells depending on size that goes vertical


class Player():
    def __init__(self):
        self.ships = []#stores every ship the player has
        self.search = ["U" for i in range(100)]#u means unknown
        self.sizes = [2,3,3,4,5]#sizes of each ship in the ga,e
        self.place_ships(self.sizes)#places every ship on the board
        listoflist = [ship.indexes for ship in self.ships]
        self.indexes = [index for sublist in listoflist for index in sublist]


    def place_ships(self,sizes):#places ship on the board
        for size in sizes:#loops through every ship
            placed = False
            while not placed:
                ship = Ship(size)#creates a ship object

                possible_placement = True#checks if placement is possible

                for i in ship.indexes:#loops through all indexes of the ship
                    if i >=100 :#indexes cannot be over 100
                        possible_placement = False

                    new_row = i // 10
                    new_col = i % 10

                    if new_col != ship.col and new_row != ship.row:#checks if the ship is placed out of bounds horizontally
                        possible_placement = False

                    for different_ship in self.ships:#loops through ships that player has
                        if i in different_ship.indexes:# checks if there are any collisions with any other ship
                            possible_placement = False
                if possible_placement == True:#if all requirements are met
                    self.ships.append(ship)#the ship is added to the board
                    placed = True

    def display_ships(self, left, up):

        pos = 0
        while pos < len(self.ships):
            x_pos = left + self.ships[pos].col * cell_size+10  # x position each ship will be in
            y_pos = up + self.ships[pos].row * cell_size +10 # y pos each ship will be in
            image_transform = None
            if self.ships[pos].orientation == "h":
                if self.ships[pos].size == 5:
                    image_transform = pygame.transform.scale(get_background("5ship_h.png"),
                                                        (self.ships[pos].size * cell_size-20, cell_size-20))
                elif self.ships[pos].size == 4:
                    image_transform = pygame.transform.scale(get_background("4ship_h.png"),
                                                        (self.ships[pos].size * cell_size-20, cell_size-20))
                elif self.ships[pos].size == 3:
                    image_transform = pygame.transform.scale(get_background("3ship_h.png"),
                                                        (self.ships[pos].size * cell_size-20, cell_size-20))

                elif self.ships[pos].size == 2:
                    image_transform = pygame.transform.scale(get_background("2ship_h.png"),
                                                        (self.ships[pos].size * cell_size-20, cell_size-20))

            else:
                if self.ships[pos].size == 5:
                    image_transform = pygame.transform.scale(get_background("5ship_v.png"),
                                                        (cell_size-20, self.ships[pos].size * cell_size-20))
                elif self.ships[pos].size == 4:
                    image_transform = pygame.transform.scale(get_background("4ship_v.png"),
                                                        (cell_size-20, self.ships[pos].size * cell_size-20))
                elif self.ships[pos].size == 3:
                    image_transform = pygame.transform.scale(get_background("3ship_v.png"),
                                                        (cell_size-20, self.ships[pos].size * cell_size-20))

                elif self.ships[pos].size == 3:
                    image_transform = pygame.transform.scale(get_background("2ship_v.png"),
                                                        (cell_size-20, self.ships[pos].size * cell_size-20))
            if image_transform is not None:
                screen.blit(image_transform, (x_pos, y_pos))

            pos += 1


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
        self.player = Player()
        self.game = Game()
    


    def playscreen(self):

        while True:
            if self.game.player1_turn:
                ai_title = get_font("prstart.ttf", 30).render("AI's Board", True,
                                                              (240, 255, 255))  # Sets the font of the text and colour
                ai_rect = ai_title.get_rect(center=(400, 50))  # creates a rect to put the text into with specified size
                screen.blit(ai_title, ai_rect)  # displays rect with text onto screen
                display_board(self.game.player1, self.game, 50, 50)
            else:
                player_title = get_font("prstart.ttf", 30).render("Players's Board", True,
                                                                  (240, 255,
                                                                   255))  # Sets the font of the text and colour
                player_rect = player_title.get_rect(
                    center=(400, 50))  # creates a rect to put the text into with specified size
                screen.blit(player_title, player_rect)  # displays rect with text onto screen
                display_board(self.game.player2,self.game,50,50)

            screen.blit(pygame.transform.scale(get_background("playbackground.png"),(800,600)),(0,0))#sets background to the display
            display_board(self.game.player1,self.game,50,50)
            self.player.display_ships(50, 50)






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
