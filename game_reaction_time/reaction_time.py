#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 14:27:40 2024

@author: ashwin_kr
"""

# make sure have install pygame module 

import pygame 
import sys
import random

# import every function from math module 
#from math import *
from math import sin, cos, radians
start_ticks = pygame.time.get_ticks()  # Starter tick

pygame.init()
# Initialize the mixer
pygame.mixer.init()

# Load the music file
pygame.mixer.music.load('inspiring-cinematic-ambient-116199.mp3')

shoot_sound = pygame.mixer.Sound('shoot-1-81135.mp3')
# Start playing the music
pygame.mixer.music.play(-1)

# here 500 means 500px
# setting the window width and height 
dimensions = (1000, 800)
width = dimensions[0]
height = dimensions[1]

display = pygame.display.set_mode(dimensions)
pygame.display.set_caption("shoot the balloon")

# will show how much time you have played the game 
clock = pygame.time.Clock()

# some css
margin = 100
lowerBound=100

# starting the game

score =0

#colors of the balloons

Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Yellow = (255, 255, 0)
Cyan = (0, 255, 255)
Magenta = (255, 0, 255)
Black = (0, 0, 0)
White = (255, 255, 255)
Gray = (128, 128, 128)
Orange = (255, 165, 0)
Purple = (128, 0, 128)
Brown = (165, 42, 42)
Pink = (255, 192, 203)
Lime = (0, 255, 0)
Teal = (0, 128, 128)
Base1={195, 94, 235}
Dis_col={235, 176, 94}

# setting up the font
font= pygame.font.SysFont("Verdana",25)
# defining information about balloon
class Balloon:
    def __init__(self,speed):
        self.a = random.randint(30,50) #generating random number between 30 and 50 to denote the size
        self.b = self.a + random.randint(0,10)

        # these are the coordinates of the balloon 
        self.x=random.randrange(margin,width-self.a-margin)
        self.y=height -lowerBound
        self.angle = 90  #the angle at which balloon will go up

        self.speed= -speed #this signifies the direction as it will go downward
        
        #this will denote the movement of the balloon 
        #-1 -- left  0 -- straight    1 -- right
        self.probPool = [-1,0,1,-1,0,1,1,0,-1]
        self.length= random.randint(50,100)
        self.color= random.choice([Red, Green, Yellow, Cyan, Magenta, Black, White, Gray, Orange, Purple, Brown, Pink, Lime, Teal])

    # fixing the movement of the balloon 
    def move(self):
        direct= random.choice(self.probPool)

        if direct == -1:
            self.angle +=-15  # move at angle of 15 degree
        elif direct == 0:
            self.angle +=0  #keep going straight
        else:
            self.angle+=15

        # denoting the movement -- y coordinate will increase according to the sin function while y coordinate according to the cos function 
        self.y+=self.speed*sin(radians(self.angle))
        self.x+=self.speed*cos(radians(self.angle))

        if(self.x+self.a >width) or(self.x<0):
            if self.y>height/5:
                # changing the direction
                self.x-= self.speed*cos(radians(self.angle))
            
            else:
                self.reset()
        
        # if its going up or down out of the display
        if self.y +self.b<0 or self.y >height+30:
            self.reset()
    
    #drawing the balloon 
    def show(self):
        pygame.draw.line(display,Black,(self.x+self.a/2,self.y+self.b),(self.x+self.a/2,height-lowerBound))
        pygame.draw.ellipse(display,self.color,(self.x,self.y,self.a,self.b))

    def burst(self):
        global score
        pos =pygame.mouse.get_pos()

        if onBalloon(self.x,self.y,self.a,self.b,pos):
            score+=1
 
            shoot_sound.play()
            pygame.time.wait(300)        
            self.reset()  #will make the another balloon 

    def reset(self):
        self.a = random.randint(10, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound
        self.angle = 90
        self.speed = -random.choice([1, 2, 3, 4])  # Randomize speed
        self.probPool = [-1, 0, 1, -1, 0, 1, 1, 0, -1]
        self.length = random.randint(50, 100)
        self.color = random.choice([Red, Green,  Yellow, Cyan, Magenta, Black, White, Gray, Orange, Purple, Brown, Pink, Lime, Teal])
        


balloons=[]
noBalloon=20

for i in range(noBalloon):
    obj=Balloon(random.choice([1,1,2,2,2,2,3,3,3,4]))  #this is the speed of the balloon
    balloons.append(obj)

def onBalloon(x,y,a,b,pos):
     if(x<pos[0]<x+a)and (y<pos[1]<y+b):
         return True
     else:
         return False
    # how the pointer will look like to kill the balloon -- its position is same as mouse
def pointer():
    pos=pygame.mouse.get_pos()
    r=25
    l=20
    color=Red

    for i in range(noBalloon):
        if onBalloon(balloons[i].x,balloons[i].y,balloons[i].a,balloons[i].b,pos):
            color=Green

    pygame.draw.ellipse(display,color,(pos[0]-r/2,pos[1]-r/2,r,r),4)
    pygame.draw.line(display,color,(pos[0],pos[1]-l/2),(pos[0],pos[1]-l),4)
    pygame.draw.line(display,color,(pos[0]+l/2,pos[1]),(pos[0]+l,pos[1]),4)
    pygame.draw.line(display,color,(pos[0],pos[1]+l/2),(pos[0],pos[1]+l),4)
    pygame.draw.line(display,color,(pos[0]-l/2,pos[1]),(pos[0]-l,pos[1]),4)

def lowerPlatform():
    pygame.draw.rect(display,Red,(0,height-lowerBound,width,lowerBound)) #drawing the rectangle to show 

def showScore():
    scoreText= font.render("Balloon Bursted : "+str(score),True,White)
    display.blit(scoreText,(150,height-lowerBound+50))
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # calculate how many seconds
    timer_text = font.render("Time: " + str(seconds), True, Green)
    display.blit(timer_text, (width - 250, height - lowerBound + 50))

def end_game_interface():
    display.fill(Black)
    score_text=font.render("Final Score: "+str(score),True,White)
    
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000 

    reaction_time = round(score/seconds,2)

    if reaction_time < 0.5:
        score_text_appreciate = font.render("Pupil Player: Reaction speed "+str(reaction_time),True,Black)
        display.fill(Green)
    elif reaction_time >=0.5 and reaction_time <=1:
        score_text_appreciate = font.render("Expert Player: Reaction speed "+str(reaction_time),True,Black)
        display.fill(Orange)
    else:
        score_text_appreciate = font.render("Master Player: Reaction speed "+str(reaction_time),True,Black)
        display.fill(Red)
    
    display.blit(score_text,(width //2-50 ,height //2))
    display.blit(score_text_appreciate,(width //2-110 ,height //2 +50))
    pygame.display.update()
    pygame.time.wait(3000)
# closing the game 
def close():
    end_game_interface()
    pygame.quit()
    sys.exit()

#initializing the all the elements of the game 
def game():
    global score
    
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                close()
            
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
               if keys[pygame.K_x]:
                 close()
          
            # to restart the game 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    close()

            #if you are clicking mouse button then check if is on balloon then burst
            #if clicking on the blank space dont do anything 
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range (noBalloon):
                    balloons[i].burst()

        display.fill(Blue)
        for i in range (noBalloon):
            balloons[i].show()

        pointer()

        for i in range (noBalloon):
            balloons[i].move()

        lowerPlatform()
        showScore()
        # keep doing the update
        pygame.display.update()

        #time is 60 ms
        clock.tick(40)
game()
