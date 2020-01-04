import itertools
import math
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np

kV = int(input('k: '))

tt = open('./test.txt', 'r')
tn = open('./train.txt', 'r')
train = []
test = []
for line in tn:
    train.append(line)
for line in tt:
    test.append(line)


# ----------------------------------------------------------------------------------------------------
# calculate Euclidean distances
def sec_step(ph):
    distances = []

    j = 0
    for _ in itertools.repeat(None, len(train)):
        if j == 0:
            j += 1
            continue
        opp = train[j]
        opp = opp.split(',')
        opp[-1] = opp[-1][:1]

        i = 0
        for _ in itertools.repeat(None, len(opp)):
            opp[i] = float(opp[i])
            i += 1

        d = math.sqrt(sum([(a - b) ** 2 for a, b in zip(ph, opp)]))
        distances.append((d, opp[-1]))
        j += 1

    distances = sorted(distances, key=itemgetter(0))
    return distances


# ----------------------------------------------------------------------------------------------------
accuracies = []


def main(k):
    acc = 0.0

    length = 0
    for ph in test:
        if length == 0:
            length += 1
            continue

        ph = ph.split(',')
        # battery_power,blue,clock_speed,dual_sim,fc,four_g,int_memory,m_dep,mobile_wt,n_cores,pc,
        # px_height,px_width,ram,sc_h,sc_w,talk_time,three_g,touch_screen,wifi,price_range
        ph[-1] = ph[-1][:1]  # delete \n

        i = 0
        for _ in itertools.repeat(None, len(ph)):
            ph[i] = float(ph[i])
            i += 1

        ds = sec_step(ph)

        # Find the most common 'range' value by looking at the 'range' values ​​of k points around the point
        n0 = 0
        n1 = 0
        n2 = 0
        n3 = 0
        i = 0
        for _ in itertools.repeat(None, k):
            opp_range = int(ds[i][1])
            if opp_range == 0:
                n0 += 1
            elif opp_range == 1:
                n1 += 1
            elif opp_range == 2:
                n2 += 1
            else:
                n3 += 1
            i += 1

        n = [(0, n0), (1, n1), (2, n2), (3, n3)]
        n = sorted(n, key=itemgetter(1))

        # the most common 'range' value == 'range' value
        if n[-1][0] == int(ph[-1]):
            acc += 1

        length += 1

    acc = acc / length
    accuracies.append((k, acc))
    global kV
    if kV == k:
        print("acc:", acc)


numbers = []
if kV > 10:
    for i in range(1, kV):
        numbers.append(i)
        main(i)
else:
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    for i in range(1, 11):
        main(i)

print(accuracies)
# accuracies =
#[(1, 0.8991008991008991),
# (2, 0.8821178821178821),
# (3, 0.9070929070929071),
# (4, 0.9120879120879121),
# (5, 0.9170829170829171),
# (6, 0.919080919080919),
# (7, 0.9240759240759241),
# (8, 0.922077922077922),
# (9, 0.9240759240759241),
# (10, 0.922077922077922)]

accs = []
for x in accuracies:
    accs.append(x[1])

y_pos = np.arange(len(numbers))

plt.barh(y_pos, accs, align='center', color='black')
plt.ylabel('K Values')
plt.xlabel('Accuracies')
plt.title('Accuracies By K Values')
plt.savefig('plot.pdf')

print("\n***The plot was written to the 'plot.pdf' file.***")
plt.show()
