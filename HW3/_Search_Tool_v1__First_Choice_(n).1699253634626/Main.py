import random
import math

DELTA = 0.01   # Mutation step size
LIMIT_STUCK = 100  # Max number of evaluations enduring no improvement
NumEval = 0    # Total number of evaluations


def main():
	fileName = input()
	# Create an instance of numerical optimization problem
	p = createProblem(fileName)   # 'p': (expr, domain)
	# Call the search algorithm
	solution, minimum = firstChoice(p)
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
	
	#filename = input("Enter the file name of a function: ")
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


def firstChoice(p):
	current = randomInit(p)   # 'current' is a list of values
	valueC = evaluate(current, p)
	i = 0
	while i < LIMIT_STUCK:
		successor = randomMutant(current, p)
		valueS = evaluate(successor, p)
		if valueS < valueC:
			current = successor
			valueC = valueS
			i = 0              # Reset stuck counter
		else:
			i += 1
	return current, valueC


def randomInit(p):
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
	expr = p[0]         # p[0] is function expression
	varNames = p[1][0]  # p[1] is domain: [varNames, low, up]
	for i in range(len(varNames)):
		assignment = varNames[i] + '=' + str(current[i])
		exec(assignment)
	return eval(expr)


def randomMutant(current, p):
	# Return a random successor
	
	domain = p[1]
	i = random.randint(0, len(domain[1]) - 1)  #domain[1]의 길이까지에서 랜덤한 정수 선택
	d = random.uniform(0, 1) * (domain[2][i] - domain[1][i]) #0부터 1 사이에서 임의의 실수 d를 선택
	
	return mutate(current, i, d, p)


def mutate(current, i, d, p):  # Mutate i-th of 'current' if legal
	curCopy = current[:]
	domain = p[1]        # [VarNames, low, up]
	l = domain[1][i]     # Lower bound of i-th
	u = domain[2][i]     # Upper bound of i-th
	if l <= (curCopy[i] + d) <= u:
		curCopy[i] += d
	return curCopy


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
	print("Search algorithm: First-Choice Hill Climbing")
	print()
	print("Mutation step size:", DELTA)
	print("Max evaluations with no improvement: {0:,} iterations"
				.format(LIMIT_STUCK))


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
