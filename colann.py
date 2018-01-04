import random
import copy
import math
import fileinput
import sys


def cost(coloring, adjacency):
    sc = size_cost(coloring, adjacency)
    bc = bad_cost(coloring, adjacency)
    return sc, bc


def size_cost(coloring, adjacency):
    return -sum((len(color)**2 for color in coloring))


def bad_cost(coloring, adjacency):
    cost = 0

    for color in coloring:
        for i, vert_num in enumerate(color):
            for k in range(i+1, len(color)):
                if adjacency[vert_num][color[k]] == 1:
                    cost += 2 * len(color)

    return cost


def gen_neighbor(coloring):
    coloring = copy.deepcopy(coloring)

    color_no = random.randrange(len(coloring))
    vertex_no = random.randrange(len(coloring[color_no]))

    vertex = coloring[color_no].pop(vertex_no)

    new_color_no = random.randrange(len(coloring))
    if new_color_no >= color_no:
        new_color_no += 1

    if new_color_no == len(coloring):
        coloring.append([vertex])
    else:
        coloring[new_color_no].append(vertex)

    if len(coloring[color_no]) == 0:
        del coloring[color_no]

    return coloring


INITTEMP = 10
CUTOFF = 0.1
FREEZE_LIM = 5
MINPERCENT = 0.02

TEMPFACTOR = 0.95
SIZEFACTOR = 2

OUTER_LOOP_LIMIT = 10
INNER_LOOP_LIMIT = 100

def gen_init_coloring(length):
    return [list(range(length))]


def annealing(adjacency):
    nb_size = len(adjacency)**2
    current = best = gen_init_coloring(len(adjacency))
    current_cost = best_cost = cost(best, adjacency)
    freezecount = 0
    temp = INITTEMP

    outer_c = 0
    inner_c = 0

    first_changes = -1
    while freezecount < FREEZE_LIM and outer_c < OUTER_LOOP_LIMIT:
        changes = trials = 0
        while trials < SIZEFACTOR * nb_size and changes < CUTOFF * nb_size and inner_c < INNER_LOOP_LIMIT:
            trials += 1
            new = gen_neighbor(current)
            new_cost = cost(new, adjacency)
            cost_diff = sum(new_cost) - sum(current_cost)
            if cost_diff <= 0:
                changes += 1
                current = new
                current_cost = new_cost
                if sum(new_cost) < sum(best_cost):
                    best = new
                    best_cost = new_cost
                    freezecount = 0
            else:
                if random.random() <= math.e ** (-cost_diff / temp):
                    changes += 1
                    current = new

        temp *= TEMPFACTOR
        if changes / trials < MINPERCENT:
            freezecount += 1
        if first_changes == -1:
            first_changes = changes
            print("LPPL: " + str(changes))

    return (best, best_cost)


def load_adjacency_matrix():
    matrix = []
    for line in fileinput.input():
        row = [int(x) for x in line.split()]
        if len(row) > 1:
            matrix.append(row)

    return matrix


def is_legal(solution):
    return solution[1][1] == 0


def print_coloring(solution):
    coloring, cost = solution

    print('Best coloring found:')
    for color in coloring:
        print(color.__str__()[1:-1])

    print('\nColors used:', len(coloring))
    print('Cost of solution:', sum(cost))
    print('Is coloring legal:', ('YES' if is_legal(solution) else 'NO'))


def print_graph(adjacency_matrix):
    print('Graph adjacency matrix:')
    for row in adjacency_matrix:
        for val in row:
            print(val, end=' ')
        print()
    print()


ILLEGAL_COLORING_ERROR_CODE = 2


if __name__ == '__main__':
    adjacency = load_adjacency_matrix()
    sln = annealing(adjacency)
    print_graph(adjacency)
    print_coloring(sln)
    if not is_legal(sln):
        sys.exit(ILLEGAL_COLORING_ERROR_CODE)
