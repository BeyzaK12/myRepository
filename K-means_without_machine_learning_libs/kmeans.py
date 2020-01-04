import itertools
import math
import random
from operator import itemgetter
import matplotlib.pyplot as plt

k = int(input('The number of centers: '))

dt = open("./data.txt", 'r')
data = []
j = 0
for i in dt:
    if j == 0:
        j += 1
        continue
    i = i.split(',')
    data.append([int(i[0]),int(i[1][:-1])])

# [[233, 150], [250, 187], [204, 172], [236, 178], [354, 163], [192, 148], [294, 153], [263, 173], [199, 162], ...]
# len(data) = 303

#---------------------------------------------------------------------------------------
# 1. Selects K random points as cluster centers called centroids
centroids = []

while len(centroids) < k:
    p = random.randrange(len(data))
    if p not in centroids:
        centroids.append(p)

# centroids: [236, 188, 20]

n = 0
for l in centroids:
    centroids[n] = data[l]
    n += 1

# centroids: [[300, 171], [233, 163], [234, 161]]

    # centroids[0] -> first centroid's [x,y]
    # centroids[1] -> second centroid's [x,y]
    # ...
    # centroids[k-1] -> last centroid's [x,y]

# centorids will be moved to new locations
for d in centroids:
    data.remove(d)

cls = {}
#---------------------------------------------------------------------------------------
def repeat(centroids):
    clusters = {}
    # {0: [], 1: [], ..., k-1: []}
    i = 0
    for _ in itertools.repeat(None, k):
        clusters[i] = []
        i += 1

    for point in data:
        if point in centroids:
            continue

        # 2. Assigns each data point to the closest cluster by calculating its distance with respect to each centroid
        distances = []
        for centroid in centroids:
            d = math.sqrt(sum([(a - b) ** 2 for a, b in zip(point, centroid)]))
            distances.append((d, centroid))

        distances = sorted(distances,key=itemgetter(0))

        s = 0
        for _ in itertools.repeat(None, len(centroids)):
            x = centroids.__getitem__(s)
            if x == distances[0][1]:
                clusters[s].append(point)
                break
            s += 1

    # 3. Determines the new cluster center by computing the average of the assigned points
    Ncentroids = centroids.copy()

    for kk in clusters:
        if len(clusters[kk]) == 0:
            continue
        Xs = 0
        Ys = 0
        for a in clusters[kk]:
            Xs += a[0]
            Ys += a[1]

        x = int( Xs/len(clusters[kk]) )
        y = int( Ys/len(clusters[kk]) )

        C = [x, y]
        Ncentroids[kk] = C

    # 4. Repeats steps 2 and 3 until none of the cluster assignments change
    if centroids == Ncentroids:
        global cls
        global cens
        cls = clusters
        cens = centroids
        return
    else:
        repeat(Ncentroids)

repeat(centroids)
# cens: [[310, 146], [245, 152], [193, 148]]
# cls: {0: [[354, 163], [294, 153], [283, 162], [340, 172], [302, 162], [417, 157], [304, 170], [360, 151], [308, 142], ...}


for i in cls:
    ii = i+1
    print("")
    print(str(ii) + ". centroid is ", cens[i])
    print("The number of points in its cluster:",len(cls[i]))


x = []
y = []
colors = []
colorsC = []

i = 0
for n in cls:
    cluster = cls[n]
    for point in cluster:
        x.append(point[0])
        y.append(point[1])
        colors.append(i)
    colorsC.append(i+1)
    i += 1


plt.scatter(x, y, s=30, c=colors, cmap='plasma', edgecolors='black', linewidths=1,alpha=0.75)

x = []
y = []

for centroid in cens:
    x.append(centroid[0])
    y.append(centroid[1])

plt.scatter(x, y, s=175, c=colorsC, cmap='plasma', edgecolors='black', marker='X')
plt.title("K-means In Action")
plt.savefig('plot.pdf')

print("\n***The plot was written to the 'plot.pdf' file.***")
plt.show()
