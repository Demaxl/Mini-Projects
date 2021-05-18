import pygame
import os
import random

# setting the window
WIDTH, HEIGHT = 640, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Memory Puzzle')

# Global Variables
FPS = 30
BOXSIZE = 70
GAP = 10
BOARDWIDTH = 6
BOARDHEIGHT = 5
XDIST = int((WIDTH - (BOARDWIDTH * (BOXSIZE + GAP))) / 2)
YDIST = int((HEIGHT - (BOARDHEIGHT * (BOXSIZE + GAP))) / 2)

# Colors
NAVYBLUE = ( 60,  60, 100)
BLUE = (0,0,255)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)

BGCOLOR = NAVYBLUE
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE
LIGHTBGCOLOR = GRAY


def create_board():
    """ Creates the general game board"""
    boxes = []
    for i in range(BOARDWIDTH):
        boxes.append([0] * BOARDHEIGHT)
    return boxes
#--------------------------------------------------------------------------------------------------------------------------------------------

def showed_boxes(val):
    """Function that generates a list of boxes that are covered/uncovered """
    revealed_boxes = []
    for i in range(BOARDWIDTH):
        revealed_boxes.append([val] * BOARDHEIGHT)
    return revealed_boxes
#--------------------------------------------------------------------------------------------------------------------------------------

def pixel_coords(boxx, boxy):
    """This function is used to get the pixel coordinates of a box """
    left = boxx * (BOXSIZE + GAP) + XDIST
    top = boxy * (BOXSIZE + GAP) + YDIST
    return (left, top)
#--------------------------------------------------------------------------------------------------------------------------------------

def board_coords(x, y):
    """This function is used to get the board coordinates the mouse is over"""
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = pixel_coords(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)
#-----------------------------------------------------------------------------------------------------------------------------------------

def get_board_images():
    """This function returns a board with randomly placed images  """
    images_list = []
    for img in os.listdir('Assets/'):
        images_list.append(img)

    images = [0] * 17
    for i in range(len(images_list)):
        load = pygame.image.load(os.path.join('Assets', images_list[i]))
        images[i] = pygame.transform.scale(load, (BOXSIZE, BOXSIZE))

    random.shuffle(images)
    needed_icons= int(BOARDWIDTH * BOARDHEIGHT / 2) # calculate how many icons are needed
    images = images[:needed_icons] * 2 # make two of each
    random.shuffle(images)

    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(images[0])
            del images[0] # remove the icons as we assign them
        board.append(column)
    return board
#-----------------------------------------------------------------------------------------------------------------------------------------

def draw_image(boxx, boxy, images):
    '''Draws the image unto the board '''
    left, top = pixel_coords(boxx, boxy)
    image = images[boxx][boxy]
    WIN.blit(image, (left, top))
#----------------------------------------------------------------------------------------------------------------------------------------------------------

def highlight_box(boxx, boxy):
    '''Draws an highlight box '''
    left, top = pixel_coords(boxx, boxy)
    pygame.draw.rect(WIN, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)
#------------------------------------------------------------------------------------------------------------------------------------------------

def cover_box(boxx, boxy, images):
    left, top = pixel_coords(boxx, boxy)
    pygame.draw.rect(WIN, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
    draw_image(boxx, boxy, images)
    pygame.display.update()
#------------------------------------------------------------------------------------------------------------------------------------------------

def win(showed_boxes):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in showed_boxes:
        if False in i:
            return False # return False if any boxes are covered.
    return True
#------------------------------------------------------------------------------------------------------------------------------------------------

def win_effect(board, images):
    # flash the background color when the player has won
    coveredboxes = showed_boxes(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR
    for i in range(13):
        color1, color2 = color2, color1 # swap colors
        WIN.fill(color1)
        draw_board(board, images, coveredboxes)
        pygame.display.update()
        pygame.time.wait(300)
#--------------------------------------------------------------------------------------------------------------------------------------------------------

def start_game_flash(images):
    ''' Reveals the images for a second at the beginning'''
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = pixel_coords(boxx, boxy)
           # pygame.draw.rect(WIN, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            #pygame.display.update()
            draw_image(boxx, boxy, images)
            pygame.display.update()
            clock.tick(FPS)
#----------------------------------------------------------------------------------------------------------------------------------------------------

def draw_board(board, images, showed_box):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = pixel_coords(boxx, boxy)
            if not showed_box[boxx][boxy]:
                pygame.draw.rect(WIN, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                draw_image(boxx, boxy, images)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    global clock
    clock = pygame.time.Clock()
    board = create_board()
    images = get_board_images()
    showed_box = showed_boxes(False)

    mousex, mousey = 0, 0
    firstclicked = None

    WIN.fill(BGCOLOR)
    start_game_flash(images)
    pygame.time.wait(250)

    while True:
        clicked = False

        WIN.fill(BGCOLOR)
        draw_board(board, images, showed_box)

        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clicked = True

        boxx, boxy = board_coords(mousex, mousey)
        if boxx != None and boxy != None:
            if not showed_box[boxx][boxy]:
                highlight_box(boxx, boxy)
            if not showed_box[boxx][boxy] and clicked:
                showed_box[boxx][boxy] = True
                if firstclicked == None:
                    firstclicked = (boxx, boxy)
                else:
                    if images[boxx][boxy] == images[firstclicked[0]][firstclicked[1]]:
                        if win(showed_box):
                            win_effect(board, images)
                            pygame.time.wait(2000)
                            break
                    else:
                        cover_box(boxx, boxy, images)
                        pygame.time.wait(1000)
                        showed_box[boxx][boxy] = False
                        showed_box[firstclicked[0]][firstclicked[1]] = False
                        
                    firstclicked = None
        pygame.display.update()
        clock.tick(FPS)
    main()
#========================================================================================================================================


if __name__ == '__main__':
    main()

# By Abdullahi A.A 
# also known as Demaxl