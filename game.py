import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 10
GAME_HEIGHT = 10

#### Put class definitions here ####
class Gem(GameElement):
        #IMAGE = "BlueGem"
        SOLID = False

        def interact(self, player):
            print "Self = %s" % self
            player.inventory.append(self) # append gem total to player.inventory
            GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!"%(len(player.inventory)))

class Rock(GameElement):
        IMAGE = "Rock"
        SOLID = True

class Character(GameElement):
        def __init__(self):
            GameElement.__init__(self) #call the original init def in GameElement
            self.inventory = []

            #player.inventory.append(gem)


        IMAGE = "Girl"

        def next_pos(self, direction):
            if direction == "up":
                return (self.x, self.y-1)
            elif direction == "down":
                return (self.x, self.y+1)
            elif direction == "left":
                return (self.x -1, self.y)
            elif direction == "right":
                return (self.x+1, self.y)
            return None
####   End class definitions    ####

def initialize():
    """Put game initialization code here"""

    rock_positions = [
        #Diamond 
    	(2, 1),
    	(1, 2),
    	(3, 2),
    	(2, 3), # end of diamond
     #    # Four corners
     #    (0,0),
     #    (0,4),
     #    (4,0),
    	# (4,4)
    ]

    rocks = []
    for pos in rock_positions:
    	rock = Rock()
    	GAME_BOARD.register(rock)
    	GAME_BOARD.set_el(pos[0], pos[1], rock)
    	rocks.append(rock)

    rocks[-1].SOLID = False

    for rock in rocks:
    	print rock


    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2,2, PLAYER)
    print PLAYER

    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3, 1, gem).IMAGE(BlueGem) 
    GAME_BOARD.set_el(7, 5, gem).IMAGE(GreenGem) 

    GAME_BOARD.draw_msg("This game is wicked awesome.")     


def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"        
    elif KEYBOARD[key.DOWN]:        
        direction = "down"
    elif KEYBOARD[key.LEFT]:
        direction = "left"
    elif KEYBOARD[key.RIGHT]:
        direction = "right"

    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        if next_x < 0 or next_y < 0: #doesn't crash when you go beyond the game board boundaries.
            return
        elif next_x > 9 or next_y > 9:
            return

        existing_el = GAME_BOARD.get_el(next_x, next_y)
    
        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)



    #add after this line
        if existing_el:
            existing_el.interact(PLAYER)

 