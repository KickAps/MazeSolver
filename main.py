import sys
import os
from enum import Enum
import math
import pygame
from pygame.locals import *


class Status(Enum):
    UNVISITED = 0
    VISITED = 1
    CHECKED = 2


class Maze:
    def __init__(self, nodes, start, end):
        self.nodes = nodes
        self.solution = []
        self.start = start
        self.end = end


class Node:
    # G Cost = distance from starting node
    # H Cost = distance from ending node
    # F Cost = G Cost + H Cost

    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.g_cost = math.inf
        self.h_cost = math.inf
        self.f_cost = math.inf
        self.parent = (0, 0)
        self.status = Status.UNVISITED

    def update_f_cost(self):
        self.f_cost = self.g_cost + self.h_cost

    def print_node(self):
        print(self.coordinates, self.g_cost, self.h_cost, self.f_cost, self.parent, self.status)


def maze_file_to_array(p_maze_file):
    """
    Convert the maze from file to array

    :param p_maze_file: The file

    :return: The array
    """

    r_maze = []
    for y, line in enumerate(p_maze_file.readlines()):
        r_maze.append([])
        for x, number in enumerate(line):
            if number != ' ' and number != '\n':
                r_maze[y].append(int(number))
    return r_maze


def init_maze(p_maze):
    """
    Get information from the maze

    :param p_maze: The maze

    :return: The nodes, the start and the end of the maze
    """

    height = len(p_maze) - 1
    width = len(p_maze[0]) - 1
    r_nodes, r_start, r_end = {}, [], []

    for y, line in enumerate(p_maze):
        for x, number in enumerate(line):
            if number == 0:
                coordinates = (x, y)
                # Define the start
                if x == 0 or y == 0:
                    r_start = coordinates
                # Define the end
                elif x == width or y == height:
                    r_end = coordinates
                # Instantiate nodes from coordinates
                r_nodes[coordinates] = Node(coordinates)

    return Maze(r_nodes, r_start, r_end)


def get_final_path(p_maze):
    """
    Give the final path

    :param p_maze: The maze information

    :return: The list of coordinates of the final path
    """

    current_pos = p_maze.end
    final_path = []

    while current_pos != p_maze.start:
        current_pos = p_maze.nodes[current_pos].parent
        final_path.append(current_pos)

    final_path.reverse()

    return final_path


def get_neighbors(nodes, current_node):
    """
    Get the available neighbors of the given node

    :param nodes: The nodes list
    :param current_node: The current nodes

    :return: The list of neighbors coordinates
    """

    x, y = current_node.coordinates
    pos = [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]
    neighbors = []
    for p in pos:
        if p in nodes:
            node = nodes[p]
            # If the neighboring node is not visited
            if node.status != Status.VISITED:
                neighbors.append(node.coordinates)
    return neighbors


def get_nodes_by_status(nodes, status):
    """
    Filter the nodes by status

    :param nodes: The nodes list
    :param status: The status

    :return: The list of nodes coordinates in the given status
    """

    filtered_nodes = []
    for coord in nodes:
        node = nodes[coord]
        # Status filter
        if node.status == status:
            filtered_nodes.append(node.coordinates)

    return filtered_nodes


def get_nodes_distance(coord_1, coord_2):
    """
    Give the distance between two points

    :param coord_1: First point coordinates
    :param coord_2: Second point coordinates

    :return: The distance
    """

    return abs(coord_1[0] - coord_2[0]) + abs(coord_1[1] - coord_2[1])


def solve_maze(current_pos, p_maze):
    """
    Solve the maze recursively

    :param current_pos: The current coordinates
    :param p_maze: The maze
    """

    # If first occurrence
    if current_pos == 0:
        solve_maze(p_maze.start, p_maze)
        return
    # If the exit is found
    elif current_pos == p_maze.end:
        p_maze.solution = get_final_path(p_maze)
        return
    # If no solution
    elif current_pos == -1:
        return

    current_node = p_maze.nodes[current_pos]
    next_node = -1
    do_next = False
    current_node.status = Status.VISITED

    # Loop on neighboring nodes
    for coord in get_neighbors(p_maze.nodes, current_node):
        node = p_maze.nodes[coord]
        node.status = Status.CHECKED

        tmp_cost = get_nodes_distance(node.coordinates, p_maze.start)
        if node.g_cost > tmp_cost:
            node.g_cost = tmp_cost
            node.parent = current_node.coordinates

        tmp_cost = get_nodes_distance(node.coordinates, p_maze.end)
        if node.h_cost > tmp_cost:
            node.h_cost = tmp_cost

        # Update the f cost of the node
        node.update_f_cost()

    # Choose the next node
    max_f_cost = math.inf
    for coord in get_nodes_by_status(p_maze.nodes, Status.CHECKED):
        node = p_maze.nodes[coord]
        if node.f_cost < max_f_cost:
            do_next = True
        elif node.f_cost == max_f_cost and node.h_cost < next_node.h_cost:
            do_next = True
        elif node.f_cost == max_f_cost and node.h_cost == next_node.h_cost and node.g_cost < next_node.g_cost:
            do_next = True

        if do_next:
            max_f_cost = node.f_cost
            next_node = node

    # Recursive call
    solve_maze(next_node.coordinates, p_maze)


def main():
    maze_filename = sys.argv[1]

    if not os.path.isfile(maze_filename):
        print("Wrong argument, need a file...")
        exit()

    maze_file = open(maze_filename, 'r', encoding="utf-8")

    maze_array = maze_file_to_array(maze_file)

    # Needed for large maze
    sys.setrecursionlimit(10000)

    pygame.init()
    app = pygame.display.set_mode((1650, 1050))

    wall = pygame.image.load("gui/grey.png").convert()
    path = pygame.image.load("gui/light_grey.png").convert()
    solution = pygame.image.load("gui/blue.png").convert()

    size = 10
    tmp = wall
    for y, line in enumerate(maze_array):
        for x, number in enumerate(line):
            if number == 0:
                tmp = path
            elif number == 1:
                tmp = wall

            app.blit(tmp, (x*size, y*size))
    pygame.display.flip()

    end = False
    while not end:
        for event in pygame.event.get():
            if event.type == QUIT:
                end = True
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:

                    maze = init_maze(maze_array)
                    solve_maze(0, maze)

                    for pos in maze.solution:
                        app.blit(solution, (pos[0] * size, pos[1] * size))
                        pygame.display.flip()
                        pygame.time.delay(10)

                    app.blit(solution, (maze.end[0] * size, maze.end[1] * size))
                    pygame.display.flip()


if __name__ == "__main__":
    main()
