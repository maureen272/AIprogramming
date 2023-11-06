import random
import math

LIMIT_STUCK = 100  # Max number of evaluations enduring no improvement
NumEval = 0    # Total number of evaluations


def main():
	# Create an instance of TSP
	fileName = input()
	p = createProblem(fileName)    # 'p': (numCities, locations, distanceTable)
	# Call the search algorithm
	solution, minimum = firstChoice(p)
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
	
	
	table = [[0 for col in range(numCities)] for row in range(numCities)]
	
  #첫번째(index 0)도시부터 이중 for문 돌려가며 다른 도시와의 거리를 두 점 사이 거리공식 사용해서 구하기
	for i in range(numCities):
		for j in range(numCities):
			table[i][j] = math.sqrt((locations[j][0]-locations[i][0])**2 + (locations[j][1]-locations[i][1])**2)
			
	return table  # A symmetric matrix of pairwise distances


def firstChoice(p):
	current = randomInit(p)   # 'current' is a list of city ids
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


def randomMutant(current, p):  # Apply inversion
	while True:
		i, j = sorted([random.randrange(p[0])
									 for _ in range(2)])
		if i < j:
			curCopy = inversion(current, i, j)
			break
	return curCopy


def inversion(current, i, j):  # Perform inversion
	curCopy = current[:]
	while i < j:
		curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
		i += 1
		j -= 1
	return curCopy


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
	print("Search algorithm: First-Choice Hill Climbing")
	print("Max evaluations with no improvement: {0:,} iterations"
				.format(LIMIT_STUCK))


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
