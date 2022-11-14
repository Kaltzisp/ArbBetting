import numpy as np
from itertools import combinations
import sympy

backs = np.array([6, 1.28, 2.3, 1.28, 6.5, 5])
horses = [i for i in range(len(backs))]
win_list = [[0] + list(i) for i in combinations(horses[1:], 2)]
loss_list = [list(i) for i in combinations(horses[1:], 3)]

# bet total volume of 1 unit
# if horse wins, payout is 0
# all loss payouts are the same
# solve for the amounts

raw_a = []
raw_b = []

raw_a.append([1] + [0 for i in range(len(horses)-1)])
raw_b.append(0)

for i in range(len(loss_list) - 1):
    row_1 = [0] * len(horses)
    row_2 = [0] * len(horses)
    for horse in loss_list[i]:
        row_1[horse] = backs[horse]
    for horse in loss_list[i+1]:
        row_2[horse] = backs[horse]
    row = [row_1[i]-row_2[i] for i in range(len(horses))]
    raw_a.append(row)
    raw_b.append(0)

raw_a.append([1 for i in range(len(horses))])
raw_b.append(1)

raw_a = np.array(raw_a)

lin_independent_rows = sympy.Matrix(raw_a).T.rref()[1]

a = [raw_a[i] for i in lin_independent_rows]
a = np.array(a)
b = [raw_b[i] for i in lin_independent_rows]
np.array(b)

x = np.linalg.solve(a, b)

print(1)