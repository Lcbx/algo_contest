import sys
import collections


Dataset = collections.namedtuple("Dataset", "Ntypes pieces costs Nmodels models")

# gets aruments used in cli
args = sys.argv
#print(args)
ex_path = args[1]


# loads the dataset 
dataset = None
with open(ex_path,"r") as file:
	content = file.read()
	content = content.split("\n")[:-1]
	content = [ [*map(int, line.rstrip().split(" "))] for line in content]
	#for line in content:
	#	print(line)
	
	Ntypes = content[0][0]
	pieces = content[1]
	costs = content[2]
	Nmodels = content[3][0]
	models = content[4:4+Nmodels]
	
	dataset = Dataset(Ntypes, pieces, costs, Nmodels, models)
#print(dataset)



import numpy as np
from lsqnonneg import lsqnonneg
import random


# transforms the dataset arrays in numpy arrays
mat = np.matrix(dataset.models)
pieces = np.array(dataset.pieces)
costs = np.array(dataset.costs)


# uses NNLS algorithm for a first idea of where to look
float_solution = lsqnonneg( mat.T, pieces)[0]
# print("float_solution", min_solution)

# NNLS uses decimal values, we floor the values to have an intial integer vector
min_solution = np.floor(float_solution)
# print("min_solution", min_solution)


# the best (legal solution's) score, must be minimized
best_score = 99999999999999999.
# the best solution found for now
best_solution = min_solution


# a flat number of iterative guesses 
ITERATIONS = 200000 


#for i in range(ITERATIONS):
i = 0
while True:
	i+=1
	# first we search around the initial solution proposed by NNLS, then around the best found so far
	if i< ITERATIONS*3/4:
		evaluated = min_solution
	else:
		evaluated = best_solution
	
	# the odds of changing the k-th element in the pieces vector
	odds = float_solution - evaluated
	odds[odds<0.] = 0.
	odds = odds%1.
	
	# generates a random change (between -2 and +2) based on the odds
	random_guess = []
	for x in odds:
		seed = random.random()
		if x < 0.1:
			ret = -2 if seed<0.03 else -1. if seed < 0.2     else 0. if seed > 0.4 else 1. if seed < 0.96 else 2. 
		else:
			ret = -2 if seed<0.03 else -1. if seed < 0.3*x else 0. if seed > x    else 1. if seed < 0.96 else 2. 
		random_guess.append(ret)
	random_guess = np.asarray(random_guess)
	
	# the proposed solution
	solution = np.abs(evaluated + random_guess)
	
	# computes how many initial pieces remain
	remaining_pieces = solution * mat - pieces
	remaining_pieces = np.squeeze(np.asarray(remaining_pieces))
	
	# verifies the solution is legal (all initial pieces must be used)
	illegal = np.any(remaining_pieces < 0)
	score = np.sum(remaining_pieces * dataset.costs)
	
	# if it's not illegal and is better than the best, it replaces it
	if not illegal and  score<best_score:
			best_score = score
			best_solution = solution
			print(*map(int, best_solution))
			#print("score", score)
			#print("random_guess", random_guess)
			# print("odds", odds)
			# print("pieces", pieces)
			# print("costs", costs)
			# print("solution", solution)
			# print("solution * mat", solution * mat)
			# print("remaining_pieces", remaining_pieces)
			sys.stdout.flush()
#print("score", best_score)