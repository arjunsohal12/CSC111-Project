"""
CSC111: TwoDGraphGraphics
This module contains all methods necessary to produce graphics for the 2D portion of the WIKILINK interface. It includes
methods that will produce the graph itself, and perform the dfs, bfs, and dijkstra algorithms.
This file is Copyright (c) 2023 Arjun Sohal, Mani Tahami.
"""
import webbrowser

import pygame

from GraphMethods import Graph, _Vertex
from ThreeDGraphGenerator import run_animation
from TwoDGraphComputations import all_neighbours

# constants
DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 800
RADIUS = 15

# colors
WHITE = (255, 255, 255)  # discoveRED state
BLUE = (50, 50, 160)  # completed state fill
RED = (220, 20, 60)
YELLOW = (200, 200, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
GREY = (100, 100, 100)


def run(graph_coordinates: dict[str:tuple[int, int]], final_graph: Graph):
    """
    Run the graph visualization and interaction program.
    Preconditions:
        - all(node in final_graph.get_vertices() for node in graph_coordinates)
    """
    global rectdict, clock  # to share with other methods
    running = True
    pygame.init()

    screen = pygame.display.set_mode((DISPLAY_WIDTH + 300, DISPLAY_HEIGHT))
    clock = pygame.time.Clock()

    screen.fill((0, 0, 0,))
    settingstab = pygame.image.load("Assets/settingsCSC111.png")

    neighbours_list = all_neighbours(final_graph)
    rectdict = {}
    draw_nodes(screen, graph_coordinates, neighbours_list, final_graph)

    screen.blit(settingstab, (1000, 0))

    exit_rect = pygame.Rect(1182, 699, 50, 50)
    three_d_rect = pygame.Rect(1184, 148, 50, 50)

    dfs_rect = pygame.Rect(1184, 230, 50, 50)
    bfs_rect = pygame.Rect(1184, 300, 50, 50)

    clock.tick(60)
    pygame.display.update()

    timer = 0
    dt = 0
    prevclick = None
    clicked_node = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_rect.collidepoint(event.pos):
                    running = False
                elif three_d_rect.collidepoint(event.pos):
                    run_animation(final_graph)
                elif bfs_rect.collidepoint(event.pos):
                    bfs_anim(final_graph.get_vertex(final_graph.center), final_graph, screen, graph_coordinates,
                             neighbours_list)
                elif dfs_rect.collidepoint(event.pos):
                    dfs_anim(final_graph.get_vertex(final_graph.center), final_graph, screen, graph_coordinates,
                             neighbours_list, first_node=final_graph.get_vertex(final_graph.center))
                for key in rectdict:
                    if rectdict[key].collidepoint(event.pos):
                        clicked_node = key
                        if prevclick != rectdict[key]:
                            timer = 0
                        prevclick = rectdict[key]
                        if timer == 0:  # First mouse click.
                            timer = 0.00001
                        elif timer < 0.5:
                            timer = 0
                            webbrowser.open_new(key)

        if timer != 0:
            timer += dt
            # Reset after 0.5 seconds.
            if timer >= 0.5:
                # run algorithm here after determining its not a double click
                dijkstra_anim(clicked_node, final_graph, screen, graph_coordinates, neighbours_list)
                timer = 0
        if not running:
            pygame.quit()
            break
        dt = clock.tick(30) / 1000


def circle_fill(screen: pygame.surface, xy: tuple[int, int], line_color: tuple[int, int, int],
                fill_color: tuple[int, int, int], thickness: int):
    """
    Draws a circle filled with a specified color and a border line of a different color on a Pygame screen.

    Preconditions:
        - all(0 <= number for number in xy)
        - all(0 <= number <= 255 for number in line_color)
        - all(0 <= number <= 255 for number in fill_color)
        - thickness >= 0
    """
    pygame.draw.circle(screen, line_color, xy, RADIUS)
    pygame.draw.circle(screen, fill_color, xy, RADIUS - thickness)


def draw_nodes(screen: pygame.surface, coordinates_dict: dict[str:tuple[int, int]],
               neighbours_list: list[tuple[str, str]], final_graph: Graph,
               color_mappings: dict[_Vertex, tuple[int, int, int]] = None,
               edge_mapping: dict[tuple[str, str], tuple[int, int, int]] = None):
    """
    Draws the nodes of a graph on a Pygame screen, with optional color mappings for the vertices and edges.

    Preconditions:
        - all(node[0] in final_graph.get_vertices() for node in neighbours_list)
        - all(node[1] in final_graph.get_vertices() for node in neighbours_list)
        - all(node in final_graph.get_vertices() for node in coordinates_dict)
    """
    if color_mappings is None and edge_mapping is None:
        for neighbours_pair in neighbours_list:
            pygame.draw.line(screen, WHITE, coordinates_dict[neighbours_pair[0]], coordinates_dict[neighbours_pair[1]],
                             2)

        for node in coordinates_dict:
            currect = pygame.Rect(coordinates_dict[node][0] - 15, coordinates_dict[node][1] - 15, 25, 25)
            rectdict[node] = currect
            if final_graph.center == node:
                circle_fill(screen, coordinates_dict[node], WHITE, RED, 2)
            else:
                circle_fill(screen, coordinates_dict[node], WHITE, BLUE, 2)
    else:
        for neighbours_pair in edge_mapping:
            pygame.draw.line(screen, edge_mapping[neighbours_pair], coordinates_dict[neighbours_pair[0]],
                             coordinates_dict[neighbours_pair[1]], 2)

        for node in coordinates_dict:
            circle_fill(screen, coordinates_dict[node], WHITE, color_mappings[final_graph.get_vertex(node)], 2)

        pygame.display.flip()
        clock.tick(5)


def bfs_anim(start_node: _Vertex, graph: Graph, screen: pygame.surface, coordinates_dict: dict[str:tuple[int, int]],
             neighbours_list: list[tuple[str, str]]):
    """
    Performs breadth-first search on a given graph starting from the specified start node, and animates the process on a
    Pygame screen.

    Preconditions:
        - start_node in graph.get_vertices()
        - first_node in graph.get_vertices()
        - all(node[0] in graph.get_vertices() for node in neighbours_list)
        - all(node[1] in graph.get_vertices() for node in neighbours_list)
        - all(node in graph.get_vertices() for node in coordinates_dict)
    """
    color_mappings = {graph.get_vertex(key): BLACK for key in graph.get_vertices()}
    edge_mapping = {neighbours_pair: GREY for neighbours_pair in neighbours_list}

    queue = [start_node]
    while len(queue) > 0:
        currnode = queue.pop(0)
        color_mappings[currnode] = YELLOW
        color_mappings[start_node] = ORANGE
        for node in currnode.get_neighbours():
            if node not in queue and color_mappings[node] == BLACK:  # not visited yet
                queue.append(node)
                # set coors
                color_mappings[node] = RED
                # call draw
                draw_nodes(screen, coordinates_dict, neighbours_list, graph, color_mappings, edge_mapping)
                edge = tuple(sorted((node.item, currnode.item)))
                edge_mapping[edge] = WHITE
        color_mappings[currnode] = BLUE
        draw_nodes(screen, coordinates_dict, neighbours_list, graph, color_mappings, edge_mapping)


def dfs_anim(start_node: _Vertex, graph: Graph, screen: pygame.surface, coordinates_dict: dict[str:tuple[int, int]],
             neighbours_list: list[tuple[str, str]], color_mappings=None, edge_mappings=None, first_node=None) -> None:
    """
    Performs depth-first search on a given graph starting from the specified start node, and animates the process on a
    Pygame screen.

    Preconditions:
        - start_node in graph.get_vertices()
        - first_node in graph.get_vertices()
        - all(node[0] in graph.get_vertices() for node in neighbours_list)
        - all(node[1] in graph.get_vertices() for node in neighbours_list)
        - all(node in graph.get_vertices() for node in coordinates_dict)
    """
    if color_mappings is None and edge_mappings is None:
        color_mappings = {graph.get_vertex(key): BLACK for key in graph.get_vertices()}
        edge_mappings = {neighbours_pair: GREY for neighbours_pair in neighbours_list}

    if color_mappings[start_node] == BLACK:
        color_mappings[start_node] = YELLOW
        if first_node is not None:
            color_mappings[first_node] = ORANGE
        draw_nodes(screen, coordinates_dict, neighbours_list, graph, color_mappings, edge_mappings)
        for neighbour in start_node.get_neighbours():
            edge = tuple(sorted((start_node.item, neighbour.item)))
            edge_mappings[edge] = WHITE
            dfs_anim(neighbour, graph, screen, coordinates_dict, neighbours_list, color_mappings, edge_mappings)

        color_mappings[start_node] = BLUE
        draw_nodes(screen, coordinates_dict, neighbours_list, graph, color_mappings, edge_mappings)


def dijkstra_anim(start_node: str, graph: Graph, screen: pygame.surface, coordinates_dict: dict[str:tuple[int, int]],
                  neighbours_list: list[tuple[str, str]]) -> None:
    """
    Performs Dijkstra's algorithm on a given graph starting from the specified start node, and animates the process
    on a Pygame screen.

    Preconditions:
        - start_node in graph.get_vertices()
        - all(node[0] in graph.get_vertices() for node in neighbours_list)
        - all(node[1] in graph.get_vertices() for node in neighbours_list)
        - all(node in graph.get_vertices() for node in coordinates_dict)
    """
    color_mappings = {graph.get_vertex(key): BLUE for key in graph.get_vertices()}
    edge_mapping = {neighbours_pair: WHITE for neighbours_pair in neighbours_list}

    currnode = graph.get_vertex(start_node)
    color_mappings[currnode] = YELLOW
    for node in graph.closest_nodes_to_each_node(start_node):
        color_mappings[graph.get_vertex(node)] = RED

    draw_nodes(screen, coordinates_dict, neighbours_list, graph, color_mappings, edge_mapping)
