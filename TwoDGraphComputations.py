"""
CSC111: TwoDGraphComputations

This module contains all methods necessary to perform computations necessary in generating a 2 dimensional
representation of our WIKILINK graph, including generating coordinates, and finding neighbours. These methods will be
called in the methods of the TwoDGraphGraphics module


"""


import math
import random

from GraphMethods import Graph

# constants
display_width = 1000
display_height = 800
radius = 15


def create_coodinates(graph: Graph) -> dict[str:tuple[int, int]]:
    dict_so_far = {}
    for node in graph.get_vertices():
        new_coordinates = generate_random_coordiante(dict_so_far)
        dict_so_far[node] = new_coordinates
    return dict_so_far


def generate_random_coordiante(dict_so_far: dict[str:tuple[int, int]]) -> tuple[int, int]:
    random_tuple = (
        round(random.uniform(radius, display_width - radius)), round(random.uniform(radius, display_height - radius)))

    while any(math.dist(random_tuple, dict_so_far[node]) < 3 * radius for node in dict_so_far):
        random_tuple = (round(random.uniform(radius, display_width - radius)),
                        round(random.uniform(radius, display_height - radius)))

    return random_tuple


def all_neighbours(graph: Graph) -> list[tuple[str, str]]:
    list_so_far = []
    for node in graph.get_vertices():
        for neighbour in graph.get_vertex(node).get_neighbours():
            if tuple(sorted((node, neighbour.get_item()))) not in list_so_far:
                list_so_far.append(tuple(sorted((node, neighbour.get_item()))))
    return list_so_far
