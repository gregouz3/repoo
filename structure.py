#!/usr/bin/python3

# -*- coding: Utf-8 -*

"""
MacGyver Labyrinth Game :
Game in which we must move MacGyver to the Guardian throught a labyrinth . 
MacGyver must absolutely recover the three tools if he wants to be able to lull the Guardian .
Script Python
Files : structure.py, classes.py, constantes.py n1 ressource/pictures
"""

import pygame
import time
from pygame.locals import *
from classes import *
from constantes import *

pygame.init()
#Open the Pygame window 
window = pygame.display.set_mode((slide_window, slide_window))
#Slow the game icon 
icon = pygame.image.load(picture_icon)
pygame.display.set_icon(icon)
#Slow the game title 
pygame.display.set_caption(title_window)

#Main loop
game = 1
while game:	
	#Loading and viewing the home screen 
	home = pygame.image.load(picture_home).convert()
	home = pygame.transform.scale(home, (750, 750))
	window.blit(home, (0,0))
	#Refresh
	pygame.display.flip()
	#These variables are reset to 1 at each loop turn
	game_game = 1
	game_home = 1

	#Home loop
	while game_home:
		#Limit speed limitation
		pygame.time.Clock().tick(30)
		for event in pygame.event.get():
			#If the user leaves, we close the game
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				game_home = 0
				game_game = 0
				game = 0
				#Variable choice of level
				choice = 0
			elif event.type == KEYDOWN:				
				#Launch of level 1
				if event.key == K_RETURN:
					game_home = 0
					choice = 'n1'		
	#We check that the player has made a level choice				
	if choice != 0:
		#Loading the background
		background = pygame.image.load(picture_background).convert()
		background = pygame.transform.scale(background, (750, 750))
		#Generate a level from a file
		level = Level(choice)
		level.generate()
		level.display(window)
		#Creation of MacGyver
		mg = Character("ressource/MacGyver.png", level)
		#Accelerate if the arrows keys are pressed
		pygame.key.set_repeat(400, 30)

	#Game loop
	while game_game:
		pygame.time.Clock().tick(30)	
		for event in pygame.event.get():
			if event.type == QUIT:
				game_game = 0
				game = 0

			elif event.type == KEYDOWN:
				#If the user press Esc here, we return only to the home
				if event.key == K_ESCAPE:
					game_game = 0				
				#MacGyver moving keys	
				elif event.key == K_RIGHT:
					mg.move('right')
				elif event.key == K_LEFT:
					mg.move('left')
				elif event.key == K_UP:
					mg.move('up')
				elif event.key == K_DOWN:
					mg.move('down')			
				#Display to news positions
				window.blit(background, (0,0))
				level.display(window)
				window.blit(mg.direction, (mg.x, mg.y))
				pygame.display.flip()

			#Item management
			item_list = mg.basket
			for (i, item) in enumerate(item_list):
				if item == '1':
					item_list[i] = 'plastic tube'
				elif item == '2':
					item_list[i] = 'ether'
				elif item == '3':
					item_list[i] = 'needle'

			#If MacGyver arrives at the guardian
			if level.structure[mg.square_y][mg.square_x] == 'a':
				#And that he rammed up all the objects
				if len(mg.basket) == 3:
					#WIN
					syringe = pygame.image.load(picture_syringe).convert_alpha()
					syringe = pygame.transform.scale(syringe, (750, 750))
					#Display animation
					window.blit(syringe, (0, 0))
					pygame.display.flip()
					#Wait 5s
					time.sleep(5)
					winner = pygame.image.load(picture_win).convert()
					winner = pygame.transform.scale(winner, (750, 750))
					#Display victory message	
					window.blit(winner, (0, 0))
					pygame.display.flip()
					#Wait 2s
					time.sleep(2)
					#Back to the home
					game_game = 0
				else:
					#LOOSE
					death = pygame.image.load(picture_death).convert()
					death = pygame.transform.scale(death, (750, 750))
					#Display animation
					window.blit(death, (0, 0))
					pygame.display.flip()
					#Wait 2s
					time.sleep(2)
					looser = pygame.image.load(picture_loose).convert()
					looser = pygame.transform.scale(looser, (750, 750))
					#Display defeat message
					window.blit(looser, (0, 0))
					pygame.display.flip()
					#Wait 5s
					time.sleep(5)
					#Back to the home
					game_game = 0


