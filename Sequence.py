
import numpy as np
import sys


nQueens = 8
Stop_Ctr = 28
Mutate = 0.000001
Mutate_Flag = True
Max_Iter = 100
Population = None

class Eightqueen:
	def __init__(self):
		self.sequence = None
		self.fitness = None
		self.survival = None
	def setSequence(self, val):
		self.sequence = val
	def setFitness(self, fitness):
		self.fitness = fitness
	def setSurvival(self, val):
		self.survival = val

def fitness(chromosome = None):

	clashes = 0;
	row_col_clashes = abs(len(chromosome) - len(np.unique(chromosome)))
	clashes += row_col_clashes

	# calculate diagonal clashes
	for i in range(len(chromosome)):
		for j in range(len(chromosome)):
			if ( i != j):
				dx = abs(i-j)
				dy = abs(chromosome[i] - chromosome[j])
				if(dx == dy):
					clashes += 1


	return 28 - clashes	


def Sequence():
	# randomly generates a sequence.
	global nQueens
	init_distribution = np.arange(nQueens)
	np.random.shuffle(init_distribution)
	return init_distribution

def genPopulation(population_size = 100):
	global Population

	Population = population_size

	population = [Eightqueen() for i in range(population_size)]
	for i in range(population_size):
		population[i].setSequence(Sequence())
		population[i].setFitness(fitness(population[i].sequence))

	return population


def getParent():
	globals()	
	parent1, parent2 = None, None
    
	summation_fitness = np.sum([x.fitness for x in population])
	for each in population:
		each.survival = each.fitness/(summation_fitness*1.0)

	while True:
		parent1_random = np.random.rand()
		parent1_rn = [x for x in population if x.survival <= parent1_random]
		try:
			parent1 = parent1_rn[0]
			break
		except:
			pass

	while True:
		parent2_random = np.random.rand()
		parent2_rn = [x for x in population if x.survival <= parent2_random]
		try:
			t = np.random.randint(len(parent2_rn))
			parent2 = parent2_rn[t]
			if parent2 != parent1:
				break
			else:
				print ("equal parents")
				continue
		except:
			print ("exception")
			continue

	if parent1 is not None and parent2 is not None:
		return parent1, parent2
	else:
		sys.exit(-1)

def reproduce_crossover(parent1, parent2):
	globals()
	n = len(parent1.sequence)
	c = np.random.randint(n, size=1)
	child = Eightqueen()
	child.sequence = []
	child.sequence.extend(parent1.sequence[0:c])
	child.sequence.extend(parent2.sequence[c:])
	child.setFitness(fitness(child.sequence))
	return child


def mutate(child):

	if child.survival < Mutate:
		c = np.random.randint(8)
		child.sequence[c] = np.random.randint(8)
	return child

def GA(iteration):
	print (" #"*10 ,"Executing Genetic  generation : ", iteration , " #"*10)
	globals()
	newpopulation = []
	for i in range(len(population)):
		parent1, parent2 = getParent()
		# print "Parents generated : ", parent1, parent2

		child = reproduce_crossover(parent1, parent2)

		if(Mutate_Flag):
			child = mutate(child)

		newpopulation.append(child)
	return newpopulation


def stop():
	globals()
	fitnessvals = [pos.fitness for pos in population]
	if Stop_Ctr in fitnessvals:
		return True
	if Max_Iter == iteration:
		return True
	return False


population = genPopulation(1000)

iteration = 0;
while not stop():
	# keep iteratin till  you find the best position
	population = GA(iteration)
	iteration +=1 

print ("Iteration number : ", iteration)
for each in population:
	if each.fitness == 28:
		print (each.sequence)