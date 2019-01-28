"""MacGyver Labyrinth Game Classes"""

import pygame
import random
from pygame.locals import * 
from constantes import *

class Level:
	"""Class to create a level."""
	def __init__(self, file):
		self.file = file
		self.structure = 0
		
	def generate(self):
		"""Method to generate the level based on the file.We create a general list,
		containing a list by line to display."""
		
		#initialization of the collectable number of items
		obj_num =1
		#Open the file 
		with open(self.file, "r") as file:
			structure_level = []
			#We browse the lines of the file
			for line in file:
				line_level = []
				#We browse the sprites (letters) contained in the file
				for sprite in line:
					#We ignore the end of line "\n"
					if sprite != '\n':
						#We add the sprite to the list of the line
						line_level.append(sprite)
				#We add the line to the level list
				structure_level.append(line_level)
		#Place items randomy, but only on the square containing '0'
		while obj_num < 4:
			random_x = random.randint(0, number_sprite_slide - 1)
			random_y = random.randint(0, number_sprite_slide - 1)
			#Check the availability of the box
			if structure_level[random_y][random_x] == '0':
				structure_level[random_y][random_x] = str(obj_num)
				obj_num += 1
			#We safeguard this structure 
			self.structure = structure_level
	
	def display(self, window):
		"""Method to display the level according to the structure list returned by generate()."""
		
		#Loading images
		#Readjusting images 
		wall = pygame.image.load(picture_wall).convert()
		wall = pygame.transform.scale(wall, (50,50))

		start = pygame.image.load(picture_start).convert_alpha()
		start = pygame.transform.scale(start, (50, 50))

		advent = pygame.image.load(picture_advent).convert_alpha()
		advent = pygame.transform.scale(advent, (50,50))

		item0 = pygame.image.load(plastic_tube).convert()
		item0 = pygame.transform.scale(item0, (50,50))
		item0.set_colorkey((255, 255, 255))
		
		item1 = pygame.image.load(ether).convert_alpha()
		item1 = pygame.transform.scale(item1, (50, 50))
		
		item2 = pygame.image.load(needle).convert()
		item2.set_colorkey((0,0,0))
		item2 = pygame.transform.scale(item2, (50, 50)) 
		
		#We browse the level list
		num_line = 0
		for line in self.structure:
			#We browse list of lines
			num_square = 0
			for sprite in line:
				#The actual position in pixels is calculated
				x = num_square * width_sprite
				y = num_line * width_sprite
				#m = Wall
				if sprite == 'm':		   
					window.blit(wall, (x,y))
				#d = Start	
				if sprite == 'd':		   
					window.blit(start, (x,y))
				#a = Advent	
				if sprite == 'a':		   
					window.blit(advent, (x,y))
				#Items
				if sprite == '1':
					window.blit(item0, (x,y))
				if sprite == '2':
					window.blit(item1, (x,y))
				if sprite == '3':
					window.blit(item2, (x,y))
				#We increment the squares and lines	
				num_square += 1
			num_line += 1


class Character:
	"""Class to create a character."""
	def __init__(self, MacGyver, level):
		#Sprites of the character
		self.MacGyver = pygame.image.load(MacGyver).convert_alpha()
		self.MacGyver = pygame.transform.scale(self.MacGyver, (50, 50))
		#Position of the character in squares and pixels
		self.square_x = 0
		self.square_y = 0
		self.x = 0
		self.y = 0

		self.direction = self.MacGyver
		#Level in which the character is located 
		self.level = level
		#Creation list of items
		self.basket = []
	
	def move(self, direction):
		"""Method to move the character"""

		#Contains the rammed items, initialized to 0
		basket_content = 0
		#Move to the right
		if direction == 'right':
			#To not exceed the screen
			if self.square_x < (number_sprite_slide - 1):
				#Check that the destination square is not a wall
				if self.level.structure[self.square_y][self.square_x+1] != 'm':
					#Moving a square
					self.square_x += 1
					#Calculation of the "real" pixel position
					self.x = self.square_x * width_sprite
					item = self.level.structure[self.square_y][self.square_x]
					#We fill in the list of items 
					if item != '0' and item != 'd' and item != 'a' and item != '':
						basket_content = item
						self.level.structure[self.square_y][self.square_x] = '0'

		#Move to the left
		elif direction == 'left':
			if self.square_x > 0:
				if self.level.structure[self.square_y][self.square_x-1] != 'm':
					self.square_x -= 1
					self.x = self.square_x * width_sprite
					item = self.level.structure[self.square_y][self.square_x]
					if item != '0' and item != 'd' and item != 'a' and item != '':
						basket_content = item
						self.level.structure[self.square_y][self.square_x] = '0'

		#Moving up
		elif direction == 'up':
			if self.square_y > 0:
				if self.level.structure[self.square_y-1][self.square_x] != 'm':
					self.square_y -= 1
					self.y = self.square_y * width_sprite
					item = self.level.structure[self.square_y][self.square_x]
					if item != '0' and item != 'd' and item != 'a' and item != '':
						basket_content = item
						self.level.structure[self.square_y][self.square_x] = '0'
		
		#Moving down
		elif direction == 'down':
			if self.square_y < (number_sprite_slide - 1):
				if self.level.structure[self.square_y+1][self.square_x] != 'm':
					self.square_y += 1
					self.y = self.square_y * width_sprite
					item = self.level.structure[self.square_y][self.square_x]
					if item != '0' and item != 'd' and item != 'a' and item != '':
						basket_content = item
						self.level.structure[self.square_y][self.square_x] = '0'
		#The items collected are added to the list
		if basket_content != 0 and basket_content != 'd' and basket_content != 'a':
			self.basket.append(basket_content)


