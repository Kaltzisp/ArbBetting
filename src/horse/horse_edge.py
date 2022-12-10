import numpy as np
from itertools import combinations
import sympy
from scipy.optimize import linprog
import itertools

backs = np.array(sorted([5, 6.5, 2.5, 21, 4.8, 23, 5.5]))
horses = [i for i in range(len(backs))]
win_list = [list(i) for i in combinations(horses, 3)]

# bet total volume of 1 unit
payout_list = []
for i in range(len(horses)):
    for lst in win_list:
        scenario_list = [0.65 for i in range(len(horses))]
        for top_3 in lst:
            scenario_list[top_3] = 0.65
        scenario_list[i] = backs[i]
        payout_list.append(scenario_list)

bounds = [0, 3]

while bounds[1] - bounds[0] > 0.001:
    res = linprog(np.array([0 for i in range(len(horses))]), A_ub=-np.array(payout_list), b_ub=[-(bounds[0]+bounds[1])/2 for i in range(len(payout_list))], A_eq=np.array([[1 for i in range(len(horses))]]), b_eq=np.array([1]))
    if res['success'] == False:
        bounds[1] = (bounds[0]+bounds[1])/2
    else:
        bounds[0] = (bounds[0]+bounds[1])/2 
x = linprog(np.array([0 for i in range(len(horses))]), A_ub=-np.array(payout_list), b_ub=[-bounds[0] for i in range(len(payout_list))], A_eq=np.array([[1 for i in range(len(horses))]]), b_eq=np.array([1]))['x']
print(bounds)

lst = []
for i in np.array(payout_list):
    lst.append(sum(x*i))
print(min(lst), max(lst))

bounds = [0, 3]
while bounds[1] - bounds[0] > 0.001:
    res = linprog(np.array([0 for i in range(len(horses))]), A_ub=np.array(payout_list), b_ub=[(bounds[0]+bounds[1])/2 for i in range(len(payout_list))], A_eq=np.array([[1 for i in range(len(horses))]]), b_eq=np.array([1]))
    if res['success'] == True:
        bounds[1] = (bounds[0]+bounds[1])/2
    else:
        bounds[0] = (bounds[0]+bounds[1])/2 
x = linprog(np.array([0 for i in range(len(horses))]), A_ub=np.array(payout_list), b_ub=[bounds[1] for i in range(len(payout_list))], A_eq=np.array([[1 for i in range(len(horses))]]), b_eq=np.array([1]))['x']
print(bounds)

lst = []
for i in np.array(payout_list):
    lst.append(sum(x*i))
print(min(lst), max(lst))


# import itertools
# def prod(lst, multi):
#     x = 1
#     for i in lst:
#         x *= i
#     return(x)

# games = [(2.38, 1.56),
#          (3.30, 1.32),
#          (1.45, 1.32)]

# multi_combo = list(itertools.product([0, 1], repeat=3))

# payout_list = []
# for i, multi_1 in enumerate(multi_combo):
#     scenario_list = [0 for i in range(len(multi_combo))]
#     scenario_list[i] = prod()
#     for j, multi_2 in enumerate(multi_combo):
#         scenario_list = [0 for i in range(len(multi_combo))]




