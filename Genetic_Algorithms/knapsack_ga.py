# starter code for solving knapsack problem using genetic algorithm
import itertools
import operator
import random
import os

fc = open('./c.txt', 'r')
fw = open('./w.txt', 'r')
fv = open('./v.txt', 'r')
fout = open('./out.txt', 'w')

c = int(fc.readline())
w = []
v = []
for line in fw:
    w.append(int(line))
for line in fv:
    v.append(int(line))

print('Capacity :', c)
print('Weight :', w)
print('Value : ', v)

popSize = int(input('\nSize of population : '))
genNumber = int(input('Max number of generation : '))

print('\nParent Selection\n---------------------------')
print('(1) Roulette-wheel Selection')
print('(2) K-Tournament Selection')
parentSelection = int(input('Which one? '))
if parentSelection == 2:
    k = int(input('k=? (between 1 and ' + str(popSize) + ') '))
elif parentSelection != 1 and parentSelection != 2:
    print("You have to write 1 or 2. Try again")
    exit(0)

print('\nN-point Crossover\n---------------------------')
n = int(input('n=? (between 1 and ' + str(len(w) - 1) + ') '))
if n < 1 or n >= len(w):
    print("You have to write an integer between 1 and", len(w), ". Try again")
    exit(0)

print('\nMutation Probability\n---------------------------')
mutProb = float(input('prob=? (between 0 and 1) '))
if mutProb < 0 or mutProb > 1:
    print("You have to write a number between 0 and 1. Try again")
    exit(0)

print('\nSurvival Selection\n---------------------------')
print('(1) Age-based Selection')
print('(2) Fitness-based Selection')
survivalSelection = int(input('Which one? '))
if survivalSelection != 1 and survivalSelection != 2:
    print("You have to write 1 or 2. Try again")
    exit(0)

elitism = int(input('\nElitism? (1 or 0) '))
if elitism != 1 and elitism != 0:
    print("You have to write 1 or 0. Try again")
    exit(0)

#----------------------------------------------------------------------------------------------------
# CREATE FIRST POPULATION
print('------------------------------------------------------------------')
population = []
for i in range(popSize):
    temp = []
    for j in range(len(w)):
        temp.append(random.randint(0, 1))
    population.append(temp)

#----------------------------------------------------------------------------------------------------
# CREATE WHOLE POPULATION
for_result = []
population_wdetails = {}  # to keep chroms with their fitness and weight values
fitnesses = {}  # to keep fitness values to use in roulet wheel

def createPopulation(population):
    for i, chrom in enumerate(population):
        ft = 0
        wt = 0
        for j, gene in enumerate(chrom):
            ft += gene * v[j]
            wt += gene * w[j]
        population_wdetails[i + 1] = [chrom, ft, wt, 0]
        fitnesses[i + 1] = ft
        for_result.append((wt, ft, chrom))

#----------------------------------------------------------------------------------------------------
# EVALUATE NEW MEMBERS
children_wdetails = {}
childrensFitnesses = []

def evaluateNewMember(chrom, item):
    ft = 0
    wt = 0
    for j, gene in enumerate(chrom):
        ft += gene * v[j]
        wt += gene * w[j]
    children_wdetails[item] = [chrom, ft, wt, 0]
    for_result.append((wt, ft, chrom))

#----------------------------------------------------------------------------------------------------
# PARENT SELECTION
parents = []

# Roulette-wheel Selection
def findParentRW():
    total = (float(sum(fitnesses.values()))) / 360.0    # the sum of all fitnesses ​​divided by 360
                                                        # this value is used to find out how much space the values ​
                                                        # occupy in a round-wheel
    list = []       # to keep members with their values that the places they occupy in the round wheel
    i = 0
    for _ in itertools.repeat(None, len(fitnesses)):
        i += 1
        if fitnesses.get(i):
            list.append((i, fitnesses.get(i) / total))

    list.sort(key=lambda tup: tup[1])   # list (example)
                                        #[(1, 40.07204610951008),
                                        # (3, 55.05043227665706),
                                        # (4, 62.57204610951008),
                                        # (2, 97.5864553314121),
                                        # (5, 104.71902017291066)]
    for n in itertools.repeat(0, popSize):
        x = random.randrange(360)           # Point where the mark stops in the round-wheel

        # -the values ​​in the example are based on-
        # If the point is between 0 and 40, the member 1 is added to the parents
        # If not, the slice size of member 3 in the second queue is added above the current range
        # If the point is between 40 and 95, the member 3 in the second row is added to the parents.
        # It doesn't matter if to start with the member with the largest slice or the member with the lowest slice.
        # Each of the values ​​0 to 360 has the same probability of being selected
        # The member with the largest slice has the advantage. It can be selected with more numbers.
        for member,slice in list:
            n += slice
            if x < n:
                parents.append(member)
                break


# k-Tournament
def findParentKT():
    # As many children as the population need to be created for the new generation
    # Since two parents form two children, parent selection is repeated by  the number of populations
    # For each parent selection, k members from the entire population will be selected
    for _ in itertools.repeat(None,popSize):
        pop_keys = list(population_wdetails)
        best = (0, 0)                           # It will change if member's fitness value is bigger
        # To select k chroms for the tourment
        # In each loop, the fittest member is found by comparison.
        for _ in itertools.repeat(None, k):
            a = random.choice(pop_keys)         # select random member
            if best[1] < fitnesses.get(a):      # compare its value with current biggest
                best = (a, fitnesses.get(a))
            pop_keys.remove(a)                  # The same parent cannot be selected more than once in a tournament
        parents.append(best[0])

#----------------------------------------------------------------------------------------------------
# CROSSOVER
def crossover(parent1, parent2):
    child1 = parent1[0]  # (example) [1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1]
    child2 = parent2[0]  # (example) [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1]

    points = []
    # n points are selected randomly to ensure variety in children of the same parents
    while len(points) < n:
        point = random.randrange(1, len(w))
        if point in points:
            continue
        elif point + 1 in points:
            continue
        elif point - 1 in points:
            continue
        points.append(point)
    points.append(len(w))
    points.sort()           # (example) [2, 4, 8, 15]

    i = 0
    for _ in itertools.repeat(None, len(points) - 1):
        # -the values ​​in the example are based on-
        # Parents 1 gives the 2nd and 3rd genes, 2-4, to parent 2.
        # Parent 2 also gives the same numbered genes to parent 1.
        # Parents 1 gives genes 8, 9, 10, 11, 12, 13 and 14, 8-15, to parent 2.
        # Parent 2 also gives the same numbered genes to parent 1.
        if i % 2 == 0:
            temp = child1[points[i]:points[i + 1]]
            child1[points[i]:points[i + 1]] = child2[points[i]:points[i + 1]]
            child2[points[i]:points[i + 1]] = temp
            i += 1
        else:
            i += 1
            continue

    return child1, child2

#----------------------------------------------------------------------------------------------------
# MUTATION
def reverse_allele(child):
    q = random.randrange(len(w))    # Select a random gene number
    if child[q] == 1:
        child[q] = 0
    else:
        child[q] = 1

#----------------------------------------------------------------------------------------------------
# Children's fitness values are calculated to refuse the child whose fitness value is the least
def calculateFitnesses(children):
    for chrom in children:
        ft = 0
        for j, gene in enumerate(chrom):
            ft += gene * v[j]
        childrensFitnesses.append((ft, chrom))
    childrensFitnesses.sort(reverse=True)

# --------------------------------------------------------------------------------------------------
# MAIN

# evaluate first population with details
createPopulation(population)
# population_wdetails: (example)
# {1: [[1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], 618, 321, 0],
#  2: [[0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1], 1505, 783, 0],
#  3: [[1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0], 849, 442, 0],
#  4: [[0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0], 965, 505, 0],
#  5: [[0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0], 1615, 845, 0]}

# fitnesses (example)
# {1: 618, 2: 1505, 3: 849, 4: 965, 5: 1615}

print("\nThe first population:")
for i in population_wdetails:
        print(i,population_wdetails[i])

for _ in itertools.repeat(None, genNumber):
    # Lists are reset in each cycle
    parents = []
    children = []
    children_wdetails = {}
    childrensFitnesses = []
    for_result = []

    # Parent selection for parents pool
    if parentSelection == 1:
        findParentRW()

    elif parentSelection == 2:
        findParentKT()

    # Select parents to crossover
    if (popSize % 2) == 0:
        range = int(popSize / 2)
    else:
        range = int((popSize + 1) / 2)

    for _ in itertools.repeat(None, range):
        p1, p2 = random.sample(parents, 2)
        while p1 == p2:
            p1, p2 = random.sample(parents, 2)
        parent1 = population_wdetails.get(p1)
        parent2 = population_wdetails.get(p2)

        child1, child2 = crossover(parent1, parent2)
        children.append(child1)
        children.append(child2)

    # If the user-specified value is counted as slice size,
    # the mutation occurs when the randomly selected value is smaller than the user-specified value.
    prob = random.uniform(0, 1)
    if mutProb == 1 or (prob <= mutProb and prob != 0):
        # bit flip mutation
        q = random.randrange(len(children) - 1)
        reverse_allele(children[q])

    # Elitism
    if elitism == 1:
        sorted_fitnesses = sorted(fitnesses.items(), key=operator.itemgetter(1))
        calculateFitnesses(children)

        fittest = sorted_fitnesses[-1][0]

        # Survival Selection
        # -------------------
        # Fitness-based
        if survivalSelection == 2:
            i = 0
            for ft, child in childrensFitnesses:
                i += 1
                if i > popSize:
                    break
                if fittest == i:
                    population_wdetails[i][-1] = population_wdetails[i][-1] + 1
                    chrom = population_wdetails[i][0]
                    ft = population_wdetails[i][1]
                    wt = population_wdetails[i][2]
                    for_result.append((wt, ft, chrom))
                    if i == popSize:
                        break
                    i = i + 1
                    evaluateNewMember(child, i)
                    population_wdetails[i] = children_wdetails[i]
                    fitnesses[i] = ft
                    continue
                evaluateNewMember(child, i)
                population_wdetails[i] = children_wdetails[i]
                fitnesses[i] = ft

        # Age-based
        else:
            # In all cases, all parent chromosomes, except the fittest chromosome, give their places to children.
            # That is, in a population, only the age of the fittest chromosome of the previous generation may be older than others.
            # There are two situations:
            # First; the fittest chromosome is still the fittest and it is older than others. But due to elitism,
            # its place is not given to a child.
            # Second; the fittest value is no longer the fittest and its age is older than others.
            # But, all chromosomes except the fittest chromosome will change, so it doesn't matter which one is the oldest.
            # In both cases, it is sufficient to find the fittest chromosome in this population and do not give its place to a child.

            i = 0
            for ft, child in childrensFitnesses:
                i += 1
                if i > popSize:
                    break
                if fittest == i:
                    population_wdetails[i][-1] = population_wdetails[i][-1] + 1
                    chrom = population_wdetails[i][0]
                    ft = population_wdetails[i][1]
                    wt = population_wdetails[i][2]
                    for_result.append((wt, ft, chrom))
                    if i == popSize:
                        break
                    i += 1
                    evaluateNewMember(child, i)
                    population_wdetails[i] = children_wdetails[i]
                    continue
                evaluateNewMember(child, i)
                population_wdetails[i] = children_wdetails[i]

    # In all cases, all parents change
    else:
        createPopulation(children)


# Function to convert
def listToString(s):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for ele in s:
        str1 += str(ele)
    # return string
    return str1

for_result.sort(reverse=True)

for wt, ft, chrom in for_result:
    if wt <= c:
        chrom = listToString(chrom)
        fout.write('chromosome: ' + chrom)
        fout.write('\nweight: ' + str(wt))
        fout.write('\nvalue: ' + str(ft))
        fout.close()

        print("\nThe fittest values\n-------------------")
        print('chromosome: ' + chrom)
        print('weight: ' + str(wt))
        print('value: ' + str(ft))
        break

if os.stat("out.txt").st_size == 0:
    fout.close()
    print("\nAll fitness values are bigger than the capacity. Sorry...")


show = str(input('\nDo you want to see all population with details? (Y or N) '))
if show == "Y":
    for i in population_wdetails:
        print(i,population_wdetails[i])
elif show != "N":
    print("You have to write Y or N. Maybe next time.")
