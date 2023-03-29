import math
import random

import pygame

from Project.GraphHelper import Graph
from graph_data import graph
from math import dist
import GraphHelper

# constants
display_width = 800
display_height = 600
radius = 30

# colors
white = (255, 255, 255)  # discovered state
blue = (50, 50, 160)  # completed state fill


def run(dict_so_far: dict[str:tuple[int, int]], final_graph: Graph):
    global screen, edges  # to share with other methods

    build_edges()
    pygame.init()

    screen = pygame.display.set_mode((display_width, display_height))
    clock = pygame.time.Clock()

    screen.fill((0, 0, 0,))

    # for n1, n2 in edges:
    #     pygame.draw.line(screen, white, graph[n1][0], graph[n2][0], 2)

    for node in final_graph.get_vertices():
        for node_2 in final_graph.get_vertices():
            if final_graph.get_vertices()[node_2] in final_graph.get_vertices()[node].get_neighbours():
                pygame.draw.line(screen, white, dict_so_far[node], dict_so_far[node_2], 2)

    for node in dict_so_far:
        circle_fill(dict_so_far[node], white, blue, 25, 2)

    pygame.display.update()

    while 1:  # wait for stop
        clock.tick(60)


def circle_fill(xy, line_color, fill_color, radius, thickness):
    global screen
    # draw grey circle and then a smaller black to get 2 pixel circle
    pygame.draw.circle(screen, line_color, xy, radius)
    pygame.draw.circle(screen, fill_color, xy, radius - thickness)


def edge_id(n1, n2):  # normalize id for either order
    # (1,2) and (2,1) become (1,2)
    return tuple(sorted((n1, n2)))


def build_edges():
    global edges
    edges = {}
    for n1, (_, adjacents) in enumerate(graph):
        for n2 in adjacents:
            eid = edge_id(n1, n2)
            if eid not in edges:
                edges[eid] = (n1, n2)


def createCoodinates(graph: Graph) -> dict[str:tuple[int, int]]:
    dict_so_far = {}
    for node in graph.get_vertices():
        dict_so_far[node] = generate_random_coordiante(dict_so_far)
    return dict_so_far


def generate_random_coordiante(dict_so_far: dict[str:tuple[int, int]]) -> tuple[int, int]:
    random_tuple = (round(random.uniform(0, display_height)), round(random.uniform(0, display_width)))
    for node in dict_so_far:
        if math.dist(random_tuple, dict_so_far[node]) < radius:
            random_tuple = (round(random.uniform(0, display_height)), round(random.uniform(0, display_width)))

    return random_tuple
