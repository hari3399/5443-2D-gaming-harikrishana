# import your modules
import random
import pygame
import words
from pygame import mixer


pygame.init()

mixer.music.load('song.mp3')
mixer.music.set_volume(0.7)


def paused():
    pygame.mixer.music.pause()

def unpaused():
    pygame.mixer.music.unpause()

# create screen, fonts, colors, game variables
screen = pygame.display.set_mode([520, 700])

pygame.display.set_caption('Wordle Game')
icon = pygame.image.load('game-controller.png')
pygame.display.set_icon(icon)

image = pygame.image.load('game-controller.png')
width = image.get_rect().width
height = image.get_rect().height
image = pygame.transform.scale(image, (int(width*0.28), int(height*0.25)))

def player(x,y):
    screen.blit(image, (x, y))



move = 0
pause = 0
matrix = [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "]]

clock = pygame.time.Clock()
game_font = pygame.font.Font('freesansbold.ttf', 56)
random_word = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
game_status = False           #whether game is over or not



def text_objects(text, font, clr):
    textSurface = font.render(text, True, clr)
    return textSurface, textSurface.get_rect()

Black = (0, 0, 0)
DarkGreen  = (0, 255, 0)
red = (255,0,0)
lightRed = (200, 0, 0)
blue = (0,0,255)
yellow = (255, 255, 0)
grey = (128, 128, 128)
white = (255, 255, 255)
green = (0,200,0)
lightBlue = (0,0,200)
activeRows = True

def button(msg,x,y,w,h,i,a,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, a, (x,y,w,h))
        if click[0] == 1 and action!= None:
            if action == "play":
                unpaused()
                game_loop()
            elif action == "stop":
                pygame.quit()
    else:
        pygame.draw.rect(screen, i,  (x,y,w,h))
        
    smallText = pygame.font.Font('freesansbold.ttf', 20)
    textSurf, textRect = text_objects(msg, smallText,Black)
    textRect.center =( (x+(w/2)), (y+(h/2)))
    screen.blit(textSurf, textRect)

#code for welcome screen
def game_intro():
    intro = True
    image = pygame.image.load('hi.png')
    width = image.get_rect().width
    height = image.get_rect().height
    image = pygame.transform.scale(image, (int(width*0.28), int(height*0.25)))
    while intro:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        screen.fill((227,245,113))
        screen.blit(image,(290,530))
        largeText = pygame.font.Font('freesansbold.ttf',15)
        heading = pygame.font.Font('freesansbold.ttf',50)
        TextSurf0, TextRect0 = text_objects("WELCOME", heading,blue)
        TextSurf, TextRect = text_objects("# The player has to guess the Wordle in six attempts or less.", largeText,lightBlue)
        TextSurf2, TextRect2 = text_objects("# If the letter is correct the color would turn green" , largeText,lightBlue)
        TextSurf3, TextRect3 = text_objects("# If the letter is correct but placed wrong then it would turn yellow", largeText,lightBlue)
        TextSurf4, TextRect4 = text_objects("# An incorrect letter turns gray, Letters can be used more than one time", largeText,lightBlue)
        TextRect0.center = (260, 120)
        TextRect.center = (215, 235)
        TextRect2.center = (180, 270)
        TextRect3.center = (240, 305)
        TextRect4.center = (255, 340)
        screen.blit(TextSurf0, TextRect0)
        screen.blit(TextSurf, TextRect)
        screen.blit(TextSurf2, TextRect2)
        screen.blit(TextSurf3, TextRect3)
        screen.blit(TextSurf4, TextRect4)

        button("play",90,450,100,50,green,DarkGreen,"play")
        button("Stop",310,450,100,50,lightRed, red,"stop")
         
        pygame.display.update()
        


# create box for playing game
def write():
    global matrix
    global move
    for j in range(0, 5):
        for i in range(0, 6):
            pygame.draw.rect(screen, Black, [j * 100 + 25, i * 100 + 12, 75, 75], 3, 5)
            guessed_word = game_font.render(matrix[i][j], True, red)
            screen.blit(guessed_word, (j * 100 + 40, i * 100 + 25))
    pygame.draw.rect(screen, DarkGreen,  [17, move * 100 + 5, 490, 90], 3, 5)


# write code for checking words
def compare_word():
    global matrix
    global move
    global random_word
    for j in range(0, 5):
        for i in range(0, 6):
            if random_word[j] == matrix[i][j] and move > i:
                pygame.draw.rect(screen, DarkGreen,  [j * 100 + 25, i * 100 + 12, 75, 75], 0, 5)
            elif matrix[i][j] in random_word and move > i:
                pygame.draw.rect(screen, yellow, [j * 100 + 25, i * 100 + 12, 75, 75], 0, 5)


# Code for main game 

def game_loop():
    pygame.mixer.music.play(-1)

    global matrix
    global move
    global random_word
    global game_status
    Xdist = 270
    Ydist = 550
    alphabet = 0
    Inactive = False
    while not Inactive:
        clock.tick(60)
        screen.fill((227,245,113))
    
    
        Xdist += 0.5
        if Xdist <=0:
           Xdist=0
        elif Xdist >= 400:
           Xdist = 0
    
        player(Xdist, Ydist)
        compare_word()
        write()
  
 
   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                  #if player chooses to quit game
                Inactive = True

        # adding player controls for letter input, backspacing, checking guesses and restarting

            if event.type == pygame.TEXTINPUT and activeRows and not game_status:
                    inputAlphabet = event.__getattribute__('text')           #if player enters letter
                    if inputAlphabet != " ":
                        inputAlphabet = inputAlphabet.lower()
                        matrix[move][alphabet] = inputAlphabet
                        alphabet += 1
                                    
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE and alphabet > 0:   #if player uses backspace
                    matrix[move][alphabet - 1] = ' ' 
                    alphabet -= 1 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and  not game_status:          
                    move += 1
                    alphabet = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_status:
                    move = 0
                    alphabet = 0 
                    game_status = False                                                   #ending the game
                    random_word = words.WORDS[random.randint(0, len(words.WORDS) - 1)]    # choosing a random word from given list of words

                    matrix =[[" ", " ", " ", " ", " "],
                            [" ", " ", " ", " ", " "],
                            [" ", " ", " ", " ", " "],
                            [" ", " ", " ", " ", " "],
                            [" ", " ", " ", " ", " "],
                            [" ", " ", " ", " ", " "]]

        # control move activeRows based on letters
            if alphabet == 5:
                activeRows = False
            if alphabet < 5:
                activeRows = True

        # check if guess is correct, add game over conditions

            for i in range(0, 6):
                written_word = matrix[i][0] + matrix[i][1] + matrix[i][2] + matrix[i][3] + matrix[i][4]
                if written_word == random_word and i <= move:
                    game_status = True
                                           
            if game_status and move < 6:                 # winning condition is moves used are less than 6
                winmsg = game_font.render('You Won', True, DarkGreen) 
                screen.blit(winmsg, (43, 610))
                pygame.time.wait(1400)
                
            
            elif move == 6:                                # if all the 6 moves are used up, then player loses
                game_status = True
                losemsg = game_font.render('You Lose', True, Black)
                screen.blit(losemsg, (43, 610))
        #songPlay()
  
        pygame.display.flip()
    
   

game_intro()
game_loop()
pygame.quit()
