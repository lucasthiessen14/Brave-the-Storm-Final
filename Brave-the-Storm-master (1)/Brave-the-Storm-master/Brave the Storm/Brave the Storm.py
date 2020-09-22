#Player/Ufo image taken from: Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>

#Importing Libraries required for Game
import pygame
import random
import sys
import math
from pygame import mixer
import time

#Initializers for pygame and mixer libraries
mixer.init()
pygame.init()

#Background music for the game
mixer.music.load(".\\assets\\a.mp3")
mixer.music.play(-1)

#Visuals for game window
icon = pygame.image.load(".\\assets\\moon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Space Evade")
background = pygame.image.load(".\\assets\\space.jpg")

#Settings for text displayed on screen
myFont = pygame.font.SysFont("Comic Sans MS",35)
myFont2 = pygame.font.SysFont("Comic Sans MS",80)
text_color = (255,255,255)

#Sets the size of the game window
length = 800
height = 600
screen = pygame.display.set_mode((length,height))

#Main Menu
def mainMenu():
    menu = True

    while menu:
        screen.blit(background, (0,0))

        mouse = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        pygame.draw.rect(screen, (130,128,128), (300, 450, 200, 50))
        botton1 = myFont.render("Start", 1, (0,0,0))
        screen.blit(botton1, (350, 450))
        title = myFont2.render("Space Evade", 1, (255,255,255))
        screen.blit(title, (180, 200))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

        if 300+200 > mouse[0] > 300 and 450+50 > mouse[1] > 450:
            pygame.draw.rect(screen, (255,0,0), (300, 450, 200, 50), 2)
            if clicked[0] == 1:
                mainGame()
        else:
            pygame.draw.rect(screen, (0,0,0), (300, 450, 200, 50), 2)

        pygame.display.update()
#Function that contains all game functionability
def mainGame():

    #Main game functions e.g - level, score
    game_over = False
    score = 0
    level = 1
    clock = pygame.time.Clock()

    #Enemy initializers
    enemyImg = pygame.image.load(".\\assets\\asteroid.png")
    enemy_size = 60 - score/5
    num_enemies = 1
    enemy_pos = [random.randint(0,length-enemy_size), 0]
    enemy_list = [enemy_pos]
    enemy_speed = 10

    #Player initializers
    playerImg = pygame.image.load(".\\assets\\spaceship.png")
    player_size = 64
    player_pos = [length/2-32, int(height-2*player_size)]
    player_speed = int(.75*enemy_speed)
    pygame.key.set_repeat(10,10)


    ###Functions to create game entities###

    #Takes the player's game character, its position, and creates it - then displays it on the screen
    def player():
        screen.blit(playerImg, player_pos)

    #Takes the enemy's game character, its position, and creates it - then displays it on the screen
    def draw_enemies(enemy_list):
        for enemy_pos in enemy_list:
            screen.blit(enemyImg, enemy_pos)

    ###Functions for game entity movement

    #This function drops enemies randomly from the top of the screen if the number of enemies spawned is less than the limit
    def drop_enemies(enemy_list):
        delay = random.random()
        if len(enemy_list) < num_enemies and delay < 0.075:
            x_pos = random.randint(0,length-enemy_size)
            y_pos = 0
            enemy_list.append([x_pos,y_pos])


    ###Functions for main game functions

    #This function creates a level system based on the score the player has obtained
    def display_level(score, level):
        if score < 50:
            level = 1
        elif score < 150:
            level = 2
        elif score < 300:
            level = 3
        elif score < 500:
            level = 4
        else:
            level = 5
        return level

    #This function increases the speed of the enemies increasing the difficulty as the player achieves a higher score
    def set_difficulty(score, enemy_speed):

        enemy_speed = score/5 + 5
        return enemy_speed

    #This function increases the number of enemies dropping at a time increasing the difficulty as the player reaches a higher level/score
    def number_enemies(level,num_enemies):
        if level == 1:
            num_enemies = 10
        elif level == 2:
            num_enemies = 12
        elif level == 3:
            num_enemies = 14
        elif level == 4:
            num_enemies = 16
        else:
            num_enemies = 18

        return num_enemies


    ###Functions to update game entity positions###

    #This function checks to see if enemies are on the screen.  If the enemy is on screen its position is updated. Otherwise, it is removed from the list
    def update_enemy_positions(enemy_list, score):
        for idx, enemy_pos in enumerate(enemy_list):
            if enemy_pos[1] >= 0 and (enemy_pos[1]+enemy_size) < length:
                enemy_pos[1] += int(enemy_speed/2)
            else:
                enemy_list.pop(idx)
                score += 1
        return score


    ###Functions to evaluate collision checks between player and game entities###

    #The position of all the enemies on the screen is taken. For each enemy, checks whether any enemy collided with the player.
    def collision_check(enemy_list, player_pos):
        for enemy_pos in enemy_list:
            if detectCollision(player_pos, enemy_pos):
                return True
        return False

    #The position of the enemies and player are calculated relative to each other to check whether they have collided
    def detectCollision(player_pos, enemy_pos):
        p_x = player_pos[0]
        p_y = player_pos[1]

        e_x = enemy_pos[0]
        e_y = enemy_pos[1]

        if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
            if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
                return True
        return False

    #Main game loop
    while not game_over:

        screen.blit(background, (0,0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:

                x = player_pos[0]
                y = player_pos[1]

                if event.key == pygame.K_UP:
                    if player_pos[1] >= 64:
                        y -= player_speed
                elif event.key == pygame.K_DOWN:
                    if player_pos[1] <= 536:
                        y += player_speed
                elif event.key == pygame.K_RIGHT:
                    if player_pos[0] <= 736:
                        x += player_speed
                elif event.key == pygame.K_LEFT:
                    if player_pos[0] >= 0:
                        x -= player_speed

                player_pos = [x,y]

        clock.tick(30)

        player()

        drop_enemies(enemy_list)
        draw_enemies(enemy_list)
        num_enemies = number_enemies(level,num_enemies)
        score = update_enemy_positions(enemy_list, score)

        enemy_speed = set_difficulty(score, enemy_speed)
        level = display_level(score, level)

        text_level = "Level: " + str(level)
        text = "Score: " + str(score)
        label = myFont.render(text, 1, text_color)
        label_level = myFont.render(text_level, 1, text_color)

        screen.blit(label, (length-200,height-40))
        screen.blit(label_level, (length-200,(height - 80)))

        if collision_check(enemy_list, player_pos):
            game_over = True

        pygame.display.update()

mainMenu()
mainGame()
