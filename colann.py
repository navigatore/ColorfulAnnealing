# cython: language_level=3, boundscheck=False
import random
import copy
import math
import fileinput
import sys
import argparse


def cost(coloring):
    sc = size_cost(coloring)
    bc = bad_cost(coloring)
    return sc, bc


def size_cost(coloring):
    return -sum((len(color[0])**2 for color in coloring))


def bad_cost(coloring):
    return sum([2 * len(color[0]) * color[1] for color in coloring])


def count_bad_edges(color, adjacency_row):
    return len([1 for x in color[0] if adjacency_row[x] == 1])


def gen_neighbor(coloring):
    color_no = random.randrange(len(coloring))
    vertex_no = random.randrange(len(coloring[color_no][0]))

    revert_info = [color_no, coloring[color_no][1], -1, 0]

    vertex = coloring[color_no][0].pop(vertex_no)

    coloring[color_no][1] -= count_bad_edges(coloring[color_no], adjacency[vertex])

    new_color_no = random.randrange(len(coloring))
    if new_color_no >= color_no:
        new_color_no += 1

    if new_color_no == len(coloring):
        coloring.append([[vertex], 0])

    else:
        revert_info[2:] = new_color_no, coloring[new_color_no][1]
        coloring[new_color_no][0].append(vertex)
        coloring[new_color_no][1] += count_bad_edges(coloring[new_color_no], adjacency[vertex])

    if len(coloring[color_no][0]) == 0:
        del coloring[color_no]
        revert_info[0] = -1
        if revert_info[2] > color_no:
            revert_info[2] -= 1
    
    return revert_info


def revert(coloring, revert_info):
    old_idx, old_be, new_idx, new_be = revert_info
    
    if old_idx != -1:
        coloring[old_idx][0].append(coloring[new_idx][0].pop())
        coloring[old_idx][1], coloring[new_idx][1] = old_be, new_be
        if len(coloring[new_idx][0]) == 0:
            del coloring[new_idx]
    
    elif new_idx != -1:
        coloring.append([[coloring[new_idx][0].pop()], 0])
        coloring[new_idx][1] = new_be


TEMPFACTOR = 0.95


def gen_init_coloring(length):
    return [ [[x], 0] for x in range(length) ]
    # return [[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 45]]


def annealing(adjacency, init_temp, outer_lim, inner_lim):
    current = best = gen_init_coloring(len(adjacency))
    current_cost = best_cost = cost(best)
    temp = init_temp
    
    deepcopied = True

    for i in range(outer_lim):
        up_changes = possible_up_changes = 0
        for _ in range(inner_lim):
            revert_info = gen_neighbor(current)
            new_cost = cost(current)
            cost_diff = sum(new_cost) - sum(current_cost)
            if cost_diff <= 0:
                current_cost = new_cost
                if sum(new_cost) < sum(best_cost):
                    deepcopied = False
                    best = current
                    best_cost = new_cost
            else:
                possible_up_changes += 1
                if random.random() <= math.e ** (-cost_diff / temp):
                    up_changes += 1
                    if not deepcopied:
                        best = copy.deepcopy(current)
                        revert(best, revert_info)
                        deepcopied = True
                else:
                    revert(current, revert_info)

        temp *= TEMPFACTOR
        if i == 0:
            print('Accepted upwards jumps (highest temp):', up_changes/possible_up_changes if possible_up_changes != 0 else 0)
            print('Max possible changes:', possible_up_changes)
        elif i == outer_lim - 1:
            print('Accepted upwards jumps (lowest temp):', up_changes/possible_up_changes if possible_up_changes != 0 else 0)
            print('Max possible changes:', possible_up_changes)

    return best, best_cost


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
