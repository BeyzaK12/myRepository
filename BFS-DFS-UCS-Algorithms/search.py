#!/usr/bin/python
import sys

graph = str(sys.argv[1])
start = input("Please enter the start state : ")
end = input("Please enter the goal state  : ")

#Read graph file line by line
with open(graph, 'r') as f:
    myNames = f.readlines()

neigs = {}      #neighbours
dist = []       #distances between two states

# to make dictinories (neigs and dist)
def make(state,ngs):

    ngs = ngs.split(",")      # ex; [(A:0), ( B:6), ( C:4), ( D:3), ( E:0), ( F:0), ( G:0)]
    temp = []               # a temporary list to match the state and its neighbors
    for i in ngs:
        i = i.lstrip()              # delete spaces in the beginning; ( B:6) -> (B:6)
        nei, dis = i.split(":")    # ex; nei = B and dis = 6
        if dis == "0":              # the distance is 0, they are not neighbors
            continue
        temp.append(nei)            # ex; temp = ['B', 'C', 'D']

        # keep distances
        if (nei,state,int(dis)) not in dist:        # ex; if ('A','B', 6) is exist, do not add ('B','A', 6)
            dist.append((state,nei,int(dis)))

    neigs[state] = temp         # keep states with neighbors, ex; {'A': ['B', 'C', 'D'], 'B': ['A', 'C', 'E']}

# repeat for all states
for neighbour in myNames:
    state , ngs = neighbour.split(':', 1)      # divide two parts; A and {A:0, B:6, C:4, D:3, E:0, F:0, G:0}
    ngs = ngs[1:(len(ngs)-2)]        # delete {} and \n; A:0, B:6, C:4, D:3, E:0, F:0, G:0
    make(state,ngs)                 # to keep states and their neighbours

# neigs
# {'A': ['B', 'C', 'D'],
#  'B': ['A', 'C', 'E'],
#  'C': ['A', 'B', 'D', 'F'],
#  'D': ['A', 'C', 'E'],
#  'E': ['B', 'D', 'F', 'G'],
#  'F': ['C', 'E', 'G'],
#  'G': ['E', 'F']}

# dist
#[('A', 'B', 6), ('A', 'C', 4), ('A', 'D', 3),
# ('B', 'C', 2), ('B', 'E', 4),
# ('C', 'D', 2), ('C', 'F', 8),
# ('D', 'E', 3),
# ('E', 'F', 7), ('E', 'G', 6),
# ('F', 'G', 6)]

# BFS -----------------------------------------------------------------------------------
Q = []      # Queue  -   to know the order of the states
P = []      # Paths  -   to keep paths that are iterated
R = []      # Result -   to write the best path

# Print result
def resultBFS():
    # ex; R : ['G','E','B','A']
    R.reverse()
    # ex; R : ['A','B','E','G']
    print("BFS : " + ' - '.join(R))     # ex; BFS : A - B - E - G


def BFS(start,end,done=0):  # 'done' is for blocking loop if we find end state
    Q.append(start)     # first state is 'start'

    # Looks look all states in Q in order
    for state in Q:
        # looks at state's neighbors one by one
        for neighbour in neigs[state]:
            # find end state in start's neighbors
            if state == start and neighbour == end:
                R.append(neighbour)
                R.append(state)
                resultBFS()
                done = 1
                break

            # 'neighbour' in Q => 'neighbour' state is passed
            if neighbour in Q:
                continue

            elif neighbour == end:
                # reverse R, then add end state in the first position
                R.append(neighbour)
                R.append(state)

                # Starting at the end, find which paths are iterated
                P.reverse()
                # ex; P = [(A, B), (A, C), (A, D), (B, C), (B, E), (C, F)]
                # ex; Q = [A, B, C, D, E, F]
                for path in P:
                    # ex; end = 'G' and state = 'E'
                    # if path[1] = 'E', path[0] = 'B' is passed through
                    if path[1]==state:
                        R.append(path[0])
                        if path[0] == start:
                            resultBFS()
                            done = 1
                            break
                        # If path[0] != start, change state and go on
                        state = path[0]
                if done == 1:
                    break

            # end state not found
            # add past path to paths list
            P.append((state,neighbour))
            # put neigbor state in Q to look for its neighbors in the future
            Q.append(neighbour)
        if done == 1:
            break

BFS(start,end)


## DFS -----------------------------------------------------------------------------------
S = []      # Stack      -   to keep the path
V = []      # Visited    -   to do not go same states again

# Print result
def resultDFS():
    print("DFS : " + ' - '.join(S))


# to look neighbors' neigbors first
def loop(state,end):
    for neighbour in neigs[state]:
        # If neighbour state is iterated
        if neighbour in V:
            continue

        # find end state, then add neighbour state to S and go resultDFS directly
        if neighbour == end:
            S.append(neighbour)
            resultDFS()
            return

        # Neighbour state is not end state
        # If it has not neighbours or its all neighbours are passed
        elif neigs[neighbour]==[] or all(elem in V for elem in neigs[neighbour]):
            V.append(neighbour)
            temp = neigs[state]

            # If neighbour state is state's last neighbour
            if temp[-1] == neighbour:
                # We remove last state(state) in S
                # because it has not the path I can go
                S.remove(S[-1])
                return

        # If state has other neighbours
        S.append(neighbour)
        V.append(neighbour)

        # look neighbour's neighbours
        loop(neighbour,end)
        break

def DFS(start,end):

    S.append(start)     # first state is 'start'
    V.append(start)     # cannot turn 'start' state
    loop(start,end)

DFS(start,end)


## UCS -----------------------------------------------------------------------------------
V = []      # Visited   -   to keep states whom distances between all neighbors are known
L = []      # List      -   to keep paths I can go and their distances



# Print result
def resultUCF(l):
    print("UCS : " + ' - '.join(L[l][:-1]))
    exit(0)

# find the shortest distance to select the next state
def findMin(end,time=0):

    min = L[0][-1]  # start by assuming the first distance is the shortest
    loc = 0         # use it where the shortest path

    # find the shortest
    for i in L:
        distance = i[-1]
        if distance < min:
            min = distance
            loc = L.index(i)

    node = L[loc][-2]     # find paths that can go with this state
    new = L[loc]          # to use when to remove from the list or to get items in it

    # find end state
    if node == end:
        resultUCF(loc)

    # paths to go through that node state are not known
    if node not in V:

        # look to know all paths that can go through node state
        for states in dist:
            if time == len(neigs[node])+1:    # ex; neigs[D] = (['A', 'C', 'E'])
                break                         # there is just 3 paths that can go, do not need go on

            # dist list covers two corners and their distances
            # ex; [('A', 'B', 6)]
            first_state = states[0]     # ex; first_state = 'A'
            second_state = states[1]    # ex; second_state = 'B'

            # one of states is the node
            if first_state == node or second_state == node :
                time = time + 1

                # If first and second states are in V,
                # that means they are passed on a shorter path

                # If they are not in V
                if second_state not in V and first_state not in V:
                    # *new[:-1] -> get items except distance
                    # new[-1] + states[-1] -> total distances between pass path and neighbour state
                    # ex; tuple = ('A', 'D', 'E', 'F', 13)
                    if first_state == node:
                        tuple = (*new[:-1],second_state,new[-1] + states[-1])
                        L.append(tuple)
                    else:
                        tuple = (*new[:-1],first_state,new[-1] + states[-1])
                        L.append(tuple)

        # node state's distances from all neighbors are known, then add it to V
        V.append(node)

    # all paths that can go with this state are added, so remove it
    L.remove(new)
    # Again look at distances to select next path
    findMin(end)

def UCF(start,end):

    m = 0
    max = len(neigs[start])     # number of start's neighbors
    for n in dist:
        if m == max:
            break
        elif n[0] == start:
            L.append((start,n[1],n[2]))
            m=m+1
        elif n[1] == start:
            L.append((start,n[0],n[2]))
            m=m+1

    # ex; L = [('A', 'B', 6), ('A', 'C', 4), ('A', 'D', 3)]
    # start state's distances from all neighbors are known, then add it to V
    V.append(start)

    # find the shortest distance to select next path
    findMin(end)


UCF(start,end)
