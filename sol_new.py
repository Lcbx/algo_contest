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

_impl = print
def print(*args):
	_impl(*args)
	sys.stdout.flush()


import numpy as np
from lsqnonneg import lsqnonneg
import random



def random_change():
	# generates a random change (between -2 and +2)
		change = []
		for _ in evaluated:
			seed = random.random()
			# important ! sort of temperature
			seed *= ITERATIONS/(i+ITERATIONS/100)
			ret = -2 if seed<0.02 else -1. if seed < 0.2 else 0. if seed > 0.4 else 1. if seed < 0.38 else 2.
			change.append(ret)
		return np.asarray(change)



# a list of tabou solutions (that have been investigated already)
tabou = set()

def test_solution(change):
	# the generated potential solution
	solution = evaluated + change
	solution[solution<0] = 0
	
	if not np.any(change!=0.) or tuple(solution) in tabou:
		return None
	
	# computes how many initial pieces remain
	remaining_pieces = solution * mat - pieces
	remaining_pieces = np.squeeze(np.asarray(remaining_pieces))
	
	# verifies the solution is legal (all initial pieces must be used)
	illegal = np.any(remaining_pieces < 0)
	
	if illegal:
		#print("illegal")
		return None
	else:
		score = np.sum(remaining_pieces * dataset.costs)
		return solution, score



# transforms the dataset arrays in numpy arrays
mat = np.matrix(dataset.models)
pieces = np.array(dataset.pieces)
costs = np.array(dataset.costs)




# uses NNLS algorithm for a first idea of where to look
float_solution = lsqnonneg( mat.T, pieces)[0]


# the currently evaluated solution
evaluated = [0] * len(float_solution)

# float_solution rouneded up
max_solution, max_score = test_solution(np.ceil(float_solution))

# the best (legal solution's) score, must be minimized
best_solution, best_score = test_solution(max_solution)
evaluated = best_solution
evaluated_score = best_score

# a flat number of iterative guesses before we change the evaluated solution
ITERATIONS = 10000 


i = 0
while True:
	
	solution = None
	score = None
	
	# finds a valid new solution
	while True:
		i+=1
		
		# if we are at local minima, we change the evaluated solution
		if i > ITERATIONS:
			#print("change")
			i = 0
			tabou.add( tuple(evaluated) )
			evaluated = max_solution
			evaluated_score = max_score
		
		change = random_change()
		result = test_solution(change)
		if result != None:
			solution, score = result
			break
	
	#print("score", score)
	#print(i)
	
	# if the score is better than the one of the evaluated solution
	if score < evaluated_score:
		
		# if it is better than the best found so far
		if score < best_score:
			best_score = score
			best_solution = solution
			print(*map(int, best_solution))
			
			print("score", score)
		#else:
			#print("score", score)
			#print("better")
		
		i = 0
		evaluated_score = score
		evaluated = solution

#print("score", best_score)