import random

import pygame.draw

from course import cell_size


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
    def display_ships(self,left,up):

        pos = 0
        while pos < len(self.ships):
            x_pos = left + self.ships[pos].col * cell_size  # x position each ship will be in
            y_pos = up + self.ships[pos].row * cell_size  # y pos each ship will be in
            if self.ships[pos].orientation == "h":
                if self.ships[pos].size == 5:
                    image_tranform = pygame.transform.scale(get_background("5ship"),(self.ships[pos].size * cell_size,cell_size))
                elif self.ships[pos].size == 4:
                    image_tranform = pygame.transform.scale(get_background("4ship"),(self.ships[pos].size * cell_size,cell_size))
                elif self.ships[pos].size == 3:
                    image_tranform = pygame.transform.scale(get_background("3ship"),(self.ships[pos].size * cell_size,cell_size))
                elif self.ships[pos].size == 3:
                    image_tranform = pygame.transform.scale(get_background("32ship"),(self.ships[pos].size * cell_size,cell_size))
                elif self.ships[pos].size == 2:
                    image_tranform = pygame.transform.scale(get_background("2ship"),(self.ships[pos].size * cell_size,cell_size))

            else:
                if self.ships[pos].size == 5:
                    image_tranform = pygame.transform.scale(get_background("5ship"),(cell_size, self.ships[pos].size * cell_size))
                elif self.ships[pos].size == 4:
                    image_tranform = pygame.transform.scale(get_background("4ship"),(cell_size, self.ships[pos].size * cell_size))
                elif self.ships[pos].size == 3:
                    image_tranform = pygame.transform.scale(get_background("3ship"),(cell_size, self.ships[pos].size * cell_size))
                elif self.ships[pos].size == 3:
                    image_tranform = pygame.transform.scale(get_background("32ship"),(cell_size, self.ships[pos].size * cell_size))
                elif self.ships[pos].size == 3:
                    image_tranform = pygame.transform.scale(get_background("2ship"),(cell_size, self.ships[pos].size * cell_size))

            image_tranform.get_rect(center=(x_pos, y_pos))

class Game():
    def __init__(self):
        self.player1 = Player()#user board
        self.player2 = Player()#ai board
        self.player1_turn = True#checks if its the users turn
        self.over = False#checks if the game is over



    def make_move(self, input):
        if self.player1_turn == True:
            player = self.player1
            opponent = self.player2
        else:
            player = self.player2
            opponent = self.player1

        if input in opponent.indexes():
            Player.search[input] = "H"

            for ship in opponent.ships:
                sunk = True
                for i in ship.indexes:
                    if player.search[i] == "U":
                        sunk = False
        else:
            player.search[input] = "M"

