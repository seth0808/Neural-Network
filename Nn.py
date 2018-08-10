from Graph import Graph
import pygame

class Nn:
	#Pygame Font
	pygame.font.init()
	myfont = pygame.font.SysFont('Comic Sans MS', 20)

	#Initialize the NN
	def __init__(self, win, x, y):

		#These method calls create a 3x4x2 (1 hidden layer) NN
		#And establishes all of the connections between them
		self.graph = Graph(x, y, win)

		self.graph.addNeuronAfter(0)
		self.graph.addNeuronAfter(0)
		self.graph.addNeuronAfter(0)
		self.graph.addNeuronAfter(0)

		self.graph.addNeuronAfter(3)
		self.graph.addNeuronAfter(3)

		
		self.graph.connectNeuronToInput(1, 3)
		self.graph.connectNeuronToInput(1, 4)
		self.graph.connectNeuronToInput(1, 5)
		self.graph.connectNeuronToInput(1, 6)

		self.graph.connectNeuronToInput(2, 3)
		self.graph.connectNeuronToInput(2, 4)
		self.graph.connectNeuronToInput(2, 5)
		self.graph.connectNeuronToInput(2, 6)

		self.graph.connectNeuronToInput(3, 7)
		self.graph.connectNeuronToInput(3, 8)

		self.graph.connectNeuronToInput(4, 7)
		self.graph.connectNeuronToInput(4, 8)

		self.graph.connectNeuronToInput(5, 7)
		self.graph.connectNeuronToInput(5, 8)

		self.graph.connectNeuronToInput(6, 7)
		self.graph.connectNeuronToInput(6, 8)

		
		self.win = win


	def operate(self, x, xO, yO):
		return self.graph.operate(x, xO, yO)
		
	def drawGraph(self):
		self.graph.display()

	def amend(self, direction):
		self.graph.fixWeights(direction)

	#Create a deep copy of the NN
	def copy(self, x, y, win):
		net = Nn(win, x, y)
		net.setGraph(self.graph, x, y, win)
		return net
	
	#Getters and Setters
	#Set: Graph
	#Get:
	def setGraph(self, newGraph, x, y, win):
		self.graph = newGraph.copy(x, y, win)
