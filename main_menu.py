"""
CSC111: MainMenu
This module contains all methods necessary to run the main menu of WIKILINK, which is the search bar in which we will
input the link to the website we wish to crawl and generate a graph from. This module will call methods from
TwoDGraphGenerator, GraphMethods and web_scraper in order to create the representation of the WIKILINK graph.
This file is Copyright (c) 2023 Arjun Sohal, Mani Tahami.
"""
import pygame

from graph_methods import Graph, generate_graph
from two_d_graph_computations import create_coodinates
from two_d_graph_graphics import run


def run_main_menu() -> None:
    """
    This function runs the main menu for a Wikipedia graph visualization program using the Pygame library.
    The main menu includes a search bar and an exit button, and allows the user to input a topic to search
    for on Wikipedia. If the user presses Enter, the program generates a graph of the Wikipedia page for the given topic
    and displays it using the run() function. The function takes no arguments and returns nothing.
    """
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode([1000, 525], pygame.NOFRAME)
    i = 0

    font = pygame.font.Font("Assets/CaviarDreams.ttf", 30)
    user_text = ''
    text_rect = pygame.Rect(120, 280, 140, 55)

    active = False
    is_error = False

    exit_image = pygame.image.load("Assets/Exit Right.png")
    exit_scaled = pygame.transform.scale(exit_image, (40, 40))
    exit_rect = pygame.Rect(950, 15, 40, 40)

    bg = pygame.image.load("Assets/SearchBar.png")
    try_again_image = pygame.image.load("Assets/TryAgain.jpeg")
    try_again_scaled = pygame.transform.scale(try_again_image, (100, 100))

    running = True
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_rect.collidepoint(event.pos):
                    active = True
                elif exit_rect.collidepoint(event.pos):
                    running = False

                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        try:
                            outputlink = 'https://en.wikipedia.org/wiki/' + user_text.replace(" ", "")
                            user_text = ""
                            graph = Graph()
                            graph.add_vertex(outputlink)
                            generate_graph(graph, outputlink, 2)
                            graph_coordinates = create_coodinates(graph)
                            run(graph_coordinates, graph)
                        except:
                            user_text = ''
                            is_error = True

                        i += 1
                    else:
                        user_text += event.unicode

        if not running:
            pygame.quit()

            break

        screen.blit(bg, (0, 0))
        text_surface = font.render(user_text, True, (0, 0, 0))
        text_rect.w = max((780, text_surface.get_width() + 10))

        screen.blit(text_surface, (text_rect.x + 5, text_rect.y + 10))

        screen.blit(exit_scaled, (950, 15))
        if is_error:
            screen.blit(try_again_scaled, (450, 400))

        pygame.display.flip()
        clock.tick(60)
