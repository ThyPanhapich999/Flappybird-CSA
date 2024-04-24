import pygame, time
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock() # create an object to help track time
fps = 60 # frames per second

#sound
wing = 'audio/wing.wav'
hit = 'audio/hit.wav'
point = 'audio/point.wav'
die = 'audio/die.wav'

pygame.mixer.init() #initialize the mixer

# set up the display    
screen_width = 680
screen_height = 750

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

#define game font
font = pygame.font.SysFont('Bauhaus 93', 48)

#define colors
white = (255, 255, 255)

#define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency #time at the start of the game
score = 0
pass_pipe = False

#load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')


#function to draw text on the screen
def draw_text(text, font, text_col, x, y): 
    img = font.render(text, True, text_col) 
    screen.blit(img, (x, y))


#function to reset the game
def reset_game():
    pipe_group.empty() #empty the pipe group
    flappy.rect.x = 100 #reset the bird's x position
    flappy.rect.y = int(screen_height / 2) #reset the bird's y position
    score = 0
    return score


'''
1.initialize the sprite
2.list to store the images of the bird
3.index to iterate through the list of images
4.counter to slow down the animation
5.load all the images of the bird and add images to the list
6. the rectangle of the image
7. the position of the rectangle
8. the velocity of the bird
9. to check if the bird has been clicked
'''

#bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) 
        self.images = []                    
        self.index = 0                      
        self.counter = 0                   
        for num in range(1,4):              
            img = pygame.image.load(f'img/bird{num}.png') 
            self.images.append(img)          
        self.image = self.images[self.index] 
        self.rect = self.image.get_rect()  
        self.rect.center = [x, y]         
        self.vel_y = 0                    
        self.clicked = False             

    def update(self):

        if flying == True: 
            #gravity
            self.vel_y += 0.5 #increase the velocity
            if self.vel_y > 8: #set a maximum velocity
                self.vel_y = 8 
            if self.rect.bottom < 630: #if the bird is above the ground
                self.rect.y += int(self.vel_y) #move the bird down

        if game_over == False: 
            #jump
            if pygame.key.get_pressed()[pygame.K_SPACE] and self.clicked == False:
                self.clicked = True
                self.vel_y = -10
                pygame.mixer.Sound(wing).play()
            if pygame.key.get_pressed()[pygame.K_SPACE] == False:
                self.clicked = False

            #handle the animation
            self.counter += 1 #increase the counter
            flap_cooldown = 5   #set the flap cooldown

            if self.counter > flap_cooldown: #if the counter is greater than the flap cooldown
                self.counter = 0
                self.index += 1          
                if self.index >= len(self.images):  #if the index is greater than the length of the list
                    self.index = 0
            self.image = self.images[self.index]  #change the image
        
            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel_y * -2)
        else:
            self.image = self.images[self.index]
        
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        #position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)] # position the bottom pipe
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)] # position the top pipe

    def update(self):
        self.rect.x -= scroll_speed #move the pipe to the left
        if self.rect.right < 0: #if the pipe is off the screen
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


bird_group = pygame.sprite.Group() #create a bird group
pipe_group = pygame.sprite.Group() #create a pipe group

flappy = Bird(100, int(screen_height / 2)) #create a flappy object

bird_group.add(flappy)  #add the flappy bird to the bird group

#create restart button instance
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

#ground loop
run = True
while run:

    clock.tick(fps)

    #draw background
    screen.blit(bg, (0,0))

    bird_group.draw(screen) #draw the bird group
    bird_group.update()    #update the bird group
    pipe_group.draw(screen) #draw the pipe group

    #draw the ground
    screen.blit(ground_img, (ground_scroll, screen_height - ground_img.get_height()))

    #check the score
    if len(pipe_group) > 0:
        #if the bird passes the pipe, increase the score
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            #if the bird passes the pipe, increase the score
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right: 
                score += 1
                pass_pipe = False
                pygame.mixer.Sound(point).play()


    draw_text(str(score), font, white, int(screen_width / 2), 20) #draw the score

    #track collision
    #if the bird hits the pipe or the top of the screen
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0: 
        game_over = True
        pygame.mixer.music.load(hit)
        pygame.mixer.music.play()


    #check if the bird has hit the ground
    if flappy.rect.bottom >= 630 :
        game_over = True
        flying = False

    if game_over == False and flying == True:

        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency: #if the time now minus the last pipe is greater than the pipe frequency
            pipe_height = random.randint(-100, 100)
            bottom_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        #draw and scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()

    #check for game over and reset
    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and flying == False and game_over == False:
                flying = True

    pygame.display.update()

pygame.quit()