import sys
import os
from enum import Enum
import math


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
        self.g_cost = math.inf
        self.h_cost = math.inf
        self.f_cost = math.inf
        self.parent = (0, 0)
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

    return [r_nodes, r_start, r_end]


def print_solved_maze(p_maze, p_maze_info):
    """
    Print the solved maze

    :param p_maze: The maze
    :param p_maze_info: The maze information
    """

    nodes, start, end = p_maze_info
    maze_string = ""
    visited_nodes = get_nodes_by_status(nodes, Status.VISITED)

    for y, line in enumerate(p_maze):
        for x, number in enumerate(line):
            tmp = str(number) + " "
            if (x, y) == start:
                tmp = "S "
            elif (x, y) == end:
                tmp = "E "
            else:
                for coord in visited_nodes:
                    if (x, y) == nodes[coord].coordinates:
                        tmp = "X "

            maze_string += tmp
        maze_string += '\n'

    print(maze_string)


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


def solve_maze(current_pos, p_maze, maze_info):
    nodes, start, end = maze_info
    # If first occurrence
    if current_pos == 0:
        solve_maze(start, p_maze, maze_info)
        return
    # If the exit is found
    elif current_pos == end:
        print_solved_maze(p_maze, maze_info)
        return
    # If no solution
    elif current_pos == -1:
        return

    current_node = nodes[current_pos]
    next_node = -1
    current_node.status = Status.VISITED

    print(current_node.coordinates)
    print(current_node.parent)

    # Loop on neighboring nodes
    for coord in get_neighbors(nodes, current_node):
        nodes[coord].status = Status.CHECKED
        nodes[coord].parent = current_node.coordinates

    print(get_nodes_by_status(nodes, Status.VISITED))

    # Choose the next node
    for coord in get_nodes_by_status(nodes, Status.CHECKED):
        next_node = coord

    print(" ")
    solve_maze(next_node, p_maze, maze_info)


def main():
    maze_filename = sys.argv[1]

    if not os.path.isfile(maze_filename):
        print("Wrong argument, need a file...")
        exit()

    maze_file = open(maze_filename, 'r', encoding="utf-8")

    print(maze_file.read())
    maze_file.seek(0)

    maze = maze_file_to_array(maze_file)
    solve_maze(0, maze, init_maze(maze))


if __name__ == "__main__":
    main()

