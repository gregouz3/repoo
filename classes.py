"""Classes du jeu de labyrinthe Mac Gyver"""

import pygame
import random
from pygame.locals import * 
from constantes import *

class Niveau:
	"""Classe permettant de créer un niveau"""
	def __init__(self, fichier):
		self.fichier = fichier
		self.structure = 0
		
	def generer(self):
		"""Méthode permettant de générer le niveau en fonction du fichier.
		On crée une liste générale, contenant une liste par ligne à afficher"""	
		
		#initialisation du nombre collectable d'items
		obj_num =1
		#On ouvre le fichier
		with open(self.fichier, "r") as fichier:
			structure_niveau = []
			#On parcourt les lignes du fichier
			for ligne in fichier:
				ligne_niveau = []
				#On parcourt les sprites (lettres) contenus dans le fichier
				for sprite in ligne:
					#On ignore les "\n" de fin de ligne
					if sprite != '\n':
						#On ajoute le sprite à la liste de la ligne
						ligne_niveau.append(sprite)
				#On ajoute la ligne à la liste du niveau
				structure_niveau.append(ligne_niveau)
				# Placez les éléments au hasard, mais uniquement sur le carré 
				#contenant '0': nous ne voulons pas d'éléments dans un mur
		while obj_num < 4:
			random_x = random.randint(0, nombre_sprite_cote - 1)
			random_y = random.randint(0, nombre_sprite_cote - 1)
			#verif de la disponibilité de la case
			if structure_niveau[random_y][random_x] == '0':
				structure_niveau[random_y][random_x] = str(obj_num)
				obj_num += 1

			#On sauvegarde cette structure
			self.structure = structure_niveau
	
	def afficher(self, fenetre):
		"""Méthode permettant d'afficher le niveau en fonction 
		de la liste de structure renvoyée par generer()"""
		#Chargement des images #reajustement des images 
		mur = pygame.image.load(image_mur).convert()
		mur = pygame.transform.scale(mur, (50,50))
		depart = pygame.image.load(image_depart).convert_alpha()
		depart = pygame.transform.scale(depart, (50, 50))
		arrivee = pygame.image.load(image_arrivee).convert_alpha()
		arrivee = pygame.transform.scale(arrivee, (50,50))
		item0 = pygame.image.load(tube_plastique).convert()
		item0 = pygame.transform.scale(item0, (50,50))
		item0.set_colorkey((255, 255, 255))
		item1 = pygame.image.load(ether).convert_alpha()
		item1 = pygame.transform.scale(item1, (50, 50))
		item2 = pygame.image.load(aiguille).convert()
		item2.set_colorkey((0,0,0))
		item2 = pygame.transform.scale(item2, (50, 50)) 
		
		#On parcourt la liste du niveau
		num_ligne = 0
		for ligne in self.structure:
			#On parcourt les listes de lignes
			num_case = 0
			for sprite in ligne:
				#On calcule la position réelle en pixels
				x = num_case * taille_sprite
				y = num_ligne * taille_sprite
				if sprite == 'm':		   #m = Mur
					fenetre.blit(mur, (x,y))
				if sprite == 'd':		   #d = Départ
					fenetre.blit(depart, (x,y))
				if sprite == 'a':		   #a = Arrivée
					fenetre.blit(arrivee, (x,y))
				if sprite == '1':
					fenetre.blit(item0, (x,y))
				if sprite == '2':
					fenetre.blit(item1, (x,y))
				if sprite == '3':
					fenetre.blit(item2, (x,y))
				num_case += 1
			num_ligne += 1


class Perso:
	"""Classe permettant de créer un personnage"""
	def __init__(self, MacGyver, niveau):
		#Sprites du personnage
		self.MacGyver = pygame.image.load(MacGyver).convert_alpha()
		self.MacGyver = pygame.transform.scale(self.MacGyver, (50, 50))

		#Position du personnage en cases et en pixels
		self.case_x = 0
		self.case_y = 0
		self.x = 0
		self.y = 0

		self.direction = self.MacGyver

		#Niveau dans lequel le personnage se trouve 
		self.niveau = niveau
		self.basket = []
	
	def deplacer(self, direction):
		"""Methode permettant de déplacer le personnage"""
		
		# contient les items collectés, vide pour le moment
		basket_content = 0
		#Déplacement vers la droite
		if direction == 'droite':
			#Pour ne pas dépasser l'écran
			if self.case_x < (nombre_sprite_cote - 1):
				#On vérifie que la case de destination n'est pas un mur
				if self.niveau.structure[self.case_y][self.case_x+1] != 'm':
					#Déplacement d'une case
					self.case_x += 1
					#Calcul de la position "réelle" en pixel
					self.x = self.case_x * taille_sprite
					item = self.niveau.structure[self.case_y][self.case_x]
					#on remplit items
					if item != '0' and item != 'd' and item != 'a' and item != '':
						basket_content = item
						self.niveau.structure[self.case_y][self.case_x] = '0'

		#Déplacement vers la gauche
		elif direction == 'gauche':
			if self.case_x > 0:
				if self.niveau.structure[self.case_y][self.case_x-1] != 'm':
					self.case_x -= 1
					self.x = self.case_x * taille_sprite
					item = self.niveau.structure[self.case_y][self.case_x]
					#on remplit items
					if item != '0' and item != 'd' and item != 'a' and item != '':
						basket_content = item
						self.niveau.structure[self.case_y][self.case_x] = '0'

		#Déplacement vers le haut
		elif direction == 'haut':
			if self.case_y > 0:
				if self.niveau.structure[self.case_y-1][self.case_x] != 'm':
					self.case_y -= 1
					self.y = self.case_y * taille_sprite
					item = self.niveau.structure[self.case_y][self.case_x]
					#on remplit items
					if item != '0' and item != 'd' and item != 'a' and item != '':
						basket_content = item
						self.niveau.structure[self.case_y][self.case_x] = '0'
		
		#Déplacement vers le bas
		elif direction == 'bas':
			if self.case_y < (nombre_sprite_cote - 1):
				if self.niveau.structure[self.case_y+1][self.case_x] != 'm':
					self.case_y += 1
					self.y = self.case_y * taille_sprite
					item = self.niveau.structure[self.case_y][self.case_x]
					#on remplit items
					if item != '0' and item != 'd' and item != 'a' and item != '':
						basket_content = item
						self.niveau.structure[self.case_y][self.case_x] = '0'
		
		if basket_content != 0 and basket_content != 'd' and basket_content != 'a':
			self.basket.append(basket_content)


