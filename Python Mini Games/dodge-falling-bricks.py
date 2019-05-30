# -*- coding: utf-8 -*-
"""
Created on Wed May 29 14:57:47 2019

@author: NEO
"""

import pygame
import sys
import random
import math
#first initialize pygame
pygame.init()

#init varibales
width = 800 #width of screen
height = 600 #height of screen
player_color = (255, 0, 0) #RGB values for any color
enemy_color = (0 , 0, 255) 
yellow = (255, 255, 0)
background_color = (0, 0, 0)
player_size = [50, 50] #size of rectangle
player_pos = [width/2, height - (2*player_size[0])] #position of rectangle
enemy_size = [50 , 50]
enemy_pos = [random.randint(0, width - enemy_size[0]), 0 ]
enemy_list = [enemy_pos] #list of enemy positions
speed = 10 #set initial speed
score = 0 #set initial score to 0
clock = pygame.time.Clock() ##define clock to control speed and framerate
game_over = False #init game_over to False in begining
myFont = pygame.font.SysFont("monospace", 35) #font to display the score

#create a screen by passing a tuple of width and height to set_mode
screen = pygame.display.set_mode((width, height))


#defining functions to control the dynamics of rectangles
def set_level(score, speed):
    """This function takes the score of the player 
    and changes the value of speed variable to increase the level.
    Returns the new speed"""
    if score < 20:
        speed = 3
    elif score < 50:
        speed = 5
    elif score < 70:
        speed = 10
    elif score < 100:
        speed = 15
    return speed


def drop_enemies(enemy_list):
    """This function takes the enemy list as input 
    and drop the enemies at random durations from the top of screen"""
    delay = random.random() #generates a random ffloat value b/w 0-1
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0 , width-enemy_size[0]) #random x position of new rectangle
        y_pos = 0 #y position of new rectangle
        enemy_list.append([x_pos, y_pos]) #append the x-y positions to the list
        
def draw_enemies(enemy_list):
    """This fucntion takes the enemy list and uses the x and y positions to display the rectangles on the screen.
    Also uses the other parameters for drawing the rectangles."""
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen , enemy_color , (enemy_pos[0], enemy_pos[1], enemy_size[0], enemy_size[1]))    


def update_enemy_pos(enemy_list, score):
    """This function takes the enemy list and score as in-params 
    and changes the enemy position on the screen"""
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >=0 and enemy_pos[1] < height: 
            enemy_pos[1]+=speed #if rectangle is between the sceen, set y postion to speed
        else:
            enemy_list.pop(idx) #if rectangle is not between screen then remove it from the list
            score+=1 #increase score by 1 whenever a rectngle passes the screen
    return score

def collision_check(enemy_list, player_pos):
    """This function takes in the enemy list and player position and checks if the x-position and y position of enemy 
    and player are overlapping which would mean a collision"""
    for enemy_pos in enemy_list:
        if detect_collision( enemy_pos, player_pos):
            return True
    return False


def detect_collision(enemy_pos, player_pos):
    """This fucntion matches the x pos and y pos of player and enemy rectangles"""
    p_x = player_pos[0]
    p_y = player_pos[1]
    e_x = enemy_pos[0]
    e_y = enemy_pos[1]
    
    if (e_x > p_x and e_x < (p_x + player_size[0])) or ( p_x > e_x and p_x < (e_x + enemy_size[0])):
        if (e_y > p_y and e_y < (p_y + player_size[1])) or (p_y > e_y and p_y < (e_y + enemy_size[1])):
            return True
    return False



#while game is not over
while not game_over:
    # events occusring during the pygame window
    for event in pygame.event.get():
        print(event)
        # if my event is Quit, exit out of pygame.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        #track movement of rectangle
        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]
            if event.key == pygame.K_RIGHT:
                x+=player_size[0]
            elif event.key == pygame.K_LEFT:
                x-=player_size[0]
            player_pos = [x,y]
    
    #fill screen with black every time the block moves
    screen.fill(background_color)
    #calling the functions
    drop_enemies(enemy_list)
    score = update_enemy_pos(enemy_list, score)
    speed = set_level(score, speed)
    text = "Score:" + str(score)
    label = myFont.render(text, 1, yellow)
    screen.blit(label, (width-200, height-40))
    if collision_check(enemy_list, player_pos):
        game_over = True
        break
    draw_enemies(enemy_list)
    #draw player rectangle
    pygame.draw.rect(screen , player_color , (player_pos[0], player_pos[1], player_size[0], player_size[1]))
    #update 30sec FPS
    clock.tick(30)
    #update the display window to render
    pygame.display.update()