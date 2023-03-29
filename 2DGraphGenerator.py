import math
import random

import pygame

from Project.GraphHelper import Graph, generate_graph

# constants
display_width = 1000
display_height = 800
radius = 15

# colors
white = (255, 255, 255)  # discovered state
blue = (50, 50, 160)  # completed state fill


def run(dict_so_far: dict[str:tuple[int, int]], final_graph: Graph):
    global screen, edges  # to share with other methods

    pygame.init()

    screen = pygame.display.set_mode((display_width, display_height))
    clock = pygame.time.Clock()

    screen.fill((0, 0, 0,))

    # for n1, n2 in edges:
    #     pygame.draw.line(screen, white, graph[n1][0], graph[n2][0], 2)

    neighbours_list = all_neighbours(final_graph)

    for neighbours_pair in neighbours_list:
        pygame.draw.line(screen, white, dict_so_far[neighbours_pair[0]], dict_so_far[neighbours_pair[1]], 2)

    for node in dict_so_far:
        circle_fill(dict_so_far[node], white, blue, radius, 2)

    pygame.display.update()

    while 1:  # wait for stop
        clock.tick(60)


def circle_fill(xy, line_color, fill_color, radius, thickness):
    global screen
    # draw grey circle and then a smaller black to get 2 pixel circle
    pygame.draw.circle(screen, line_color, xy, radius)
    pygame.draw.circle(screen, fill_color, xy, radius - thickness)


def createCoodinates(graph: Graph) -> dict[str:tuple[int, int]]:
    dict_so_far = {}
    for node in graph.get_vertices():
        new_coordinates = generate_random_coordiante(dict_so_far)
        dict_so_far[node] = new_coordinates
    return dict_so_far


def generate_random_coordiante(dict_so_far: dict[str:tuple[int, int]]) -> tuple[int, int]:
    random_tuple = (
        round(random.uniform(radius, display_width - radius)), round(random.uniform(radius, display_height - radius)))
    i = 0
    while any(math.dist(random_tuple, dict_so_far[node]) < 3 * radius for node in dict_so_far):
        print(i)
        i += 1

        random_tuple = (round(random.uniform(radius, display_width - radius)),
                        round(random.uniform(radius, display_height - radius)))

    return random_tuple


def all_neighbours(graph: Graph) -> list[tuple[str, str]]:
    list_so_far = []
    for node in graph.get_vertices():
        for neighbour in graph.get_vertices()[node].get_neighbours():
            if tuple(sorted((node, neighbour.get_item()))) not in list_so_far:
                list_so_far.append(tuple(sorted((node, neighbour.get_item()))))
    return list_so_far


graph1 = Graph()
graph1.add_vertex('https://en.wikipedia.org/wiki/Canada')
generate_graph(graph1, 'https://en.wikipedia.org/wiki/Canada', 2)
dicti = createCoodinates(graph1)
run(dicti, graph1)

