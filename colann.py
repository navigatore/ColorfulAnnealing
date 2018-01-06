import random
import copy
import math
import fileinput
import sys
import argparse
import codecs

def cost(coloring, adjacency):
    sc = size_cost(coloring, adjacency)
    bc = bad_cost(coloring, adjacency)
    return sc, bc


def size_cost(coloring, adjacency):
    return -sum((len(color[0])**2 for color in coloring))


def bad_cost(coloring, adjacency):
    return sum ([2 * len(color[0]) * color[1] for color in coloring])


def count_bad_edges(color, adjacency_row):
    return len([1 for x in color[0] if adjacency_row[x] == 1])

def gen_neighbor(coloring):
    coloring = copy.deepcopy(coloring)

    color_no = random.randrange(len(coloring))
    vertex_no = random.randrange(len(coloring[color_no][0]))

    vertex = coloring[color_no][0].pop(vertex_no)

    coloring[color_no][1] -= count_bad_edges(coloring[color_no], adjacency[vertex])

    new_color_no = random.randrange(len(coloring))
    if new_color_no >= color_no:
        new_color_no += 1

    if new_color_no == len(coloring):
        coloring.append([[vertex], 0])
    else:
        coloring[new_color_no][0].append(vertex)
        coloring[new_color_no][1] += count_bad_edges(coloring[new_color_no], adjacency[vertex]) 

    if len(coloring[color_no][0]) == 0:
        del coloring[color_no]

    return coloring


TEMPFACTOR = 0.95

def gen_init_coloring(length):
    return [ [[x], 0] for x in range(length) ]


def annealing(adjacency, init_temp, outer_lim, inner_lim):
    nb_size = len(adjacency)**2
    current = best = gen_init_coloring(len(adjacency))
    current_cost = best_cost = cost(best, adjacency)
    freezecount = 0
    temp = init_temp

    outer_c = 0

    first_changes = -1
    while outer_c < outer_lim:
        outer_c += 1
        changes = trials = 0
        inner_c = 0
        while inner_c < inner_lim:
            inner_c += 1
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
        if first_changes == -1:
            first_changes = changes
            print("LPPL: " + str(changes/inner_lim))

    return (best, best_cost)


def load_adjacency_matrix():
    matrix = []
    for line in fileinput.input([]):
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
        print(color[0].__str__()[1:-1], '|', color[1], 'BE')

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
    parser = argparse.ArgumentParser()
    parser.add_argument('init_temp', type=float, help='initial temperature')
    parser.add_argument('outer_lim', type=int, help='number of iterations in an outer loop of algorithm')
    parser.add_argument('inner_lim', type=int, help='number of iterations in an inner loop (where temperature is constant)')
    args = parser.parse_args()

    adjacency = load_adjacency_matrix()
    sln = annealing(adjacency, args.init_temp, args.outer_lim, args.inner_lim)
    # print_graph(adjacency)
    print_coloring(sln)
    if not is_legal(sln):
        sys.exit(ILLEGAL_COLORING_ERROR_CODE)
