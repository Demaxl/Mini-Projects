"""
My First game made with the Pygame Framework.
This is a game was designed by a youtuber named Tech with Tim.
In a video(Pygame for beginners) he explained the basics of Pygame
and how to build this a game. This is just an improved version of it


Controls:
W-A-S-D : To move the short
LCTRL : To fire bullets

Tip:
Dodge the computer's blue bullets :)
"""
  


import pygame
import os
import configparser
import time
import _thread

pygame.init() # To initialise the pygame library
pygame.font.init() # To initialise the pygame font library
pygame.mixer.init() # To initialise the pygame sound library

settings = configparser.ConfigParser()
settings.read('settings.ini')

# setting the display
WIDTH = settings.getint('SETTINGS', 'WIDTH')
HEIGHT = settings.getint('SETTINGS', 'HEIGHT')

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Battle of Ships')
#-----------------------------------------------------------------------------------------------------------------------

# Global Variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
RESTART_FONT = pygame.font.SysFont('comicsans', 100)
BULLET_FIRE = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
BULLET_HIT = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))

VEL = settings.getint('SETTINGS', 'VEL')
BULLET_VEL = settings.getint('SETTINGS', 'BULLET_VEL')
MAX_BULLETS = settings.getint('SETTINGS', 'MAX_BULLETS')
SPACESHIP_WIDTH = settings.getint('SETTINGS', 'SPACESHIP_WIDTH')
SPACESHIP_HEIGHT = settings.getint('SETTINGS', 'SPACESHIP_HEIGHT')

YELLOW_HIT = pygame.USEREVENT + 1   # Creates a pygame custom event
RED_HIT = pygame.USEREVENT + 2      # We add numbers to it to make it a unique number
SPECIAL_HIT = pygame.USEREVENT + 3

BORDER = pygame.Rect((WIDTH//2)-5, 0, 10, HEIGHT)
#-----------------------------------------------------------------------------------------------------------------------

# Loading Images
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
        os.path.join('Assets', 'spaceship_yellow.png'))
# to resize an image and rotate an image
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
                        os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets', 'space.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
#-----------------------------------------------------------------------------------------------------------------------------

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, special_bullets):
    WIN.blit(BACKGROUND, (0,0)) 
    # pygame.draw.rect(window, color, rectange)
    pygame.draw.rect(WIN, BLACK, BORDER) # Used to draw a rectangle on a window

    # Cretes a text object using the HEALTH_FONT style
    red_health_text = HEALTH_FONT.render(f'Player Health: {red_health}', 1, RED)
    yellow_health_text = HEALTH_FONT.render(f'Computer Health: {yellow_health}', 1, YELLOW)

                                                # Gets the width
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) # These are the coords of the yellow rect
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in special_bullets:
        pygame.draw.rect(WIN, BLUE, bullet)

    pygame.display.update()
#-------------------------------------------------------------------------------------------------------------------

def tThread(a, b):
    global timer
    while True:
        time.sleep(1)
        timer += 1

def bulletThread(a, b):
    global bullet_timer
    while True:
        bullet_timer += 0.1
        time.sleep(0.5)
#------------------------------------------------------------------------------------------------------------------------------

movement = None
def computer_handle_movement(yellow, red, timer):
    global movement
    if timer % 2 == 0:
        movement = 'down'
    else:
        movement = 'up'
    upper = red.y - 100
    lower = red.y + 100

    if movement == 'up':
        if yellow.y > upper and yellow.y > 0:
            yellow.y -= VEL 

    elif movement == 'down':
        if yellow.y + yellow.width < lower and yellow.y + VEL + yellow.width < HEIGHT:
            yellow.y += VEL   
#------------------------------------------------------------------------------------------------------------

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.width < HEIGHT: # DOWN
        red.y += VEL
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width : # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # RIGHT
        red.x += VEL
#-------------------------------------------------------------------------------------------------------------

def handle_bullets(yellow_bullets, red_bullets, yellow, red, special_bullets):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        # A pygame function that checks if 2 rectangles have collided
        # i.e yellow has collided with bullet
        if red.colliderect(bullet):
            # Makes a new event saying that the red ship was hit
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
  
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
    
    for bullet in special_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(SPECIAL_HIT))
            special_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            special_bullets.remove(bullet)
#---------------------------------------------------------------------------------------------------------

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2,
                         HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    # Makes the window pause for 5000 miliseconds(5 seconds)
    pygame.time.delay(5000)
#-----------------------------------------------------------------------------------------------------------------------------

def comp_move(bullet_timer, yellow_bullets, yellow, special_bullets):
    if str(bullet_timer).endswith('.5') == 0 and len(yellow_bullets)+2 < MAX_BULLETS: 
        bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 -2, 10, 5)
        yellow_bullets.append(bullet)
        BULLET_FIRE.play() # plays the loaded sound
        return

    elif '.9' in str(bullet_timer) and len(special_bullets) == 0: 
        bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 -2, 20, 10)
        special_bullets.append(bullet)
        BULLET_FIRE.play() # plays the loaded sound
        return
#-------------------------------------------------------------------------------------------------------------------------

restarted = False
def main():
    global timer, bullet_timer, restarted
    # creates a pygame rectangle
    """
    These rectangles were created to keep track of the postions of 
    the space ships
    """
    red = pygame.Rect(700, 300 ,SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300 ,SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    FPS = 60
    timer = 0
    bullet_timer = 0

    red_bullets = []
    yellow_bullets = []
    special_bullets = []

    red_health = 10
    yellow_health = 10  
    
    
    clock = pygame.time.Clock()
    if not restarted:
        _thread.start_new_thread(tThread, (1,2))
        _thread.start_new_thread(bulletThread, (1,2))
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN: # i.e A key is being pressed
                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 -2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE.play()
                

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT.play()
            if event.type == SPECIAL_HIT:
                red_health -= 3
                BULLET_HIT.play()

        comp_move(bullet_timer, yellow_bullets, yellow, special_bullets)
        winner_text = ''
        if red_health <= 0:
            winner_text = 'Yellow Wins!'
        if yellow_health <= 0:
            winner_text = 'Red Wins!'

        if winner_text != '':
            draw_winner(winner_text)
            break
        # gets the keys that are being pressed
        keys_pressed = pygame.key.get_pressed()
       
        computer_handle_movement(yellow, red, timer)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red, special_bullets)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, special_bullets)
 
    restarted = True
    main()
    


if __name__ == '__main__': 
    main()


