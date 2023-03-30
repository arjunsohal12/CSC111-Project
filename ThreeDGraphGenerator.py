import random
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
import GraphHelper


def generate_coordinates(graph: GraphHelper.Graph):
    # Generate a dict of positions
    vertices = graph.get_vertices()
    pos = {(vertex, vertices[vertex]): (random.uniform(0, 4), random.uniform(0, 3), random.uniform(0, 3)) for vertex in
           vertices}

    return pos


def network_plot_3D(graph, pos_dict, angle):
    n = len(graph.get_vertices())
    cmap = plt.colormaps['plasma']
    # Get the maximum number of edges adjacent to a single node
    edge_max = max([vertex[1].get_degree() for vertex in pos_dict])
    # Define color range proportional to number of edges adjacent to a single node
    colors = [cmap(vertex[1].get_degree() / edge_max) for vertex in pos_dict]

    # 3D network plot
    with plt.style.context('ggplot'):
        global ax
        global fig
        global scat

        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(projection='3d')

        # Loop on the pos dictionary to extract the x,y,z coordinates of each node
        i = 0
        for key, value in pos_dict.items():
            xi = value[0]
            yi = value[1]
            zi = value[2]

            # Scatter plot
            scat = ax.scatter(xi, yi, zi, c=colors[i], s=20 + 20 * key[1].get_degree(), edgecolors='k', alpha=0.7)
            i += 1
        # Loop on the list of edges to get the x,y,z, coordinates of the connected nodes
        # Those two points are the extrema of the line to be plotted
        for item, vertex in pos_dict:
            for neighbour in vertex.neighbours:
                vertuple = pos_dict[(item, vertex)]
                neightuple = pos_dict[(neighbour.item, neighbour)]
                x = np.array((vertuple[0], neightuple[0]))
                y = np.array((vertuple[1], neightuple[1]))
                z = np.array((vertuple[2], neightuple[2]))

                # Plot the connecting lines
                ax.plot(x, y, z, c='black', alpha=0.5)

    # Hide the axes
    ax.set_axis_off()
    # rotate graph
    #
    # for angle in range(0, 360):
    #     ax.view_init(30, angle)
    #     plt.draw()
    #     plt.pause(.000000000000000000000000001)
    #
    # return




def init():
    ax.view_init(elev=10., azim=0)
    return [scat]


def animate(i):
    ax.view_init(elev=10., azim=i)
    plt.draw()
    plt.pause(0.000001)
    return [scat]


def run_animation(graph: GraphHelper.Graph):
    posdict = generate_coordinates(graph)
    network_plot_3D(graph, posdict, 0)
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=360, interval=20, blit=True)
    plt.show()


# graph1 = GraphHelper.Graph()
# graph1.add_vertex('https://en.wikipedia.org/wiki/Hart_House')
# GraphHelper.generate_graph(graph1, 'https://en.wikipedia.org/wiki/Hart_House', 2)
# run_animation(graph1)
