import random
import math

NumEval = 0    # Total number of evaluations


def main():
	# Create an instance of TSP
	fileName = input()
	p = createProblem(fileName)    # 'p': (numCities, locations, table)
	# Call the search algorithm
	solution, minimum = steepestAscent(p)
	# Show the problem and algorithm settings
	describeProblem(p)
	displaySetting()
	# Report results
	displayResult(solution, minimum)


def createProblem(fileName):
	# Read in a TSP (# of cities, locatioins) from a file.
	# Then, create a problem instance and return it.
	infile = open(fileName, 'r')
	# First line is number of cities
	numCities = int(infile.readline())
	locations = []
	line = infile.readline()  # The rest of the lines are locations
	while line != '':
		locations.append(eval(line))  # Make a tuple and append
		line = infile.readline()
	infile.close()
	table = calcDistanceTable(numCities, locations)
	return numCities, locations, table


def calcDistanceTable(numCities, locations):
	# A symmetric matrix of pairwise distances
	
	table = [[0 for col in range(numCities)] for row in range(numCities)]
	
  #첫번째(index 0)도시부터 이중 for문 돌려가며 다른 도시와의 거리를 두 점 사이 거리공식 사용해서 구하기
	for i in range(numCities):
		for j in range(numCities):
			table[i][j] = math.sqrt((locations[j][0]-locations[i][0])**2 + (locations[j][1]-locations[i][1])**2)
			
	return table  # A symmetric matrix of pairwise distances


def steepestAscent(p):
	current = randomInit(p)   # 'current' is a list of city ids
	valueC = evaluate(current, p)
	while True:
		neighbors = mutants(current, p)
		(successor, valueS) = bestOf(neighbors, p)
		if valueS >= valueC:
			break
		else:
			current = successor
			valueC = valueS
	return current, valueC


def randomInit(p):   # Return a random initial tour
	n = p[0]
	init = list(range(n))
	random.shuffle(init)
	return init


def evaluate(current, p):
	## Calculate the tour cost of 'current'
	## 'p' is a Problem instance
	## 'current' is a list of city ids
	## Consider the cost to return to the first city from the last city
	
	#총 eval횟수 체크
	global NumEval
	NumEval += 1
	#만들어두었던 거리 테이블을 참조하여 한 여행에서 i번째 인덱스와 i+1번째 인덱스 사이의 거리를 for문을 돌려 총거리 구하기
	cost = 0.0
	for i in range(len(current)-1):
			cost += p[2][current[i]][current[i+1]]
	return cost


def mutants(current, p):  # Inversion only
	n = p[0]
	neighbors = []
	count = 0
	triedPairs = []
	while count <= n:  # Pick two random loci for inversion
		i, j = sorted([random.randrange(n) for _ in range(2)])
		if i < j and [i, j] not in triedPairs:
			triedPairs.append([i, j])
			curCopy = inversion(current, i, j)
			count += 1
			neighbors.append(curCopy)
	return neighbors


def inversion(current, i, j):  # Perform inversion
	curCopy = current[:]
	while i < j:
		curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
		i += 1
		j -= 1
	return curCopy


def bestOf(neighbors, p):
	# Select the best solution among neighbors
	
	#각 neighbor의 eval값 담아두는 리스트 생성
	evals = []
	
	for neighbor in neighbors:
			evals.append(evaluate(neighbor, p))

	
	bestValue = min(evals)
	best = neighbors[evals.index(bestValue)]
	return best, bestValue


def describeProblem(p):
	print()
	n = p[0]
	print("Number of cities:", n)
	print("City locations:")
	locations = p[1]
	for i in range(n):
		print("{0:>12}".format(str(locations[i])), end='')
		if i % 5 == 4:
			print()


def displaySetting():
	print()
	print("Search algorithm: Steepest-Ascent Hill Climbing")


def displayResult(solution, minimum):
	print()
	print("Best order of visits:")
	tenPerRow(solution)       # Print 10 cities per row
	print("Minimum tour cost: {0:,}".format(round(minimum)))
	print()
	print("Total number of evaluations: {0:,}".format(NumEval))


def tenPerRow(solution):
	for i in range(len(solution)):
		print("{0:>5}".format(solution[i]), end='')
		if i % 10 == 9:
			print()


main()
