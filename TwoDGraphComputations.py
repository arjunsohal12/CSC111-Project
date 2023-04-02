"""
CSC111: TwoDGraphComputations
This module contains all methods necessary to perform computations necessary in generating a 2 dimensional
representation of our WIKILINK graph, including generating coordinates, and finding neighbours. These methods will be
called in the methods of the TwoDGraphGraphics module
This file is Copyright (c) 2023 Arjun Sohal, Mani Tahami.
"""
import math
import random

from GraphMethods import Graph


DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 800
RADIUS = 15

def create_coodinates(graph: Graph) -> dict[str:tuple[int, int]]:
    """Creates a dictionary of random (x,y) coordinates for each vertex in the graph"""
    dict_so_far = {}
    for node in graph.get_vertices():
        new_coordinates = generate_random_coordiante(dict_so_far)
        dict_so_far[node] = new_coordinates
    return dict_so_far


def generate_random_coordiante(coordinates_dict: dict[str:tuple[int, int]]) -> tuple[int, int]:
    """
    Generates a random coordinate tuple that does not overlap with any existing coordinates in the given dictionary.

    Preconditions:
        - all(0 <= coordinates_dict[key][0] <= DISPLAY_WIDTH for key in coordinates_dict)
        - all(0 <= coordinates_dict[key][1] <= DISPLAY_HEIGHT for key in coordinates_dict)
    """
    random_tuple = (
        round(random.uniform(RADIUS, DISPLAY_WIDTH - RADIUS)), round(random.uniform(RADIUS, DISPLAY_HEIGHT - RADIUS)))

    while any(math.dist(random_tuple, coordinates_dict[node]) < 3 * RADIUS for node in coordinates_dict):
        random_tuple = (round(random.uniform(RADIUS, DISPLAY_WIDTH - RADIUS)),
                        round(random.uniform(RADIUS, DISPLAY_HEIGHT - RADIUS)))

    return random_tuple


def all_neighbours(graph: Graph) -> list[tuple[str, str]]:
    """ Returns a list of all unique pairs of neighbouring vertices in the given graph."""

    list_so_far = []
    for node in graph.get_vertices():
        for neighbour in graph.get_vertex(node).get_neighbours():
            if tuple(sorted((node, neighbour.get_item()))) not in list_so_far:
                list_so_far.append(tuple(sorted((node, neighbour.get_item()))))
    return list_so_far
