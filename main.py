import pygame as pg

# Screen resolution
scale = 1
width = 1080 * scale
height = 864 * scale
res = (width, height)

# Vars
turn = "white" # Used in defs: DetectMouse
orgPos = (0, 0) # Used in defs: CheckMove
gridSize = 108 * scale

# The setup
pg.init() # Make pygame
screen = pg.display.set_mode(res) # Make screen with resolution
background = pg.transform.scale(pg.image.load("Media/board.png"), res) # Get the background
clock = pg.time.Clock() # Make a clock for the gameloop fps

# Sprite groups to draw
grid = pg.sprite.Group() # All squares of grid. Used in defs: CheckMove, Grid, UpdatePieces
pawns = pg.sprite.Group() # All pawns in the game. Used in defs: Pawns, DetectMouse, UpdatePieces
rooks = pg.sprite.Group() # All rooks in the game. Used in defs: 
knights = pg.sprite.Group() # All knights in the game. Used in defs: 
bishops = pg.sprite.Group() # All bishops in the game. Used in defs: 
queens = pg.sprite.Group() # All queens in the game. Used in defs: 
kings = pg.sprite.Group() # All kings in the game. Used in defs: 
piecesGroup = pg.sprite.Group() # All pieces in the game. Used in defs: Draw, Pawns, CheckMove
circles = pg.sprite.Group() # Make new sprite group to show the circles

# Class for a square of the grid
class GridSquare(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load("Media/grid-circle.png"), (gridSize, gridSize)) # Make the circle for the inner square to the correct size
        self.rect = self.image.get_rect() # Make the square the correct size

# Class for a pawn in the game
class Piece(pg.sprite.Sprite):
    def __init__(self, pieceType, img, posX, posY, colour):
        super().__init__()
        self.type = pieceType # Check what type the piece is (ex: pawn)
        self.posY = posY # Starting Y position which is chosen by posX in class asignment
        self.posX = posX # Starting X position which is chosen by posX in class asignment
        self.colour = colour # Which colour the piece is
        self.active = False # If the user is selecting the piece
        self.ResetPos() # Update the position which the piece is standing on
        self.image = pg.transform.scale(pg.image.load(img), (gridSize, gridSize)) # Make the image the correct scale
        self.rect = self.image.get_rect() # Make the piece the correct size
        self.rect.center = self.position # Put the piece on the correct place
        self.orginx = self.rect.centerx
        self.orginy = self.rect.centery
    def ResetPos(self): # Updating the position of the pawn
        if self.colour == "white": # Used the correct formula for the specific colour
            self.position = ((gridSize * 2.5) + (gridSize * (self.posX - 1)), height - ((gridSize / 2) + (gridSize * (self.posY - 1))))
        elif self.colour == "black": # Same thing as white but the exact opposite
            self.position = ((gridSize * 2.5) + (gridSize * (self.posX - 1)), (gridSize / 2) + (gridSize * (self.posY - 1)))
    def DetectMouse(self):
        if self.rect.collidepoint(pg.mouse.get_pos()): # Check if mouse is colliding with the pawn
            if pg.mouse.get_pressed()[0]: # Check if the mouse is being pressed
                for piece in piecesGroup: # Make if so if one piece is active others aren't
                    if piece.active != False: return
                global turn # Check if its the users turn
                if turn == self.colour:
                    self.active = True # Select the piece
                    self.orginx = self.rect.centerx
                    self.orginy = self.rect.centery
                    UpdatePiece(self)
            elif self.active != False:
                self.Unselect()
    def Unselect(self):
        self.active = False # If the mouse isn't being pressed deselect the pawn
        self.orginx = None
        self.orginy = None
        circles.empty()

def CheckMove(piece):
    if piece.active == False: return False
    for square in grid:
        if square.rect.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed()[0]: # Check if mouse collides with a square in grid
            global turn
            match piece.type:
                case "pawn":
                    if PawnLogic(piece, square) == False:
                        return False
                case "rook":
                    if RooksLogic(piece, square) == False:
                        return False
                case "knight":
                    if KnightsLogic(piece, square) == False:
                        return False
                case "bishop":
                    if BishopsLogic(piece, square) == False:
                        return False
                case "queen":
                    if QueensLogic(piece, square) == False:
                        return False
                case "king":
                    if KingsLogic(piece, square) == False:
                        return False
            piece.rect.center = square.rect.center # Move piece to hovered square
            SwitchTurn()

def SwitchTurn():
    global turn
    if turn == "white": turn = "black"
    elif turn == "black": turn = "white"

def Pawns(): # Make pawns
    for i in range(1, 9):
        whitePiece = Piece("pawn", "Media/white_pawn.png", i, 2, "white")
        blackPiece = Piece("pawn", "Media/black_pawn.png", i, 2, "black")
        pawns.add(whitePiece) # Put the piece in the correct group
        pawns.add(blackPiece) # Put the piece in the correct group
    for piece in pawns:
        piecesGroup.add(piece) # Put the piece in the correct group
def Rooks(): # Make rooks
    num = 1
    for i in range(1, 3):
        whitePiece = Piece("rook", "Media/white_rook.png", num, 1, "white")
        blackPiece = Piece("rook", "Media/black_rook.png", num, 1, "black")
        rooks.add(whitePiece) # Put the piece in the correct group
        rooks.add(blackPiece) # Put the piece in the correct group
        num += 7
    for piece in rooks:
        piecesGroup.add(piece) # Put the piece in the correct group
def Knights(): # Make knights
    num = 2
    for i in range(1, 3):
        whitePiece = Piece("knight", "Media/white_knight.png", num, 1, "white")
        blackPiece = Piece("knight", "Media/black_knight.png", num, 1, "black")
        knights.add(whitePiece) # Put the piece in the correct group
        knights.add(blackPiece) # Put the piece in the correct group
        num += 5
    for piece in knights:
        piecesGroup.add(piece) # Put the piece in the correct group
def Bishops(): # Make bishops
    num = 3
    for i in range(1, 3):
        whitePiece = Piece("bishop", "Media/white_bishop.png", num, 1, "white")
        blackPiece = Piece("bishop", "Media/black_bishop.png", num, 1, "black")
        bishops.add(whitePiece) # Put the piece in the correct group
        bishops.add(blackPiece) # Put the piece in the correct group
        num += 3
    for piece in bishops:
        piecesGroup.add(piece) # Put the piece in the correct group
def Queens(): # Make queens
    whitePiece = Piece("queen", "Media/white_queen.png", 4, 1, "white")
    blackPiece = Piece("queen", "Media/black_queen.png", 5, 1, "black")
    queens.add(whitePiece) # Put the piece in the correct group
    queens.add(blackPiece) # Put the piece in the correct group
    for piece in queens:
        piecesGroup.add(piece) # Put the piece in the correct group
def Kings(): # Make Kings
    whitePiece = Piece("king", "Media/white_king.png", 5, 1, "white")
    blackPiece = Piece("king", "Media/black_king.png", 4, 1, "black")
    kings.add(whitePiece) # Put the piece in the correct group
    kings.add(blackPiece) # Put the piece in the correct group
    for piece in kings:
        piecesGroup.add(piece) # Put the piece in the correct group

def PawnLogic(piece, square):
    if (piece.orginx == square.rect.centerx and piece.orginy == square.rect.centery): return True
    if piece.colour == "white": # If the piece is white
        if piece.rect.centery == height-(gridSize + (gridSize / 2)):
            if ((piece.orginy - gridSize*2) == square.rect.centery and
                piece.orginx == square.rect.centerx):
                return True
        if ((piece.orginy - gridSize) == square.rect.centery and
            piece.orginx == square.rect.centerx):
            return True
    if piece.colour == "black": # If the piece is black
        if piece.rect.centery == (gridSize + (gridSize / 2)):
            if ((piece.orginy - gridSize*2) == square.rect.centery and
                piece.orginx == square.rect.centerx):
                return True
        if ((piece.orginy + gridSize) == square.rect.centery and
            piece.orginx == square.rect.centerx):
            return True
    return False
def RooksLogic(piece, square):
    if (piece.orginx == square.rect.centerx and piece.orginy == square.rect.centery): return True
    if piece.orginy == square.rect.centery or piece.orginx == square.rect.centerx:
        return True
    return False
def KnightsLogic(piece, square):
    if (piece.orginx == square.rect.centerx and piece.orginy == square.rect.centery): return True
    if ((piece.orginy - gridSize*2) == square.rect.centery and (piece.orginx - gridSize) == square.rect.centerx or (piece.orginy - gridSize*2) == square.rect.centery and (piece.orginx + gridSize) == square.rect.centerx or
        (piece.orginy + gridSize*2) == square.rect.centery and (piece.orginx - gridSize) == square.rect.centerx or (piece.orginy + gridSize*2) == square.rect.centery and (piece.orginx + gridSize) == square.rect.centerx or
        (piece.orginy + gridSize) == square.rect.centery and (piece.orginx - gridSize*2) == square.rect.centerx or (piece.orginy + gridSize) == square.rect.centery and (piece.orginx + gridSize*2) == square.rect.centerx or
        (piece.orginy - gridSize) == square.rect.centery and (piece.orginx - gridSize*2) == square.rect.centerx or (piece.orginy - gridSize) == square.rect.centery and (piece.orginx + gridSize*2) == square.rect.centerx): # Add the square infront of piece to circles
        return True
    return False
def BishopsLogic(piece, square):
    if (piece.orginx == square.rect.centerx and piece.orginy == square.rect.centery): return True
    for i in range(8):
        if ((piece.orginy - gridSize*i) == square.rect.centery and (piece.orginx - gridSize*i) == square.rect.centerx or
            (piece.orginy - gridSize*i) == square.rect.centery and (piece.orginx + gridSize*i) == square.rect.centerx or
            (piece.orginy + gridSize*i) == square.rect.centery and (piece.orginx - gridSize*i) == square.rect.centerx or
            (piece.orginy + gridSize*i) == square.rect.centery and (piece.orginx + gridSize*i) == square.rect.centerx):
            return True
    return False
def QueensLogic(piece, square):
    if (piece.orginx == square.rect.centerx and piece.orginy == square.rect.centery): return True
    if piece.orginy == square.rect.centery or piece.orginx == square.rect.centerx:
        return True
    for i in range(8):
        if ((piece.orginy - gridSize*i) == square.rect.centery and (piece.orginx - gridSize*i) == square.rect.centerx or
            (piece.orginy + gridSize*i) == square.rect.centery and (piece.orginx + gridSize*i) == square.rect.centerx or
            (piece.orginy - gridSize*i) == square.rect.centery and (piece.orginx + gridSize*i) == square.rect.centerx or
            (piece.orginy + gridSize*i) == square.rect.centery and (piece.orginx - gridSize*i) == square.rect.centerx):
            return True
    return False
def KingsLogic(piece, square):
    if (piece.orginx == square.rect.centerx and piece.orginy == square.rect.centery): return None
    if ((piece.orginy - gridSize) == square.rect.centery and piece.orginx == square.rect.centerx or
        (piece.orginy + gridSize) == square.rect.centery and piece.orginx == square.rect.centerx or
        (piece.orginx - gridSize) == square.rect.centerx and piece.orginy == square.rect.centery or
        (piece.orginx + gridSize) == square.rect.centerx and piece.orginy == square.rect.centery or
        (piece.orginy - gridSize) == square.rect.centery and (piece.orginx - gridSize) == square.rect.centerx or
        (piece.orginy - gridSize) == square.rect.centery and (piece.orginx + gridSize) == square.rect.centerx or
        (piece.orginy + gridSize) == square.rect.centery and (piece.orginx - gridSize) == square.rect.centerx or
        (piece.orginy + gridSize) == square.rect.centery and (piece.orginx + gridSize) == square.rect.centerx):
        return True
    return False

def Grid(): # Make grid
    for row in range(1, 9):
        for column in range(1, 9):
            square = GridSquare(row, column)
            square.rect.center = (width - ((gridSize * (column - 1)) + (gridSize / 2)), (gridSize * (row - 1)) + (gridSize / 2)) # Place the squares in the correct place to form a grid
            grid.add(square) # Add the squared to the sprite group "Grid"
def Draw():
    piecesGroup.draw(screen) # Draw the pieces on the screen



def UpdatePiece(piece):
    pieceType = piece.type
    if piece.active != False:
        for square in grid:
            if piece.rect.centery == square.rect.centery and piece.rect.centerx == square.rect.centerx:
                continue
            match pieceType:
                case "pawn":
                    if PawnLogic(piece, square):
                        circles.add(square)
                case "rook":
                    if RooksLogic(piece, square):
                        circles.add(square)
                case "knight":
                    if KnightsLogic(piece, square):
                        circles.add(square)
                case "bishop":
                    if BishopsLogic(piece, square):
                        circles.add(square)
                case "queen":
                    if QueensLogic(piece, square):
                        circles.add(square)
                case "king":
                    if KingsLogic(piece, square):
                        circles.add(square)



def Update(): # Update every frame
    screen.blit(background, (0, 0))
    Draw()
    for piece in piecesGroup:
        CheckMove(piece)
        piece.DetectMouse()
    circles.draw(screen) # Draw circles
    if pg.mouse.get_pressed()[0] == False:
        for piece in piecesGroup:
            if piece.active != False:
                piece.Unselect()
def End():
    for event in pg.event.get():
        if event.type == pg.QUIT: break
def Start():
    Grid()
    Pawns()
    Knights()
    Bishops()
    Rooks()
    Queens()
    Kings()

Start()
while True:
    End()
    Update()
    pg.display.flip()
    clock.tick(60)