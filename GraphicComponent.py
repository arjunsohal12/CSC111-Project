import pygame
import sys
import GraphHelper
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode([1000, 525], pygame.NOFRAME)

def searchbar(graph: GraphHelper.Graph):
    i = 0

    font = pygame.font.Font("Assets/CaviarDreams.ttf", 30)
    font_25 = pygame.font.Font("Assets/CaviarDreams.ttf", 25)
    font_20 = pygame.font.Font("Assets/CaviarDreams.ttf", 20)
    font_25_bold = pygame.font.Font("Assets/CaviarDreams_Bold.ttf", 25)

    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('gray15')
    color = color_passive

    user_text = ''
    text_rect = pygame.Rect(120, 280, 140, 55)

    inputs = []
    active = False

    exit = pygame.image.load("Assets/Exit Right.png")
    exit = pygame.transform.scale(exit, (40, 40))
    exit_rect = pygame.Rect(950, 15, 40, 40)

    bg = pygame.image.load("Assets/SearchBar.png")
    outputlink = ''
    while True:

        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_rect.collidepoint(event.pos):
                    active = True
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        inputs.append(str(user_text))
                        outputlink = 'https://en.wikipedia.org/wiki/' + user_text
                        user_text = ""
                        i += 1
                    else:
                        user_text += event.unicode

        if i == 1:
            graph.add_vertex(outputlink)
            GraphHelper.generate_graph(graph, outputlink, 2)
        screen.blit(bg, (0, 0))
        text_surface = font.render(user_text, True, (0, 0, 0))
        text_rect.w = max((780, text_surface.get_width() + 10))

        screen.blit(text_surface, (text_rect.x + 5, text_rect.y + 10))

        screen.blit(exit, (950, 15))
        pygame.display.flip()
        clock.tick(60)

graph1 = GraphHelper.Graph()
print('hello')

searchbar(graph1)
print('hello')

print(graph1.get_vertices())
