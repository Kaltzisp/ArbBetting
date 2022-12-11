import numpy as np
from itertools import combinations
import sympy
from scipy.optimize import linprog
import itertools

backs = np.array(sorted([3.6, 5.5, 13, 2.35, 5.5]))
horses = [i for i in range(len(backs))]
win_list = [list(i) for i in combinations(horses, 3)]

# bet total volume of 1 unit
payout_list = []
for i in range(len(horses)):
    for lst in win_list:
        scenario_list = [0 for i in range(len(horses))]
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
# def prod(games, multi_combo):
#     x = 1
#     lst = []
#     for i in multi_combo:
#         odds = 1
#         for j, team in enumerate(i):
#             odds *= games[j][team]
#         lst.append(odds)
#     return(lst)

# games = [(2.38, 1.56),
#          (3.30, 1.32),
#          (1.45, 1.32)]

# multi_combo = list(itertools.product([0, 1], repeat=3))
# multi_odds = prod(games, multi_combo)

# payout_list = []
# for i, multi_1 in enumerate(multi_combo):
#     scenario_list = [0 for i in range(len(multi_combo))]
#     scenario_list[i] = multi_odds[i]
#     for j, multi_2 in enumerate(multi_combo):
#         if sum(abs(np.array(multi_1) - np.array(multi_2))) == 1:
#             scenario_list[j] = 0.65
#     payout_list.append(scenario_list)


# bounds = [0, 3]

# while bounds[1] - bounds[0] > 0.001:
#     res = linprog(np.array([0 for i in range(len(multi_combo))]), A_ub=-np.array(payout_list), b_ub=[-(bounds[0]+bounds[1])/2 for i in range(len(payout_list))], A_eq=np.array([[1 for i in range(len(multi_combo))]]), b_eq=np.array([1]))
#     if res['success'] == False:
#         bounds[1] = (bounds[0]+bounds[1])/2
#     else:
#         bounds[0] = (bounds[0]+bounds[1])/2 
# x = linprog(np.array([0 for i in range(len(multi_combo))]), A_ub=-np.array(payout_list), b_ub=[-bounds[0] for i in range(len(payout_list))], A_eq=np.array([[1 for i in range(len(multi_combo))]]), b_eq=np.array([1]))['x']
# print(bounds)

# lst = []
# for i in np.array(payout_list):
#     lst.append(sum(x*i))
# print(min(lst), max(lst))
# print(1)

