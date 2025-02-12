#import modules
import pygame
import sys
import random



#initialise board
from pygame.locals import *
pygame.init()
pygame.display.set_caption("Tactical Battleships")
screen = pygame.display.set_mode((800,600),0,32)
square_size = 30
h_margin = square_size * 4
v_margin = square_size * 4
brown = (222,184,135)
def get_font(font,size):
    return pygame.font.Font(font,size)
def get_background(background): # Returns the desired background
    return pygame.image.load(background)

class Button():
    def __init__(self,image,pos, button_text, font, base_colour, over_colour):
        self.image = image
        self.font = font
        self.base_colour = base_colour
        self.over_colour = over_colour
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.button_text = button_text
        self.text = self.font.render(self.button_text, True, self.base_colour)
        self.image_rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is None:
            self.image = self.text
            screen.blit(self.text,self.text_rect)
        elif self.image is not None:
            screen.blit(self.image,self.image_rect)
            screen.blit(self.text,self.text_rect)
    def checkForInput(self, position):
        if position[0] in range(self.image_rect.left, self.image_rect.right) and position[1] in range(self.image_rect.top, self.image_rect.bottom):
            return True
        else:
            return False
    def hoverchange(self, position):
        if position[0] in range(self.image_rect.left, self.image_rect.right) and position[1] in range(self.image_rect.top, self.image_rect.bottom):
            self.text = self.font.render(self.button_text, True, self.over_colour)
        else:
            self.text = self.font.render(self.button_text, True, self.base_colour)
class level_of_difficulty():
    def __init__(self,back_button, easy_button, regular_button, difficult_button):
        self.back_button = back_button
        self.easy_button = easy_button
        self.regular_button = regular_button
        self.difficult_button = difficult_button

    def screen(self):
        while True:
            screen.fill((240, 255, 255))
            difficult_mousepos = pygame.mouse.get_pos()

            difficulty_title = get_font("prstart.ttf", 25).render("Choose your difficulty!", True,(0, 0, 0) )
            title_rect = difficulty_title.get_rect(center =(400,100))

            screen.blit(difficulty_title,title_rect)
            for button in [self.back_button,self.regular_button,self.easy_button,self.difficult_button]:
                button.hoverchange(difficult_mousepos)
                button.update(screen)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.checkForInput(difficult_mousepos):
                        start.menuscreen()
                    elif self.easy_button.checkForInput(difficult_mousepos):
                        play.playscreen()
                    elif self.regular_button.checkForInput(difficult_mousepos):
                        pass
                    elif self.difficult_button.checkForInput(difficult_mousepos):
                        pass
            pygame.display.update()
easy_button = Button(pygame.transform.scale(get_background("easy.png"),(250,50)),(400,200),"easy",get_font("prstart.ttf",25),(240, 255, 255), "red")
regular_button = Button(pygame.transform.scale(get_background("regular.png"),(250,50)),(400,300),"regular",get_font("prstart.ttf",25),(240, 255, 255), "red")
difficult_button = Button(pygame.transform.scale(get_background("difficult.png"),(250,50)),(400,400),"difficult)",get_font("prstart.ttf",25),(240, 255, 255), "red")
exit_play_button = Button(pygame.transform.scale(get_background("button.png"),(70,50)),(35,20),"Exit",get_font("prstart.ttf",15),(240, 255, 255), "red")
difficulty = level_of_difficulty(exit_play_button,easy_button,regular_button,difficult_button)


class Play_easy():
    def __init__(self,back_button):
        self.back_button = back_button

    def draw_grid(self):
        pos = 0
        while pos < 100:
            x = h_margin + pos % 10 * square_size
            y = v_margin + pos // 10 * square_size
            square = pygame.Rect( x, y, square_size, square_size)
            pygame.draw.rect(screen,brown, square, width = 3)
            pos += 1


    def playscreen(self):
        while True:
            screen.blit(pygame.transform.scale(get_background("playbackground.png"),(800,600)),(0,0))
            self.draw_grid()

            play_mouse_pos = pygame.mouse.get_pos()
            self.back_button.hoverchange(play_mouse_pos)
            self.back_button.update(screen)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.checkForInput(play_mouse_pos):
                        start.menuscreen()
            pygame.display.update()

play = Play_easy(exit_play_button)
class settings():
    def __init__(self,back_button):
        self.back_button = back_button

    def settingscreen(self):
        while True:
            screen.fill((167, 199, 231))

            setting_mouse_pos = pygame.mouse.get_pos()
            self.back_button.hoverchange(setting_mouse_pos)
            self.back_button.update(screen)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.checkForInput(setting_mouse_pos):
                        start.menuscreen()
            pygame.display.update()
setting = settings(exit_play_button)

class Mainmenu():
    def __init__(self, play_button,setting_button,leaderboard_button):
        self.play_buttons = play_button
        self.setting_button = setting_button
        self.leaderboard_button = leaderboard_button
    def menuscreen(self):
        pygame.display.set_caption("menu")
        while True:
            screen.blit(get_background("background.png"),(0,0) )

            MOUSEPOS = pygame.mouse.get_pos()

            menu_title = get_font("prstart.ttf",30).render("Tactical Battleships", True, (240, 255, 255))
            menu_rect = menu_title.get_rect(center=(400,50))

            screen.blit(menu_title,menu_rect)

            for button in [self.play_buttons,self.setting_button,self.leaderboard_button,]:
                button.hoverchange(MOUSEPOS)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_buttons.checkForInput(MOUSEPOS):
                        difficulty.screen()
                    elif self.setting_button.checkForInput(MOUSEPOS):
                        setting.settingscreen()
                    elif self.leaderboard_button.checkForInput(MOUSEPOS):
                        pass
            pygame.display.update()
playbuttons = Button(get_background("button.png"),(400,250),"Play",get_font("prstart.ttf",25),(240, 255, 255), "red")
settingbutton = Button(get_background("button.png"), (400, 350), "Settings", get_font("prstart.ttf",25), (240, 255, 255), "red")
leaderboardbutton = Button(get_background("button.png"), (400, 450), "Leaderboard",get_font("prstart.ttf",25), (240, 255, 255), "red")
class Ship():
    def __init__(self,size_of_ship):
        self.row = random.randrange(0,9)
        self.col = random.randrange(0, 9)
        self.size = size_of_ship
        self.orientation = random.choice(["h","v"])
        self.indexes = self.compute_indexes()

    def compute_indexes(self):
        start_index = self.row * 10 + self.col
        if self.orientation == "h":
            return  [start_index + i for i in range(self.size)]
        elif self.orientation == "v":
            return [start_index + i * 10 for i in range(self.size)]


class Player():
    def __init__(self):
        self.ships = []
        self.search = ["U" for i in range(100)]
        self.sizes = [2,3,3,4,5]
        self.place_ships(self.sizes)
        listoflist = [ship.indexes for ship in self.ships]
        self.indexes = [index for sublist in listoflist for index in sublist]


    def place_ships(self,sizes):
        for size in sizes:
            placed = False
            while not placed:
                ship = Ship(size)

                possible_placement = True

                for i in ship.indexes:
                    if i >=100 :
                        possible_placement = False

                    new_row = i // 10
                    new_col = i % 10

                    if new_col != ship.col and new_row != ship.row:
                        possible_placement = False

                    for different_ship in self.ships:
                        if i in different_ship.indexes():
                            possible_placement = False
                if possible_placement == True:
                    self.ships.append(ship)
                    placed = True
class Game():
    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        self.player1_turn = True
        self.over = False

    def make_move(self, i):
        if self.player1_turn == True:
            player = self.player1
            opponent = self.player2
        else:
            player = self.player2
            opponent = self.player1

        if i in opponent.indexes():
            Player.search[i] = "H"

            for ship in opponent.ships:
                sunk = True
                for i in ship.indexes:
                    if player.search[i] == "U":
                        sunk = False
        else:
            player.search[i] = "M"

start = Mainmenu(playbuttons,settingbutton,leaderboardbutton)
start.menuscreen()
