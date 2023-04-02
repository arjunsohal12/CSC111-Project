"""
CSC111: ThreeDGraphGenerator
This module contains all methods necessary to produce graphics for the 3D portion of the WIKILINK interface. It includes
methods that will produce the graph itself, and color and size the nodes based on their degree.
This file is Copyright (c) 2023 Arjun Sohal, Mani Tahami.
"""
import random

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

from GraphMethods import Graph


def generate_coordinates(graph: Graph):
    """Generates a dictionary of positions for each vertex in the given graph."""
    vertices = graph.get_vertices()
    pos = {(vertex, vertices[vertex]): (random.uniform(0, 4), random.uniform(0, 3), random.uniform(0, 3)) for vertex in
           vertices}

    return pos


def network_plot_3d(pos_dict):
    """
    Generate a 3D network plot from a dictionary of positions.
    """

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


def init():
    """Initialize the 3D network plot by setting the initial view and returning
    the scatter plot object."""
    ax.view_init(elev=10., azim=0)
    return [scat]


def animate(i):
    """
    Update the view of the 3D network plot by changing the azimuthal angle.
    """
    ax.view_init(elev=10., azim=i)
    plt.draw()
    plt.pause(0.000001)
    return [scat]


def run_animation(graph: Graph):
    """Run an animation of a 3D network plot for a given graph."""
    posdict = generate_coordinates(graph)
    network_plot_3d(posdict)
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=360, interval=20, blit=True)
    plt.show()
