#import modules

import numpy as np
import pygame
import sys
import random



#initialise board

pygame.init()# initialising the python modules
pygame.display.set_caption("Tactical Battleships")#Changes the window title to "Tactical Battleships"
screen = pygame.display.set_mode((800,600),0,0) #creates a display surface with the dimensions 800 by 600
cell_size = 35#The size of each cell in the board
h_margin = cell_size * 4 # the horizontal borders of the game table
v_margin = cell_size * 4 # vertical borders of the game table


white = (255,255,255) #Hexadecimal for the brown colour
blue = (0, 59, 115) # rgb blue
red = (255, 0, 0) # rgb red
black = (0,0,0) # rgb black
bblue = (0,0,255) # rgb bllue
gold = (187, 165, 61)
colour =  {"U":white, "H":red,"M":blue,"S":black,"A":gold,"B":bblue} # library of colours
def get_font(font,size):#function that takes allows me to set the font without longer lines of code
    return pygame.font.Font(font,size)# sets font
def get_background(background): #function that sets the background of a rect or screen without longer lines of code
    return pygame.image.load(background)# sets background
def display_board(player, left,up,searching= False):#displays board onto screen
        pos = 0
        while pos <= 99:#loops through each cell of the board
            x_pos = left + pos % 10 * cell_size# x position each cell will be in
            y_pos = up + pos // 10 * cell_size# y pos each cell will be in
            cell = pygame.Rect(x_pos,y_pos,cell_size,cell_size)# creates a rect for each cell
            pygame.draw.rect(screen,blue,cell,width=5)#displays rect onto screen

            if searching:
                centre_x = x_pos +cell_size//2 #finds coord of the centre of a cell
                centre_y = y_pos + cell_size//2 # finds the coord of the centre of a cell
                pygame.draw.circle(screen,colour[player.search[pos]],(centre_x,centre_y), radius = cell_size//4) # creates a circle placed at the centre of each cell


            pos += 1 # increment
def probabilitynextmove(board_with_probabilities):
        return np.unravel_index(board_with_probabilities.argmax(), board_with_probabilities.shape)  #makes the two array numbers into a single index and converts that index into any x,y coordinate

def locationsprobability(board_with_hits, board_with_misses, length_of_the_ship):
    list_of_probabilities = []

    # Check all rows for possible locations
    for row in range(0, 10):
        for col in range(0, 11 - length_of_the_ship):
            positions_to_consider = range(col, col + length_of_the_ship)
            # State where hits happened
            positions_with_hits = []
            empty_slot_counter = 0
            # Check if the elements of a list all correspond to 0s, and if they do create a matrix where that segment has a certain probabiliity
            for element in positions_to_consider:
                if board_with_misses[row, element] == 0:
                    if board_with_hits[row, element] == 1:
                        positions_with_hits.append(element)
                    empty_slot_counter += 1

            # Check if the number of continious empty slots corresponds to the length of the ship
            if empty_slot_counter == length_of_the_ship:
                new_state = np.full((10, 10), 0.0)
                if_there_is_hit = 4 * len(positions_with_hits) if len(positions_with_hits) else 1
                for element in positions_to_consider:
                    if element in positions_with_hits:
                        new_state[row, element] = 0
                    else:
                        new_state[row, element] = float(length_of_the_ship) * if_there_is_hit
                list_of_probabilities.append(new_state)

    # Check all cols for possible locations
    for col in range(0, 10):
        for row in range(0, 11 - length_of_the_ship):
            positions_to_consider = range(row, row + length_of_the_ship)
            positions_with_hits = []
            empty_slot_counter = 0

            # Check if the elements of a list all correspond to 0s, and if they do create a matrix where that segment has a certain probabiliity
            for element in positions_to_consider:
                if board_with_misses[element, col] == 0:
                    if board_with_hits[element, col] == 1:
                        positions_with_hits.append(element)
                    empty_slot_counter += 1

            # Check if the number of continious empty slots corresponds to the length of the ship
            if empty_slot_counter == length_of_the_ship:
                if_there_is_hit = 4 if len(positions_with_hits) else 1

                new_state = np.full((10, 10), 0.0)
                for element in positions_to_consider:
                    if element in positions_with_hits:
                        new_state[element, col] = 0
                    else:
                        new_state[element, col] = float(length_of_the_ship) * if_there_is_hit
                list_of_probabilities.append(new_state)

    final_matrix = np.full((10, 10), 0)
    for curr_matrix in list_of_probabilities:
        final_matrix = np.add(final_matrix, curr_matrix)

    return final_matrix
def probabilitiesforallships(board_with_hits, board_with_misses):
        final = np.full((10, 10), 0) # creates a matrix map
        ships = [5, 4, 3, 3, 2] # stores ships
        for i in ships:
            probabilites = locationsprobability(board_with_hits, board_with_misses, i)# loops through shiops and finds placement possibility
            final = np.add(final, probabilites) # adds the probability value into the matrix
        return final

class Button:
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

    def update(self, sscreen):# function checks if an image is taken in or not
        if self.image is None:
            self.image = self.text
            screen.blit(self.text,self.text_rect) # displays text if there is not image
        elif self.image is not None:
            sscreen.blit(self.image,self.image_rect) #displays image onto button
            sscreen.blit(self.text,self.text_rect) # displays text onto button
    def check_for_input(self, position):#checks if mouse has hovered over text
        if position[0] in range(self.image_rect.left, self.image_rect.right) and position[1] in range(self.image_rect.top, self.image_rect.bottom):#checks if mouse position is within button position
            return True
        else:
            return False
    def hoverchange(self, position):
        if self.check_for_input(position):#Calls previous function to check if mouse position in withing button position
            self.text = self.font.render(self.button_text, True, self.over_colour)#Changes text colour
        else:
            self.text = self.font.render(self.button_text, True, self.base_colour)#text colour stays the same
class Ship:
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
class Ability:
    def __init__(self,type):
        self.type = type # power or double
        self.row = random.randrange(0, 9)  # random y position ship is placed in
        self.col = random.randrange(0, 9)  # random x position ship is placed in
        self.Aindex = self.calc_indexes() # random coordinate on board
    def calc_indexes(self):
        index = self.row * 10 + self.col  #the random board coordinate
        return index

class Player:
    def __init__(self):
        self.ships = []#stores every ship the player has
        self.abilities = []
        self.search = ["U" for _ in range(100)]#u means unknown
        self.sizes = [2,3,3,4,5]#sizes of each ship in the ga,e
        self.place_ships(self.sizes)#places every ship on the board
        self.type_power = ["double", "power"]
        #self.place_ability(self.type)


        listoflist = [ship.indexes  for ship in self.ships] #creats a list with all lists of coordinates
        self.indexes = [index for sublist in listoflist for index in sublist] #separates eahc individual list into separate indexes



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
                if possible_placement:#if all requirements are met
                    self.ships.append(ship)#the ship is added to the board
                    placed = True
    def place_ability(self, type):
        for i in type: #loops twice , double and power
            placed = False # same as ship placing
            while not placed:
                ability = Ability(i) #creates ability object
                possible_placement = True


                for anything in self.ships :
                    if ability.Aindex in anything.indexes : #checks if there are any ships with the same coordinates
                        possible_placement = False
                for anything in self.abilities:
                    if ability.Aindex == anything.Aindex: # checks if there are any abilities with the same coordinate
                        possible_placement = False
                if possible_placement:
                    self.abilities.append(ability) #adds to abilities list
                    self.search[ability.Aindex] = "A" # testing
                    placed = True # ends loop
        self.ability_indexes = [ability.Aindex for ability in self.abilities]# lists of each index of all abilities



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

                elif self.ships[pos].size == 2:
                    image_transform = pygame.transform.scale(get_background("2ship_v.png"),
                                                        (cell_size-20, self.ships[pos].size * cell_size-20))
            if image_transform is not None:
                screen.blit(image_transform, (x_pos, y_pos))

            pos += 1

class Game:
    def __init__(self):
        self.board_hits = np.zeros((10, 10)) # for probability ai, here so it wont reset each call
        self.board_misses = np.zeros((10, 10))# for probability ai, here so it wont reset each call

        self.player = Player()#user board

        self.AI = Player()#ai board
        self.AI.place_ability(self.AI.type_power)
        self.player_turn = True#checks if its the users turn
        self.turn_count = 0
        self.winner = None # Will store the person who has won
        self.game_ongoing = True#checks if the game is still on
        self.power_ability = False #to check if they user clicked an ability
        self.double_ability = False # check if user clicked an ability




    def make_move(self, input):
        if input < 100:# condition needed for ability "power"
            player = self.player if self.player_turn else self.AI #swaps when play_turn is false
            opponent = self.AI if self.player_turn else self.player # swaps when play_turn is ture



            if input in opponent.indexes:

                opponent.search[input] = "H" #hit if input is same as a ship pos

                for ship in opponent.ships: #loops through all their ships
                    sunk = True #condition if all positions of a ship is hit
                    for i in ship.indexes: # each singular ship

                        if opponent.search[i] == "U": # if even one cell is not hit then its not sunk
                            sunk = False
                    if sunk:
                        for i in ship.indexes:
                            opponent.search[i] = "S" # all positions of the ship become S when sunk is true
                for i in opponent.indexes: #every positions of every ship
                    if opponent.search[i] == "S": #checks if every position is sunk or S

                        self.game_ongoing = False # thats person won
                    else:
                        self.game_ongoing = True # if not it breaks the loop keeping game_ongoing false
                        break
            elif hasattr(opponent, 'ability_indexes') and input in opponent.ability_indexes : # hasattr used due to only one player object having ability_indexes
                print("gold") # testing
                opponent.search[input] = "B" # makes the cell with ability turn blue when clicked
                for abilitytype in opponent.abilities: # loops through objects
                    if abilitytype.Aindex == input and abilitytype.type == "double": #checks if the ability is double
                        self.double_ability = True #activates ability
                    elif abilitytype.Aindex == input and abilitytype.type == "power": # checks if ability is power
                        self.power_ability = True #activates ability
                    else:
                        print("idk") # testing


            else: # if not ability or hit


                opponent.search[input] = "M" # miss
                if player == self.player: #swap turns
                    self.player_turn = False #swap turns
                    print("[AI] guessing ") # testing

                else:
                    print("[Move Done] ") # testing
                    self.player_turn = True #swap turns
            if not self.game_ongoing: #win condition
                print("you won") # testing
                if player == self.player: # checks who won
                    self.winner = "player"
                else:
                    self.winner = "AI"

        else:

            return
    def random_ai(self):
         # hit condition loop
        search = self.player.search # stores player board

        unknown_positions = [i for i, square in enumerate(search) if square == "U"] #stores index and whats in the square into a list thats unknown
        if len(unknown_positions) > 0 : #if theres any value in list
            self.make_move(random.choice(unknown_positions)) #make move with random position

    def hunt_ai(self):
        search = self.player.search
        unknown_positions = [i for i, square in enumerate(search) if square == "U" ] #stores index and whats in the square into a list thats unknown
        hit_positions = [i for i,square in enumerate(search) if square == "H"] # #stores index and whats in the square into a list thats hit
        nearby_cells = [] #nearby cells
        nearby_2cells = [] #nearby 2 cells away
        for i in unknown_positions:
            if i+1 in hit_positions or i -1 in hit_positions or i + 10 in hit_positions or i -10 in hit_positions:
                nearby_cells.append(i) #stores nearby cells coord into nearby_cells
            if i+2 in hit_positions or i -2 in hit_positions or i + 20 in hit_positions or i -20 in hit_positions:
                nearby_2cells.append(i) #stores nearby 2 cells coord into nearby_cells
        for i in unknown_positions:
            if i in nearby_cells and i in nearby_2cells: #if a coordinates in both lists
                self.make_move(i) # make move on that coordinate
                return # ends function
        if len(nearby_cells) > 0:
            self.make_move(random.choice(nearby_cells))
            return # ends function



        print("ai:its a hit") # testing
        self.make_move(random.choice(unknown_positions)) #does random pos if no other options work

    def probability_ai(self):

        for i, s in enumerate(self.player.search): #loops through with index and value in the players board
            row, col = divmod(i, 10) # divs eachother and mods eachother
            if s == "H":
                self.board_hits[row, col] = 1 # 1 = hit
                print("hit") # testing
            elif s == "S":
                self.board_hits[row, col] = 1# 1 = hit
                print("hit") # testing
            elif s == "M":
                self.board_misses[row, col] = 2 # 2 = miss
                print("miss") # testing

        probs =probabilitiesforallships(self.board_hits, self.board_misses) # calls function that returns a table with probabilty of ship placement
        probs[self.board_hits == 1] = 0 # debugging

        row, col = probabilitynextmove(probs) # returns next coordinates to make next move on
        idx = row * 10 + col # turns into index
        self.make_move(idx) # make move


class LevelOfDifficulty:#display loop for level of difficulty screen
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
                    if self.back_button.check_for_input(difficult_mousepos):
                        start.menuscreen()#runs main menu screen when back button clicked
                    elif self.easy_button.check_for_input(difficult_mousepos):
                        play.playscreen()#runs game screen when easy button clicked
                    elif self.regular_button.check_for_input(difficult_mousepos):
                        medium.playscreen()
                    elif self.difficult_button.check_for_input(difficult_mousepos):
                        difficult.playscreen()
            pygame.display.update()#allows display to refresh

difficulty = LevelOfDifficulty()#create object of level of difficulty class


class PlayEasy:
    def __init__(self):
        self.back_button = Button(pygame.transform.scale(get_background("button.png"),(70,50)),(35,20),"Exit",get_font("prstart.ttf",15),(240, 255, 255), "red")#button object that allows you to go back from game screen

        self.game = Game()
        self.double_button = Button(pygame.transform.scale(get_background("button.png"), (70, 50)), (400, 450),
                               "Double trouble (Activate)",
                               get_font("prstart.ttf", 5), (240, 255, 255), "red")
        self.power_button = Button(pygame.transform.scale(get_background("button.png"), (70, 50)), (400, 500),
                              "power (Activate)",
                              get_font("prstart.ttf", 5), (240, 255, 255), "red")
        self.restart_button = Button(pygame.transform.scale(get_background("button.png"), (70, 50)), (750, 20), "Restart",
                                  get_font("prstart.ttf", 10), (240, 255, 255), "red")
        self.double_button_activate = False
        self.power_button_activate = False
    def playscreen(self):

        while True:
            screen.blit(pygame.transform.scale(get_background("playbackground.png"), (800, 600)),
                        (0, 0))  # sets background to the display
            play_mouse_pos = pygame.mouse.get_pos()  # holds x, y coordinates of mouse cursor


            ai_title = get_font("prstart.ttf", 10).render("AI's Board", True,
                                                              (240, 255, 255))  # Sets the font of the text and colour
            ai_rect = ai_title.get_rect(center=(200, 30))  # creates a rect to put the text into with specified size
            screen.blit(ai_title, ai_rect)  # displays rect with text onto screen
            display_board(self.game.AI, 25, 50,True)


            player_title = get_font("prstart.ttf", 10).render("your Board", True,
                                                                  (240, 255,
                                                                   255))  # Sets the font of the text and colour
            player_rect = player_title.get_rect(
                    center=(600, 30))  # creates a rect to put the text into with specified size
            screen.blit(player_title, player_rect)  # displays rect with text onto screen
            display_board(self.game.player,(150 + h_margin*2),50,True)
            #self.game.player.display_ships((150+ h_margin*2), 50)

            if self.game.double_ability:  # if true

                self.double_button.hoverchange(play_mouse_pos)  # button can be hovered
                self.double_button.update(screen)  # button will display

            if self.game.power_ability:
                self.power_button.hoverchange(play_mouse_pos)  # button can be hovered
                self.power_button.update(screen)  # button will display
            if not self.game.game_ongoing:
                win_title = get_font("prstart.ttf", 30).render(f"{self.game.winner} has won!", True,
                                                                  (240, 255,
                                                                   255))  # Sets the font of the text and colour
                win_rect = win_title.get_rect(
                    center=(400, 550))  # creates a rect to put the text into with specified size
                screen.blit(win_title, win_rect)


            if self.game.player_turn:
                turn_title = get_font("prstart.ttf", 30).render("your Turn", True,
                                                                  (240, 255,
                                                                   255))  # Sets the font of the text and colour
                turn_title_rect = player_title.get_rect(
                    center=(125, 500))  # creates a rect to put the text into with specified size
                screen.blit(turn_title, turn_title_rect)
            else:
                ai_turn_title = get_font("prstart.ttf", 30).render("AIs Turn", True,
                                                                (240, 255,
                                                                 255))  # Sets the font of the text and colour
                ai_turn_title_rect = player_title.get_rect(
                    center=(550, 500))  # creates a rect to put the text into with specified size
                screen.blit(ai_turn_title, ai_turn_title_rect)




            self.back_button.hoverchange(play_mouse_pos)# changes colour of button text when hovered on
            self.back_button.update(screen)#checks whether button has image or not
            self.restart_button.hoverchange(play_mouse_pos)  # changes colour of button text when hovered on
            self.restart_button.update(screen)  # checks whether button has image or not


            for event in pygame.event.get():#goes through every event in pygame
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()# allows the game to stop running without any problems
                if event.type == pygame.MOUSEBUTTONDOWN:#checks for when you hold down on your mouse
                    if self.back_button.check_for_input(play_mouse_pos):#if mouse cursor is on button
                        start.menuscreen()#runs main menu screen if back button clicked
                        self.game = Game()#resets the game
                    if self.restart_button.check_for_input(play_mouse_pos):
                        self.game = Game()#resets the game
                    if self.power_button.check_for_input(play_mouse_pos): # if you click the power up power
                        self.power_button_activate = True
                        self.game.power_ability = False
                    if self.double_button.check_for_input(play_mouse_pos): # if you click the power up double
                        self.double_button_activate = True
                        self.game.double_ability = False
                    if  self.game.player_turn and self.game.game_ongoing and 25 < play_mouse_pos[
                        0] <= cell_size * 10 + 25 and play_mouse_pos[1] >50 <= play_mouse_pos[1]<= cell_size*10+50:#Check if the click was inside the board range
                            print("in range!")
                            row = (play_mouse_pos[1]-50) // cell_size  # Get row
                            col = (play_mouse_pos[0]-25)  // cell_size  # Get column
                            cell_index = row * 10 + col
                            if self.game.AI.search[cell_index]== "U" or self.game.AI.search[cell_index] == "A": # only places when position is unknown and testing

                                if self.power_button_activate: # if powerup "power"  is active
                                    self.game.player_turn = True
                                    self.game.make_move(cell_index)
                                    self.game.make_move(cell_index+1)
                                    self.game.make_move(cell_index-1)
                                    self.game.make_move(cell_index+10)
                                    self.game.make_move(cell_index-10)
                                    self.power_button_activate = False
                                elif self.double_button_activate: # if double is active
                                    self.game.make_move(cell_index)

                                    self.game.player_turn = True #Stops ai turn
                                    self.double_button_activate = False

                                elif not self.double_button_activate and not self.power_button_activate:# if both power ups not active

                                    self.game.make_move(cell_index)

                            else:# prevent shooting same spot
                                    print("this spot is taken already!!")
            if self.game.game_ongoing and not self.game.player_turn and not self.double_button_activate and not self.power_button_activate:# runs ai if no power ups are active and inot players turn and games ongoing
                self.run_ai() # runs ai functiom
            pygame.display.update()#allows display to refresh
    def run_ai(self):# creates just so i can inherit and override ai
        self.game.random_ai()




play = PlayEasy()#creates object of play class
class Playmedium(PlayEasy): # INHERITENCE
    def run_ai(self): #OVERRIDE
        self.game.hunt_ai()

medium = Playmedium() # object
class Playdifficult(PlayEasy):#INHERITENCE


    def run_ai(self): #OVERRIDE
        print("[AI] single debug shot")
        self.game.probability_ai()
difficult = Playdifficult()# object
class Settings:#class for settings screen
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
                    if self.back_button.check_for_input(setting_mouse_pos):#if mouse cursor is on button
                        start.menuscreen()#runs main menu screen if back button clicked
            pygame.display.update()#allows display to refresh

setting = Settings()#creates object of settings class

class  Mainmenu:
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
                    if self.play_buttons.check_for_input(MOUSEPOS):#if mouse position is on play button
                        difficulty.screen()#show difficulty screen
                    elif self.setting_button.check_for_input(MOUSEPOS):#if mouse position is on settings button
                        setting.settingscreen()#show settings screen
                    elif self.leaderboard_button.check_for_input(MOUSEPOS):#if mouse position is on leaderboard button
                        pass
            pygame.display.update()#allows display to refresh

start = Mainmenu()#creates object of main menu
start.menuscreen()#calls menu screen function of start object which creates a display
