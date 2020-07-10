import sys
import os
from enum import Enum


class Status(Enum):
    UNVISITED = 0
    VISITED = 1
    CHECKED = 2


class Node:
    # G Cost = distance from starting node
    # H Cost = distance from ending node
    # F Cost = G Cost + H Cost

    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0
        self.parent_node = (0, 0)
        self.status = Status.UNVISITED

    def set_g_cost(self, p_g_cost):
        self.g_cost = p_g_cost
        self.update_f_cost()

    def set_h_cost(self, p_h_cost):
        self.h_cost = p_h_cost
        self.update_f_cost()

    def update_f_cost(self):
        self.f_cost = self.g_cost + self.h_cost


def maze_file_to_array(p_maze_file):
    r_maze = []
    for y, line in enumerate(p_maze_file.readlines()):
        r_maze.append([])
        for x, number in enumerate(line):
            if number != ' ' and number != '\n':
                r_maze[y].append(int(number))
    return r_maze


def init_maze(p_maze):
    height = len(p_maze) - 1
    width = len(p_maze[0]) - 1
    r_unvisited_nodes, r_start, r_end = {}, [], []

    for y, line in enumerate(p_maze):
        for x, number in enumerate(line):
            if number == 0:
                coordinates = (x, y)
                if x == 0 or y == 0:
                    r_start = coordinates
                elif x == width or y == height:
                    r_end = coordinates

                r_unvisited_nodes[coordinates] = Node(coordinates)

    return r_unvisited_nodes, r_start, r_end


maze_filename = sys.argv[1]

if not os.path.isfile(maze_filename):
    print("Wrong argument, need a file...")
    exit()

maze_file = open(maze_filename, 'r', encoding="utf-8")

print(maze_file.read())
maze_file.seek(0)

maze = maze_file_to_array(maze_file)
unvisited_nodes, start, end = init_maze(maze)

# for node in unvisited_nodes:
#     unvisited_nodes[node].set_g_cost(3)
#     unvisited_nodes[node].set_h_cost(2)
#     #unvisited_nodes[node].print_node()
#     #print("OK" if unvisited_nodes[node].coordinates == [0, 1] else "KO")
# #print(unvisited_nodes[start].print_node())
# print(unvisited_nodes[end].f_cost)





