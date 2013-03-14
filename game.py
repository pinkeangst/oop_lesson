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
        #???IMAGE = "BlueGem"
        IMAGE = "BlueGem"
        SOLID = False

        def interact(self, player):
            #print "Self = %s" % self
            player.inventory.append(self) # append gem total to player.inventory
            GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!"%(len(player.inventory)))
            print "Blue Inventory = %s" % player.inventory


class GreenGem(GameElement):
        IMAGE = "GreenGem"
        SOLID = False
        SPECIAL = False # for magic green gem

        def interact(self, player):

            player.inventory.append(self) # append gem total to player.inventory
            GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!"%(len(player.inventory)))
         
            print "Green Inventory = %s" % player.inventory   

class OrangeGem(GameElement):
        IMAGE = "OrangeGem"
        SOLID = False

        def interact(self, player):

            player.inventory.append(self)
            GAME_BOARD.draw_msg("You acquired a very special gem! Congratulations!")
            print "Inventory = %s" % player.inventory


class Rock(GameElement):
        IMAGE = "Rock"
        SOLID = True

class Character(GameElement):
        def __init__(self):
            GameElement.__init__(self) #call the original init def in GameElement
            self.inventory = []
            self.orangeInventory = []


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

class NonPlayer(Character): #Subclass of Class Character; speak messages when you interact with them.
        def __init__(self):
            Character.__init__(self)
            #self.interact?

        IMAGE = "Boy"
        SOLID = True

        def interact(self, player):
            GAME_BOARD.draw_msg("You're the coolest person I've ever met! I have antennae!!!")

# class Door(GameElement):
#         IMAGE = "Door Tall Closed"
#         SOLID = True



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

    #Elaine added gem_positions 3/13/13
    gem_positions = [
        # Four corners
        (0,0),
        (0,4),
        (4,0),
        (4,4)
    ]
    gems = []
    for pos in gem_positions:
        gem = Gem()
        GAME_BOARD.register(gem)
        GAME_BOARD.set_el(pos[0], pos[1], gem)
        gems.append(gem)

    #Elaine added greengem_positions 3/13/13
    ggem_positions = [
        # Four corners
        (1,4),
        (3,7),
        (2,9),
        (8,6)
    ]
    ggems = []
    for pos in ggem_positions:
        ggem = GreenGem()
        GAME_BOARD.register(ggem)
        GAME_BOARD.set_el(pos[0], pos[1], ggem)
        ggems.append(ggem)


    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2,2, PLAYER)
    print PLAYER

    global NONPLAY # non-characters that interact with other characters by speaking e.g. Boy
    NONPLAY = NonPlayer()
    GAME_BOARD.register(NONPLAY)
    GAME_BOARD.set_el(4,2, NONPLAY)
    print NONPLAY

    global ORANGEGEM # for the special green gem
    ORANGEGEM = OrangeGem()
    GAME_BOARD.register(ORANGEGEM)
    GAME_BOARD.set_el(2,8, ORANGEGEM)
    print ORANGEGEM

    # global DOOR # for the special green gem
    # DOOR = Door()
    # GAME_BOARD.register(DOOR)
    # GAME_BOARD.set_el(8,2, DOOR)
    # print DOOR



    GAME_BOARD.draw_msg("This game is wicked awesome. ")     


def keyboard_handler():
    direction = None
    meetChar = False #Start out not interacting with a nonChar

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

        #Prevents the game from crashing if you go beyond the game board boundaries.
        if next_x < 0 or next_y < 0: 
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

 