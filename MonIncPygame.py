from pygame import *
from pygame.sprite import *
from random import *

#creating a sprite controlled by mouse movement: http://programarcadegames.com/python_examples/show_file.php?file=move_sprite_mouse.py
#scoreboard: https://github.com/JamesMcColl/Grudius-X/blob/3cede7ddbd809616f4ee950f9b547a4b756ca99e/Assignment4/ScoreTest.py
#shell of program based off of dig-for-gold game

DELAY = 1000;            #Seed a timer to move sprite


class Burger(Sprite):     #sprites can become rectangles or images under Gold
    def __init__(self):
        Sprite.__init__(self)   #init- make a brand new sprite for me
        self.image = image.load("Burg.bmp").convert_alpha()
        self.rect = self.image.get_rect()  #update sprite so it's not generic, give it values that I want- move this way, it's this picture, etc. 

    # move Burger to a new random location
    def move(self):
        randX = randint(0, 600)  
        randY = randint(0, 400)   
        self.rect.center = (randX,randY)   #self.rect.center- move to two random numbers 

class Bomb(Burger):           #do everything that burger does, but this is bomb
    def __init__(self):
        Sprite.__init__(self)
        self.image = image.load("Randall.bmp").convert_alpha()
        self.rect = self.image.get_rect()        

class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)   #new sprite different from burger and bomb
        self.image = image.load("Sully.bmp").convert_alpha()   
        self.rect = self.image.get_rect()    #image.load = load image method

    # detect collision
    def hit(self, target):  
        return self.rect.colliderect(target)  

    def update(self):     
        self.rect.center = mouse.get_pos()   #follow mouse position

#scoreboard
class Scoreboard(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.lives = 5
        self.score = 0
        self.font = font.SysFont("Arial", 30)  #initialize points to beginning with 5

    def update(self):
        self.text = " score = %d" % (self.lives + self.score)      #update the scoreboard, display it
        self.image = self.font.render(self.text, 1, (0, 150, 255))  
        self.rect = self.image.get_rect()
        
    def gameover(self):
        self.text = "Game over!"                                    #display game over when get to 0 pts
        self.image = self.font.render(self.text, 1, (0, 150, 255))
        self.rect = self.image.get_rect()

    def youwon(self):
        self.text = "You've reached 10- You won!"                   #display you won when get to 10 pts
        self.image = self.font.render(self.text, 1, (0, 150, 255))
        self.rect = self.image.get_rect()


#main
init()

screen = display.set_mode((640, 480))
display.set_caption('Eat-The-Burger!')  #title at top of page
time.set_timer(USEREVENT, 20)

#add background image through blit
bg_img = image.load("MonstersInc.bmp").convert_alpha()
bg_rect = bg_img.get_rect()


# hide the mouse cursor so we only see elephant
mouse.set_visible(False)  #make mouse pointer go away

f = font.Font(None, 25)

# create group of icons 
burger = Burger()   
player = Player()
bomb = Bomb()
score = Scoreboard()

# creates a group of sprites so all can be updated at once
sprites = RenderPlain(player, burger, bomb, score)

hits = 0
time.set_timer(USEREVENT + 1, DELAY)
gameOver = False
youWon = False

while not gameOver:  
    e = event.poll()
    if e.type == QUIT:
        quit()  #quit program
        
#collision of burger
    elif e.type == MOUSEBUTTONDOWN:   #mouseclick
        if player.hit(burger):          #bool
            mixer.Sound("Bite.wav").play()  #sound that plays when hit burger
            burger.move()  #method
                         
            score.score += 1 #add point   

#collision of bomb
        if player.hit(bomb):
           mixer.Sound("Bomb.wav").play()  #sound that plays when hit bomb (Randall)
           bomb.move()
           score.lives += -1

           #reset timer
           time.set_timer(USEREVENT + 1, DELAY)
           
        #if lives are equal to 0, game is over
        if score.score + score.lives == 0:
            gameOver = True

        #if lives are equal to 10, win game
        elif score.score + score.lives == 10:
            youWon = True
           

    #timer- at this point bc time ran out 
    elif e.type == USEREVENT + 1: # TIME has passed  
        burger.move()
        bomb.move()
 
       #update screen     
    screen.blit(bg_img, bg_rect)

    # update and redraw sprites   
    sprites.update()  #every time something happens- update sprites
    if gameOver == True:
        score.gameover()
        sprites.draw(screen)
        display.update()
        pygame.time.delay(1000)

    if youWon == True:
        score.youwon()
        sprites.draw(screen)
        display.update()
        pygame.time.delay(1000)
        
    sprites.draw(screen)
    display.update()
    

