import pygame as pg

# Screen resolution
width = 1080
height = 864
res = (width, height)

# Vars
turn = "white" # Used in defs: DetectMouse
orgPos = (0, 0) # Used in defs: CheckMove

# The setup
pg.init() # Make pygame
screen = pg.display.set_mode(res) # Make screen with resolution
background = pg.transform.scale(pg.image.load("Media/board.png"), (1080, 864)) # Get the background
clock = pg.time.Clock() # Make a clock for the gameloop fps

# Sprite groups to draw
grid = pg.sprite.Group() # All squares of grid. Used in defs: CheckMove, Grid, UpdatePieces
pawns = pg.sprite.Group() # All pawns in the game. Used in defs: Pawns, DetectMouse, UpdatePieces
pieces_group = pg.sprite.Group() # All pieces in the game. Used in defs: Draw, Pawns, CheckMove

# Class for a square of the grid
class GridSquare(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load("Media/grid-circle.png"), (108, 108)) # Make the circle for the inner square to the correct size
        self.rect = self.image.get_rect() # Make the square the correct size

# Class for a pawn in the game
class Pawn(pg.sprite.Sprite):
    def __init__(self, img, posX, colour):
        super().__init__()
        self.posY = 2 # Starting Y position
        self.posX = posX # Starting X position which is chosen by posX in class asignment
        self.colour = colour # Which colour the piece is
        self.active = False # If the user is selecting the piece
        self.UpdatePos() # Update the position which the piece is standing on
        self.image = pg.transform.scale(pg.image.load(img), (108, 108)) # Make the image the correct scale
        self.rect = self.image.get_rect() # Make the piece the correct size
        self.rect.center = self.position # Put the piece on the correct place
    def UpdatePos(self): # Updating the position of the pawn
        if self.colour == "white": # Used the correct formula for the specific colour
            self.position = ((108 * 2.5) + (108 * (self.posX - 1)), height - ((108 / 2) + (108 * (self.posY - 1))))
# (1 square is 108x108 pixels)
#   (108 * 2.5)                       | Ignoring black space and centering the piece
#   (108 * (self.posX - 1)            | Putting the pawn 1 square to the right depending on the X position declared in __init__()
#
#   height - (((108 / 2) + self.posY) | Centering the piece from the bottom
#   (108 * (self.posY - 1))           | Moving the pawn 1 square up from positioning
        elif self.colour == "black": # Same thing as white but the exact opposite
            self.position = ((108 * 2.5) + (108 * (self.posX - 1)), (108 / 2) + (108 * (self.posY - 1)))
    def DetectMouse(self):
        if self.rect.collidepoint(pg.mouse.get_pos()): # Check if mouse is colliding with the pawn
            if pg.mouse.get_pressed()[0]: # Check if the mouse is being pressed
                for pawn in pawns: # Make if so if one pawn is active others aren't
                    if pawn.active == True: return
                global turn # Check if its the users turn
                if turn == self.colour:
                    self.active = True # Select the pawn
            elif self.active == True: self.active = False # If the mouse isn't being pressed deselect the pawn

def CheckMove():
    for square in grid:
        if square.rect.collidepoint(pg.mouse.get_pos()): # Check if mouse collides with a square in grid
            if pg.mouse.get_pressed()[0]: # Check if mouse is pressed
                for i in pieces_group: 
                    orgPos = i.rect.center # Get the original position of the piece
                    #! if i.rect.collidepoint(pg.mouse.get_pos()): return            | Forgot what this was for
                    if i.active == True: # If piece is selected
                        global turn
                        if square.rect.center == orgPos: return # If moved location is same as original location don't move
                        i.rect.center = square.rect.center # Move piece to hovered square

def Pawns(): # Make pawns
    for i in range(1, 9):
        white_pawn = Pawn("Media/white_pawn.png", i, "white")
        black_pawn = Pawn("Media/black_pawn.png", i, "black")
        pawns.add(white_pawn) # Put the pawns in the correct group
        pawns.add(black_pawn) # Put the pawns in the correct group
    for pawn in pawns:
        pieces_group.add(pawn) # Put the pawns in the correct group

def Grid(): # Make grid
    for row in range(1, 9):
        for pos in range(1, 9):
            square = GridSquare()
            square.rect.center = (width - ((108 * (pos - 1)) + 54), (108 * (row - 1)) + 54) # Place the squares in the correct place to form a grid
            grid.add(square) # Add the squared to the sprite group "Grid"

def Draw():
    pieces_group.draw(screen) # Draw the pieces on the screen

def UpdatePieces():
    for pawn in pawns:
        pawn.DetectMouse() # Detect mouse activity over pawn using DetectMouse funtion of pawn
        if pawn.active == True:
            circles = pg.sprite.Group() # Make new sprite group to show the circles
            for square in grid:
                if pawn.colour == "white": # If the pawn is white
                    if (pawn.rect.centery - 108) == square.rect.centery:
                        if pawn.rect.centerx == square.rect.centerx: # Add the square infront of pawn to circles
                            circles.add(square)
                elif (pawn.rect.centery + 108) == square.rect.centery:
                    if pawn.rect.centerx == square.rect.centerx: # Add the square infront of pawn to circles
                        circles.add(square)
            circles.draw(screen) # Draw circles

def Update(): # Update every frame
    screen.blit(background, (0, 0))
    Draw()
    UpdatePieces()
    CheckMove()

def End():
    for event in pg.event.get():
        if event.type == pg.QUIT: return True

Grid()
Pawns()
while True: # Gameloop
    if End(): break
    Update()
    pg.display.flip()
    clock.tick(60)