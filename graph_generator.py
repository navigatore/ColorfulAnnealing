import argparse
import random

def gen_graph(n, p):
    graph = [[0] * n for _ in range(n)]

    for i in range(n - 1):
        for k in range(i + 1, n):
            if random.random() < p:
                graph[i][k] = graph[k][i] = 1

    return graph


def print_graph(adjacency_matrix):
    for row in adjacency_matrix:
        for val in row:
            print(val, end=' ')
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, help='number of vertices in generated graph')
    parser.add_argument('p', type=float, help='probability of creating an edge between vertices')
    args = parser.parse_args()

    print_graph(gen_graph(args.n, args.p))
