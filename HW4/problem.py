import random
import math

class Problem():
    def __init__(self) -> None:
        self._solution = []
        self._value = 0
        self._numEval = 0

    # accessor
    def getNumEval(self):
        return self._numEval
    def getSolution(self):
        return self._solution
    def getValue(self):
        return self._value
    
    # mutator
    def setNumEval(self, cnt):
        self._numEval += cnt
    def storeResult(self, solution, value):
        self._solution = solution
        self._value = value
    def report(self):
        print()
        print("Total number of evaluations: {0:,}".format(self._numEval))

class Numeric(Problem):
    def __init__(self) -> None:
        super().__init__()
        self._delta = 0.01
        self._domain = []
        self._expression = ""

        # gradient descent
        self._dx = 0.0001
        self._alpha = 0.01

    # accessor
    def getDelta(self):
        return self._delta
    def getDx(self):
        return self._dx
    def getAlpha(self):
        return self._alpha
    
    #gradient-descent
    def takeStep(self, current):
        new_cur = []
        for i in range(len(current)):
            grad = self.gradient(current, i)
            value = current[i] - (self._alpha * grad)
            if(self.isLegal(value, i)):
                new_cur.append(value)
            else:
                new_cur.append(current[i])
    
        return new_cur
        
    
    def gradient(self, current, i):
        current_dx = []
        for j in range(len(current)):
            if(j == i):
                current_dx.append(current[j] + self._dx)
            else:
                current_dx.append(current[j])
        return (self.evaluate(current_dx) - self.evaluate(current)) / self._dx

    def isLegal(self, value, i):
        low = self._domain[1][i]
        up = self._domain[2][i]
        if(low <= value <= up):  return True;
        else:    return False;

    def setVariables(self):
        filename = input("Enter the file name of a function: ")
        infile = open(filename, 'r')
        expression = infile.readline().strip()
        self._expression = expression
        
        varNames, low, up = [], [], []
        for line in infile:
            varNames.append(line.split(",")[0].strip())
            low.append(float(line.split(",")[1]))
            up.append(float(line.split(",")[2]))

        domain = [varNames, low, up]
        infile.close()

        self._domain = domain

    def randomInit(self): ###
        init = []
        var_n = len(self._domain[0])

        for i in range(var_n):
            low = self._domain[1][i]
            up = self._domain[2][i]
            init.append(random.uniform(low, up))

        return init    # Return a random initial point
                   

    def evaluate(self, current):
        ## Evaluate the expression of 'p' after assigning
        ## the values of 'current' to the variables
        self.setNumEval(1)
        expr = self._expression         # p[0] is function expression
        varNames = self._domain[0]  # p[1] is domain
        for i in range(len(varNames)):
            assignment = varNames[i] + '=' + str(current[i])
            exec(assignment)
        return eval(expr)

    def mutate(self, current, i, d): ## Mutate i-th of 'current' if legal
        curCopy = current[:]
        domain = self._domain        # [VarNames, low, up]
        l = domain[1][i]     # Lower bound of i-th
        u = domain[2][i]     # Upper bound of i-th
        if l <= (curCopy[i] + d) <= u:
            curCopy[i] += d
        return curCopy

    def describeProblem(self):
        print()
        print("Objective function:")
        print(self._expression)   # Expression
        print("Search space:")
        varNames = self._domain[0] # p[1] is domain: [VarNames, low, up]
        low = self._domain[1]
        up = self._domain[2]
        for i in range(len(low)):
            print(" " + varNames[i] + ":", (low[i], up[i])) 

    def displayResult(self):
        print()
        print("Solution found:")
        print(self.coordinate(self._solution))  # Convert list to tuple
        print("Minimum value: {0:,.3f}".format(self._value))
        self.report()

    def coordinate(self, solution):
        c = [round(value, 3) for value in solution]
        return tuple(c)  # Convert the list to a tuple

    #FCHC.N
    def randomMutant(self, current): 
        d_ran = [self._delta, -self._delta]
        return self.mutate(current, random.choice(range(len(current))), random.choice(d_ran)) # Return a random successor

    #SAHC.N
    def mutants(self, current): 

        neighbors = []
        for i in range(len(current)):
            neighbors.append(self.mutate(current, i, self._delta))
            neighbors.append(self.mutate(current, i, -self._delta))

        return neighbors     # Return a set of successors


class Tsp(Problem):
    def __init__(self) -> None:
        super().__init__()
        self._numCities = 0
        self._locations = []
        self._table = []

    #accessor

    def createProblem(self):
        fileName = input("Enter the file name of a TSP: ")
        infile = open(fileName, 'r')
        # First line is number of cities
        numCities = int(infile.readline())
        locations = []
        line = infile.readline()  # The rest of the lines are locations
        while line != '':
            locations.append(eval(line)) # Make a tuple and append
            line = infile.readline()
        infile.close()
        table = self.calcDistanceTable(numCities, locations)
        
        self._numCities = numCities
        self._locations = locations
        self._table = table

    def calcDistanceTable(self, numCities, locations):
        table = [[0 for col in range(numCities)] for row in range(numCities)]
       
        for i in range(numCities):
            for j in range(numCities):
                table[i][j] = math.sqrt((locations[j][0]-locations[i][0])**2 + (locations[j][1]-locations[i][1])**2)

        return table # A symmetric matrix of pairwise distances

    def randomInit(self):   # Return a random initial tour
        n = self._numCities
        init = list(range(n))
        random.shuffle(init)
        return init

    def evaluate(self, current):
        ## Calculate the tour cost of 'current'
        ## 'p' is a Problem instance
        ## 'current' is a list of city ids
        self.setNumEval(1)
       
        cost = 0.0
        for i in range(len(current)-1):
            cost += self._table[current[i]][current[i+1]]
        
        return cost

    def inversion(self, current, i, j):  ## Perform inversion
        curCopy = current[:]
        while i < j:
            curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
            i += 1
            j -= 1
        return curCopy

    def describeProblem(self):
        print()
        n = self._numCities
        print("Number of cities:", n)
        print("City locations:")
        locations = self._locations
        for i in range(n):
            print("{0:>12}".format(str(locations[i])), end = '')
            if i % 5 == 4:
                print()

    def displayResult(self):
        print()
        print("Best order of visits:")
        self.tenPerRow(self._solution)       # Print 10 cities per row
        print()
        print("Minimum tour cost: {0:,}".format(round(self._value)))
        self.report()

    def tenPerRow(self, solution):
        for i in range(len(solution)):
            print("{0:>5}".format(solution[i]), end='')
            if i % 10 == 9:
                print()

    #FCHC.Tsp
    def randomMutant(self, current): # Inversion only
        while True:
            i, j = sorted([random.randrange(self._numCities)
                        for _ in range(2)])
            if i < j:
                curCopy = self.inversion(current, i, j)
                break
        return curCopy

    #SAHC.Tsp
    def mutants(self, current): # Inversion only
        n = self._numCities
        neighbors = []
        count = 0
        triedPairs = []
        while count <= n:  # Pick two random loci for inversion
            i, j = sorted([random.randrange(n) for _ in range(2)])
            if i < j and [i, j] not in triedPairs:
                triedPairs.append([i, j])
                curCopy = self.inversion(current, i, j)
                count += 1
                neighbors.append(curCopy)
        return neighbors