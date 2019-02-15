#!/usr/bin/python3

# -*- coding: Utf-8 -*

"""
MacGyver Labyrinth Game :
Game in which we must move MacGyver to the Guardian throught a labyrinth.
MacGyver must absolutely recover the three tools if he wants to be able to lull the Guardian .
Script Python
Files : structure.py, classes.py, constantes.py n1 ressource/pictures
"""

import time
import pygame
from pygame.locals import *
from classes import *
from constants import *

def launch_the_labyrinth():
    """Game launch function"""

    pygame.init()
	  #Open the Pygame window
    window = pygame.display.set_mode((SLIDE_WINDOW, SLIDE_WINDOW))
	  #Slow the game icon
    icon = pygame.image.load(PICTURE_ICON)
    pygame.display.set_icon(icon)
	  #Slow the game title
    pygame.display.set_caption(TITLE_WINDOW)

	  #Main loop
    game = True
    while game:
	      #Loading and viewing the home screen
        home = pygame.image.load(PICTURE_HOME).convert()
        home = pygame.transform.scale(home, (750, 750))
        window.blit(home, (0, 0))
		    #Refresh
        pygame.display.flip()
		    #These variables are reset to 1 at each loop turn
        game_game = True
        game_home = True

		    #Home loop
        while game_home:
			      #Limit speed limitation
            pygame.time.Clock().tick(30)
            for event in pygame.event.get():
				        #If the user leaves, we close the game
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    game_home, game_game, game = False, False, False
					          #Variable choice of level
                    choice = 0
                elif event.type == KEYDOWN:
				            #Launch of level 1
                    if event.key == K_RETURN:
                        game_home = False
                        choice = 'n1'
		    #We check that the player has made a level choice
        if choice != 0:
			      #Loading the background
            background = pygame.image.load(PICTURE_BACKGROUND).convert()
            background = pygame.transform.scale(background, (750, 750))
			      #Generate a level from a file
            level = Level(choice)
            level.generate()
            level.display(window)
			      #Creation of MacGyver
            macgyver = Character("ressource/MacGyver.png", level)
			      #Accelerate if the arrows keys are pressed
            pygame.key.set_repeat(400, 30)

		    #Game loop
        while game_game:
            pygame.time.Clock().tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_game, game = False, False

                elif event.type == KEYDOWN:
					          #If the user press Esc here, we return only to the home
                    if event.key == K_ESCAPE:
                        game_game = False
					          #MacGyver moving keys
                    elif event.key == K_RIGHT:
                        macgyver.move('right')
                    elif event.key == K_LEFT:
                        macgyver.move('left')
                    elif event.key == K_UP:
                        macgyver.move('up')
                    elif event.key == K_DOWN:
                        macgyver.move('down')
					          #Display to news positions
                    window.blit(background, (0, 0))
                    level.display(window)
                    window.blit(macgyver.direction, (macgyver.pos_x, macgyver.pos_y))
                    pygame.display.flip()

				        #Item management
                item_list = macgyver.basket
                for (i, item) in enumerate(item_list):
                    if item == '1':
                        item_list[i] = 'plastic tube'
                    elif item == '2':
                        item_list[i] = 'ether'
                    elif item == '3':
                        item_list[i] = 'needle'

				        #Display item's collected
                if len(macgyver.basket) == 1:
                    one_item = pygame.image.load(ONE_ITEM).convert_alpha()
                    one_item = pygame.transform.scale(one_item, (300, 200))
                    window.blit(one_item, (450, 50))
                    pygame.display.flip()

                if len(macgyver.basket) == 2:
                    two_items = pygame.image.load(TWO_ITEMS).convert_alpha()
                    two_items = pygame.transform.scale(two_items, (300, 200))
                    window.blit(two_items, (450, 50))
                    pygame.display.flip()

                if len(macgyver.basket) == 3:
                    three_items = pygame.image.load(THREE_ITEMS).convert_alpha()
                    three_items = pygame.transform.scale(three_items, (300, 200))
                    window.blit(three_items, (450, 50))
                    pygame.display.flip()

								#If MacGyver arrives at the guardian
                if level.structure[macgyver.square_y][macgyver.square_x] == 'a':
								    #And that he rammed up all the objects
                    if len(macgyver.basket) == 3:
										    #WIN
                        syringe = pygame.image.load(PICTURE_SYRINGE).convert_alpha()
                        syringe = pygame.transform.scale(syringe, (750, 750))
										    #Display animation
                        window.blit(syringe, (0, 0))
                        pygame.display.flip()
										    #Wait 5s
                        time.sleep(5)
                        winner = pygame.image.load(PICTURE_WIN).convert()
                        winner = pygame.transform.scale(winner, (750, 750))
									     	#Display victory message
                        window.blit(winner, (0, 0))
                        pygame.display.flip()
										    #Wait 2s
                        time.sleep(2)
										    #Back to the home
                        game_game = False
                    else:
				                #LOOSE
                        death = pygame.image.load(PICTURE_DEATH).convert()
                        death = pygame.transform.scale(death, (750, 750))
										    #Display animation
                        window.blit(death, (0, 0))
                        pygame.display.flip()
										    #Wait 2s
                        time.sleep(2)
                        looser = pygame.image.load(PICTURE_LOOSE).convert()
                        looser = pygame.transform.scale(looser, (750, 750))
										    #Display defeat message
                        window.blit(looser, (0, 0))
                        pygame.display.flip()
										    #Wait 5s
                        time.sleep(5)
										    #Back to the home
                        game_game = False

if __name__ == "__main__":
    launch_the_labyrinth()
