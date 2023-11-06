import random
import math

DELTA = 0.01   # Mutation step size
NumEval = 0    # Total number of evaluations


def main():
	# Create an instance of numerical optimization problem
	fileName = input()
	p = createProblem(fileName)   # 'p': (expr, domain)
	# Call the search algorithm
	solution, minimum = steepestAscent(p)
	# Show the problem and algorithm settings
	describeProblem(p)
	displaySetting()
	# Report results
	displayResult(solution, minimum)


def createProblem(fileName):
	## Read in an expression and its domain from a file.
	## Then, return a problem 'p'.
	## 'p' is a tuple of 'expression' and 'domain'.
	## 'expression' is a string.
	## 'domain' is a list of 'varNames', 'low', and 'up'.
	## 'varNames' is a list of variable names.
	## 'low' is a list of lower bounds of the varaibles.
	## 'up' is a list of upper bounds of the varaibles.
	
	infile = open(fileName, 'r')
	expression = infile.readline().strip()
	
	varNames, low, up = [], [], []
	for line in infile:
		varNames.append(line.split(",")[0])
		low.append(int(line.split(",")[1]))
		up.append(int(line.split(",")[2]))
		
	domain = [varNames, low, up] #list 세개 묶어주기
	infile.close()
	return expression, domain


def steepestAscent(p):
	current = randomInit(p)  # 'current' is a list of values
	valueC = evaluate(current, p)
	while True:
		neighbors = mutants(current, p)
		successor, valueS = bestOf(neighbors, p)
		if valueS >= valueC:
			break
		else:
			current = successor
			valueC = valueS
	return current, valueC


def randomInit(p):  # Return a random initial point as a list
	# Return a random initial point
	# as a list of values
	
	init = []
	varNum = len(p[1][0])
	for i in range(varNum): #개수만큼 반복
		low = p[1][1][i]
		up = p[1][2][i]
		init.append(random.uniform(low, up)) #각 변수의 max min값을 알아낸뒤 random.uniform을 사용해 임의의 실수 저장
	return init    # list of values


def evaluate(current, p):
	# Evaluate the expression of 'p' after assigning
	# the values of 'current' to the variables
	global NumEval

	NumEval += 1
	func = p[0]         # p[0] is function expression
	varNames = p[1][0]  # p[1] is domain
	for i in range(len(varNames)):
		result = varNames[i] + '=' + str(current[i])
		exec(result)
	return eval(func)


def mutants(current, p):
	# Return a set of successors
	
	neighbors = []
	for i in range(len(current)):
			neighbors.append(mutate(current, i, DELTA, p))
			neighbors.append(mutate(current, i, -DELTA, p))
	return neighbors


def mutate(current, i, d, p):  # Mutate i-th of 'current' if legal
	curCopy = current[:]
	domain = p[1]        # [VarNames, low, up]
	l = domain[1][i]     # Lower bound of i-th
	u = domain[2][i]     # Upper bound of i-th
	if l <= (curCopy[i] + d) <= u:
		curCopy[i] += d
	return curCopy


def bestOf(neighbors, p):
	# Select the best solution among neighbors
	
 #각 neighbor들에 대해 evaluate를 실행해서 계산
	evals = []
	for neighbor in neighbors:
			evals.append(evaluate(neighbor, p))
	#가장 낮은 값이 좋은값
	bestValue = min(evals)
	#가장 낮은 값 좌표, 가장 낮은 값 담아서 return
	best = neighbors[evals.index(bestValue)]
	
	return best, bestValue


def describeProblem(p):
	print()
	print("Objective function:")
	print(p[0])   # Expression
	print("Search space:")
	varNames = p[1][0]  # p[1] is domain: [VarNames, low, up]
	low = p[1][1]
	up = p[1][2]
	for i in range(len(low)):
		print(" " + varNames[i] + ":", (low[i], up[i]))


def displaySetting():
	print()
	print("Search algorithm: Steepest-Ascent Hill Climbing")
	print()
	print("Mutation step size:", DELTA)


def displayResult(solution, minimum):
	print()
	print("Solution found:")
	print(coordinate(solution))  # Convert list to tuple
	print("Minimum value: {0:,.3f}".format(minimum))
	print()
	print("Total number of evaluations: {0:,}".format(NumEval))


def coordinate(solution):
	c = [round(value, 3) for value in solution]
	return tuple(c)  # Convert the list to a tuple


main()
