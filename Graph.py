import random
import math
import pygame

class Weight:

	#Initialize a new Weight
	#These represent the connections between Neurons
	def __init__(self, setValue):
		if setValue == -1:
			self.value = random.random()
		else:
			self.value = setValue

	#Alter the weight value based on the feedack
	def change(self, direction):
		if direction == 1:
			self.value += 0.002
		else:
			self.value -= 0.002

	#Create a deep copy of the Weight
	def copy(self):
		return Weight(self.value)

	#Getters and Setters
	#Set
	#Get: value

	def getValue(self):
		return self.value

class Neuron:
	#Biases neurons are equivalent and present in all neurons
	bias = 1

	#Initialize a new Neuron
	#Set the outputValue if the Neuron is only intended as an input
	#Otherwise leave teh outputValue as zero
	def __init__(self, inputs, num, layer, outputValue):
		if outputValue == 0:
			self.inputs = inputs
			self.num = num
			self.layer = layer
			self.output=0
		else:
			self.num = num
			self.output = outputValue
	
	#Perform the operation of the Neuron
	#Sigm(sum(input*weight)+bias)->outputValue
	def operate(self):

		sum = 0
		for i in range(0, len(self.inputs)):
			sum += (self.inputs[i][0].getOutput() * self.inputs[i][1].getValue())
		
		preActivation = sum #TODO: Why does adding the bias here show bad results?

		tmp = math.exp(preActivation)
		self.output = tmp / (tmp+1)

	#Create a deep copy of the Neuron
	def copy(self):
		newList = []
		for i in range(0, len(self.inputs)):
			newList.append([self.inputs[i][0].copy(), self.inputs[i][1]])
		return Neuron(newList, self.num, self.layer, 0)

	#Getters and Setters
	#Set: output, x, y
	#Get: num, output, layer
	def setOutput(self, value):
		self.output = value
	def setCoords(self, x, y):
		self.x = x
		self.y = y
	def getNum(self):
		return self.num
	def getOutput(self):
		return self.output
	def getLayer(self):
		return self.layer

		

class Graph:
	#Pygame Font
	pygame.font.init()
	myfont = pygame.font.SysFont('Comic Sans MS', 20)

	#Initialize a new Graph
	#Three Neurons are created at layer zero to represent inputs
	#These neurons do not complete regular operations
	#They only serve as placeholders for the input data
	#The random decider picks which final neuron decides which player movement
	def __init__(self, x, y, win):
		self.weights = []
		self.__neurons = []
		self.numCount = 0
		self.__neurons.append(Neuron([], self.numCount, 0, 0))
		self.numCount += 1
		self.__neurons.append(Neuron([], self.numCount, 0, 0))
		self.numCount += 1
		self.__neurons.append(Neuron([], self.numCount, 0, 0))
		self.numCount += 1
		self.x = x 
		self.y = y - 80
		self.win = win
		self.randomDecider = round(random.random())

	#Create a new Neuron and connect it to an existing Neuron
	def addNeuronAfter(self, num):
		for i in range(0, len(self.__neurons)):
			if self.__neurons[i].num == num:
				w = Weight(-1)
				self.weights.append(w)
				new = Neuron([[self.__neurons[i], w]], self.numCount, self.__neurons[i].layer+1, 0)
				self.numCount += 1
				self.__neurons.append(new)
				break

	#Estalish a connection between to existing Neurons 
	def connectNeuronToInput(self, num, numOfDest):
		for i in range(0, len(self.__neurons)):
			if num == self.__neurons[i].num:
				for j in range(0, len(self.__neurons)):
					if numOfDest == self.__neurons[j].num:
						w = Weight(-1)
						self.weights.append(w)
						self.__neurons[j].inputs.append([self.__neurons[i], w])

	#Perform the graph traversal for every Neuron to operate in order
	def operate(self, x, xO, yO):
		layers = [[]]
		currentLayer = 0
		#This seperates the graph into layers
		#This way the operations are performed in order by layer
		#Instead of post order traversal
		for i in range(0, len(self.__neurons)):
			if (self.__neurons[i].layer > currentLayer):
				currentLayer += 1
				layers.append([self.__neurons[i]])
			else:
				layers[currentLayer].append(self.__neurons[i])

		#If a Neuron is an input Neuron (0, 1, 2) then the game input values
		#Are provided as output. Otherwise the Nueron performs its operation
		#In the end the final two Neurons have their values
		decision = []
		for i in range(0, len(layers)):
			for j in range(0, len(layers[i])): 
				if layers[i][j].getNum() == 0:
					layers[i][j].setOutput(x)
				elif layers[i][j].getNum() == 1:
					layers[i][j].setOutput(xO)
				elif layers[i][j].getNum() == 2:
					layers[i][j].setOutput(yO)
				else:
					layers[i][j].operate()
					if layers[i][j].layer == currentLayer:
						decision.append([layers[i][j].getNum(), layers[i][j].output]) 
		#Helpful for deugging
		print(decision)
		#This returns the NN response for how the player should act
		if self.randomDecider == 1:
			if decision[0][1] > decision[1][1]:
				if decision[0][0] > decision[1][0]:
					return -1
				else:
					return 1
		else:
			if decision[0][1] > decision[1][1]:
				if decision[0][0] > decision[1][0]:
					return 1
				else:
					return -1

	#Pick which weights to adjust based on a postive or negative feedback(direction)
	def fixWeights(self, direction):
		weightValues = []
		if direction == 1:
			for i in range(0, len(self.weights)):
				weightValues.append(self.weights[i].getValue())
			maxValue = max(weightValues)
			for i in range(0, len(self.weights)):
				if maxValue == self.weights[i].getValue():
					self.weights[i].change(1)
		else:
			for i in range(0, len(self.weights)):
				weightValues.append(self.weights[i].getValue())
			minValue = max(weightValues)
			for i in range(0, len(self.weights)):
				if minValue == self.weights[i].getValue():
					self.weights[i].change(-1)
				
	#Steps to display the graphs for each game using Pygame tools
	def display(self):
		layers = [[]]
		currentLayer = 0
		for i in range(0, len(self.__neurons)):
			if (self.__neurons[i].layer > currentLayer):
				currentLayer += 1
				layers.append([self.__neurons[i]])
			else:
				layers[currentLayer].append(self.__neurons[i])
		for i in range(0, currentLayer+1):

			for j in range(0, len(layers[i])):

				textsurface = self.myfont.render(str(layers[i][j].num), False, (255, 255, 255))

				self.win.blit(textsurface,(self.x + ((100/(currentLayer+1))*i), self.y + ((100/(len(layers[i])+1))*(j+1))   ))

				layers[i][j].setCoords(self.x + ((100/(currentLayer+1))*i), self.y + ((100/(len(layers[i])+1))*(j+1)))

		for i in range(0, len(self.__neurons)):
			for j in range(0, len(self.__neurons)):
				for k in range(0, len(self.__neurons[i].inputs)):
					if (self.__neurons[i].inputs[k][0].getNum() == self.__neurons[j].getNum()):
						value = self.__neurons[i].inputs[k][1].getValue()*10
						if value > 1:
							value =1
						pygame.draw.line(self.win, (255, 255*value, 255*value), (self.__neurons[i].x, self.__neurons[i].y), (self.__neurons[j].x, self.__neurons[j].y))

	#Create a deep copy of the graph
	#This requires also performing a deep copy of the 
	#Neuron list, Weight list, and all attriutes(values)
	def copy(self, x, y , win):
		graph = Graph(x, y, win)
		graph.setNeurons(self.__neurons)
		graph.setWeights(self.weights)
		graph.setValues(self.numCount,self.randomDecider)
		return graph

	#Getters and Setters
	#Set: Neurons, Weights, Values
	#Get:
	def setNeurons(self, neurons):
		for i in range(0, len(neurons)):
			self.__neurons.append(neurons[i].copy())
	def setWeights(self, weights):
		print(len(weights))
		for i in range(0, len(weights)):
			self.weights.append(weights[i].copy())
	def setValues(self, numCount, randomDecider):
		self.numCount = numCount
		self.randomDecider = randomDecider
