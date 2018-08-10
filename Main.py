import pygame
import random 
from Game import Game
from Nn import Nn

#Initialize Pygame#
pygame.init()
win = pygame.display.set_mode((501, 600))
pygame.display.set_caption("game")
pygame.font.init()

#Set the game positions#
games=[]
for i in range(0, 5):
	for j in range(0, 5):
		x = (i*100)
		y = (j*100) + 80
		g = Game(x, y, win)
		games.append(g)


#GUI Attributes
run = True
display = [1, 0]
currentBest = 0
count = 0
parent = -1
gen = 0
trial = 0

while run:
	#Event Handelers
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_g:
				if display[0] == 1:
					display = [0, 1]
				else:
					display = [1, 0]
			if event.key == pygame.K_r:
				for i in range(0, 25):
					games[i].restart()
			if event.key == pygame.K_n:
				for i in range(0, 25):
					games[i].restart()

	#For previous keyboard involvement
	#keys = pygame.key.get_pressed()
	#if keys[pygame.K_LEFT]:
		#for i in range(0, 25):
			#games[i].keyPressed(-1)
	#if keys[pygame.K_RIGHT]:
		#for i in range(0, 25):
			#games[i].keyPressed(1)
		

	#Display
	win.fill(0)
	for i in range(0, 6):
		for j in range(0, 5):
			pygame.draw.rect(win, (0, 0, 255), (i*100, j*100, 1, 100))

	for i in range(0, 6):
		for j in range(0, 6):
			pygame.draw.rect(win, (255, 0, 0), (i*100, j*100, 100, 1))


	if display[0] == 1:
		#Display the Game
		
		oneIsStillPlaying = False
		for i in range(0, 25):
			games[i].operate()
			games[i].wallCollision()
			games[i].obstacleCollision()
			if i == currentBest:
				if games[i].draw(1) == True:
					oneIsStillPlaying = True
			else:
				if games[i].draw(0) == True:
					oneIsStillPlaying = True
			if parent != -1 and i == parent:
				games[i].parent()
			games[i].drawObstacle()
			games[i].points()
		if count == 5:
			currentBestScore = 0
			count = 0
		count+=1
		if oneIsStillPlaying == False:
			for i in range(0, 25):
				best = games[i].restart()
				if currentBestScore < best:
					currentBestScore = best
					currentBest = i
			trial += 1
		if trial == 100:
			trial = 0
			gen += 1
			parent = currentBest
			for i in range(0, 25):
				if i != parent:
					games[i] = games[parent].mutantCopy(games[i].getStartingPos(), games[i].getYValue(), win)

	elif display[1] == 1:
		#Display the Graph
		for i in range(0, 25):
			games[i].drawNet()

	#Further Display
	myfont = pygame.font.SysFont('arial', 25)
	textsurface = myfont.render("Toggle Game/Graph with [g]       Gen:  " + str(gen) + "  Trial:  " + str(trial), False, (255, 255, 255))
	win.blit(textsurface,(0, 520))
	pygame.display.update()
