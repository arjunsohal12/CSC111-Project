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
display_width = 1000
display_height = 800
radius = 15

# colors
white = (255, 255, 255)  # discovered state
blue = (50, 50, 160)  # completed state fill
red = (220, 20, 60)
yellow = (200, 200, 0)
black = (0, 0, 0)
orange = (255, 165, 0)
grey = (100, 100, 100)


def run(dict_so_far: dict[str:tuple[int, int]], final_graph: Graph):
    global rectdict, clock  # to share with other methods
    running = True
    pygame.init()

    screen = pygame.display.set_mode((display_width + 300, display_height))
    clock = pygame.time.Clock()

    screen.fill((0, 0, 0,))
    settingstab = pygame.image.load("Assets/settingsCSC111.png")

    neighbours_list = all_neighbours(final_graph)
    rectdict = {}
    draw_nodes(screen, dict_so_far, neighbours_list, final_graph)

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
                    bfs_anim(final_graph.get_vertex(final_graph.center), final_graph, screen, dict_so_far,
                             neighbours_list)
                elif dfs_rect.collidepoint(event.pos):
                    dfs_anim(final_graph.get_vertex(final_graph.center), final_graph, screen, dict_so_far,
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
                dijkstra_anim(clicked_node, final_graph, screen, dict_so_far, neighbours_list)
                timer = 0
        if not running:
            pygame.quit()
            break
        dt = clock.tick(30) / 1000


def circle_fill(screen: pygame.surface, xy, line_color, fill_color, thickness):
    # draw grey circle and then a smaller black to get 2 pixel circle
    pygame.draw.circle(screen, line_color, xy, radius)
    pygame.draw.circle(screen, fill_color, xy, radius - thickness)


def draw_nodes(screen, dict_so_far, neighbours_list, final_graph,
               color_mappings: dict[_Vertex, tuple[int, int, int]] = None,
               edge_mapping: dict[tuple[str, str], tuple[int, int, int]] = None):
    if color_mappings is None and edge_mapping is None:
        for neighbours_pair in neighbours_list:
            pygame.draw.line(screen, white, dict_so_far[neighbours_pair[0]], dict_so_far[neighbours_pair[1]], 2)

        for node in dict_so_far:
            currect = pygame.Rect(dict_so_far[node][0] - 15, dict_so_far[node][1] - 15, 25, 25)
            rectdict[node] = currect
            if final_graph.center == node:
                circle_fill(screen, dict_so_far[node], white, red, 2)
            else:
                circle_fill(screen, dict_so_far[node], white, blue, 2)
    else:
        for neighbours_pair in edge_mapping:
            pygame.draw.line(screen, edge_mapping[neighbours_pair], dict_so_far[neighbours_pair[0]],
                             dict_so_far[neighbours_pair[1]], 2)

        for node in dict_so_far:
            circle_fill(screen, dict_so_far[node], white, color_mappings[final_graph.get_vertex(node)], 2)

        pygame.display.flip()
        clock.tick(5)


def bfs_anim(start_node: _Vertex, graph: Graph, screen: pygame.surface, dict_so_far: dict[str:tuple[int, int]],
             neighbours_list):
    # Wait 1
    # pygame.time.delay(1000)
    color_mappings = {graph.get_vertex(key): black for key in graph.get_vertices()}
    edge_mapping = {neighbours_pair: grey for neighbours_pair in neighbours_list}

    queue = [start_node]
    while len(queue) > 0:
        currnode = queue.pop(0)
        color_mappings[currnode] = yellow
        color_mappings[start_node] = orange
        for node in currnode.get_neighbours():
            if node not in queue and color_mappings[node] == black:  # not visited yet
                queue.append(node)
                # set coors
                color_mappings[node] = red
                # call draw
                draw_nodes(screen, dict_so_far, neighbours_list, graph, color_mappings, edge_mapping)
                edge = tuple(sorted((node.item, currnode.item)))
                edge_mapping[edge] = white
        color_mappings[currnode] = blue
        draw_nodes(screen, dict_so_far, neighbours_list, graph, color_mappings, edge_mapping)


def dfs_anim(start_node: _Vertex, graph: Graph, screen: pygame.surface, dict_so_far: dict[str:tuple[int, int]],
             neighbours_list, color_mappings=None, edge_mappings=None, first_node=None):
    if color_mappings is None and edge_mappings is None:
        color_mappings = {graph.get_vertex(key): black for key in graph.get_vertices()}
        edge_mappings = {neighbours_pair: grey for neighbours_pair in neighbours_list}

    if color_mappings[start_node] == black:  # not visited yet
        color_mappings[start_node] = yellow
        if first_node is not None:
            color_mappings[first_node] = orange
        draw_nodes(screen, dict_so_far, neighbours_list, graph, color_mappings, edge_mappings)
        for neighbour in start_node.get_neighbours():
            edge = tuple(sorted((start_node.item, neighbour.item)))
            edge_mappings[edge] = white
            dfs_anim(neighbour, graph, screen, dict_so_far, neighbours_list, color_mappings, edge_mappings)

        color_mappings[start_node] = blue
        draw_nodes(screen, dict_so_far, neighbours_list, graph, color_mappings, edge_mappings)


def dijkstra_anim(start_node: str, graph: Graph, screen: pygame.surface, dict_so_far: dict[str:tuple[int, int]],
                  neighbours_list):
    color_mappings = {graph.get_vertex(key): blue for key in graph.get_vertices()}
    edge_mapping = {neighbours_pair: white for neighbours_pair in neighbours_list}

    currnode = graph.get_vertex(start_node)
    color_mappings[currnode] = yellow
    for node in graph.closest_nodes_to_each_node(start_node):
        color_mappings[graph.get_vertex(node)] = red

    draw_nodes(screen, dict_so_far, neighbours_list, graph, color_mappings, edge_mapping)
