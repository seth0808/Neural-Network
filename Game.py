import pygame
import random 
from Nn import Nn
import math

class Game:

	#Game Attriutes
	gameOver = False
	pointValue = 0
	xO = 0
	yO = 0
	velO = 4
	widthO = 10
	heightO = 10
	width = 10
	height = 20
	vel = 1
	startingPos = 0
	#Pygame Font
	pygame.font.init()
	myfont = pygame.font.SysFont('Comic Sans MS', 20)

	#Initialize a new Game
	#Create a NN for the game and begin
	def __init__(self, x, y, win):
		self.win = win
		self.x = x + 50
		self.y = y
		self.startingPos = x
		self.resetObstacle()
		self.Nn = Nn(win, x, y)

	#Track and print point values
	def points(self):
		if self.gameOver == False:
			self.pointValue += 1
		textsurface = self.myfont.render(str(self.pointValue), False, (255, 255, 255))
		self.win.blit(textsurface,(self.startingPos + 5,self.y - 80))

	#Identification for the parent game copy
	def parent(self):
		textsurface = self.myfont.render("P", False, (255, 255, 255))
		self.win.blit(textsurface,(self.startingPos + 90,self.y - 80))
		
	#Display the NN
	def drawNet(self):
		self.Nn.drawGraph()

	#Pygame procedure for displaying the game componenets (player)
	#Highlight green if currently leading in fitness
	def draw(self, best):
		if self.gameOver == False:
			if best == 1:
				pygame.draw.rect(self.win, (0, 255, 0), (self.x, self.y, self.width, self.height))
			else:
				pygame.draw.rect(self.win, (255, 0, 0), (self.x, self.y, self.width, self.height))
			return True
		else:
			return False

	#Pygame procedure for displaying the game componenets (obstacle)
	def drawObstacle(self):
		if self.gameOver == False:
			pygame.draw.rect(self.win, (0, 0, 255), (self.xO, self.yO, self.widthO, self.heightO))
			#Change position
			self.yO += self.velO

	#Reset the obstacle's position
	def resetObstacle(self):
		self.xO = random.randint(self.startingPos, self.startingPos + 90)
		self.yO = self.y - 90

	#Check and handling for a collision 
	def obstacleCollision(self):
		if self.yO + 10 >= self.y:
			if self.xO + 10 >= self.x and self.xO <= self.x:
				self.gameOver = True
				self.Nn.amend(-1)
			elif self.xO <= self.x + 10 and self.xO + 10  >= self.x + 10:
				self.gameOver = True
				self.Nn.amend(-1)

	#Function was used for keyboard
	#def keyPressed(self, direction):
		#if direction == -1:
			#self.x-=self.vel
		#else:
			#self.x+=self.vel

	#Insert inputs from the game parameters into the game's specific NN		
	def operate(self):
		#Prepare the values
		if self.gameOver == False:
			firstParam = self.x-(self.startingPos)

			secondParam = self.xO-self.startingPos

			thirdParam = (self.yO+100)-self.y

			#normalize
			sum = firstParam + secondParam + thirdParam + 0.00001

			value = self.Nn.operate(firstParam/sum, secondParam/sum, thirdParam/sum)
			#The result from the NN determines in which direction the player travels
			if value == -1:
				self.x -= self.vel
			else:
				self.x += self.vel

	#Start a new game (NN is untouched)
	#Returns the score from the game for evaluation by Main.py
	def restart(self):
		self.x = self.startingPos + 50
		self.resetObstacle()
		self.gameOver = False
		returnScore = self.pointValue
		self.pointValue = 0
		return returnScore 

	#Check and handle for a wall collision
	def wallCollision(self):
		if self.x < self.startingPos:
			self.Nn.amend(-1)
			self.gameOver = True
		elif self.x > self.startingPos + 90:
			self.gameOver = True
			self.Nn.amend(-1)

		if self.yO > self.y + 20:
			self.resetObstacle()
			self.Nn.amend(1)

	#Create a deep copy of the Game for the child copies
	def mutantCopy(self, x, y, win):
		mutant = Game(x, y, win)
		mutant.setNN(self.Nn, x, y, win)

		#TODO:
		#Create Mutations
		
		return mutant

	#Getters and Setters
	#Set: NN
	#Get: startinPos, y-value
	def setNN(self, net, x, y, win):
		self.Nn = net.copy(x, y, win)

	def getStartingPos(self):
		return self.startingPos

	def getYValue(self):
		return self.y
