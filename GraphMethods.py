from __future__ import annotations

import heapq
import math
from typing import Any

import web_scraper


class _Vertex:
    """A vertex in a graph.
    Instance Attributes:
        - item: The data stored in this vertex.
        - neighbours: The vertices that are adjacent to this vertex.
    """
    item: str
    neighbours: dict[_Vertex, float]

    def __init__(self, item: Any, neighbours: dict[_Vertex, float]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.neighbours = neighbours

    def get_degree(self) -> int:
        """
        Returns the degree of this vertex
        """
        return len(self.neighbours)

    def get_neighbours(self) -> dict[_Vertex, float]:
        """
        Return a dictionary containing the neighbouring vertices of this vertex, along with the weight of the edges connecting them.
        """

        return self.neighbours

    def get_item(self) -> str:
        """Return the item held by this node"""
        return self.item


class Graph:
    """A graph.
    Representation Invariants:
    - all(item == self._vertices[item].item for item in self._vertices)
    - all(item == self._vertices[item].item for item in items)
    - all(weight > 0 for weight in self.weightage_list)
    Instance Attributes:
        -center: The center vertex of the graph (a string).
        - items: A set containing the items held by all vertices in the graph (each item is a string).
        - weightage_list: A list containing the weightage of all edges in the graph (each weightage is a float).
    """

    center: str
    items: set[str]
    weightage_list: list[float]
    # Private Instance Attributes:
    #  - _vertices: A dictionary mapping item strings to `_Vertex` instances.
    _vertices: dict[str, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}
        self.items = set()
        self.center = ''
        self.weightage_list = []

    def add_vertex(self, item: str) -> None:
        """Add a vertex with the given item to this graph.
        The new vertex is not adjacent to any other vertices.
        Preconditions:
            - item not in self._vertices
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, {})
            if len(self.items) == 0:
                self.center = item
            self.items.add(item)

    def add_edge(self, item1: Any, item2: Any, weightage: int) -> None:
        """Add an edge between the two vertices with the given items in this graph.
        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.
        Preconditions:
            - item1 != item2
            - weightage != 0
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            if v1 in v2.neighbours and v2 in v1.neighbours:
                v1.neighbours[v2] += 1 / weightage
                v2.neighbours[v1] += 1 / weightage
            else:
                v1.neighbours[v2] = 1 / weightage
                v2.neighbours[v1] = 1 / weightage
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def get_vertices(self) -> dict:
        """
        returns dict of vertices
        """
        return self._vertices

    def get_vertex(self, item: str) -> _Vertex:
        """
        returns vertex with item
        Preconditions:
            - item in self._vertices
        """
        return self._vertices[item]

    def closest_nodes_to_each_node(self, src: str) -> set[str]:
        """
        Finds and returns the set of nodes in the graph that are closest to each node, excluding the source node by
        using the dijkstra's algorithm.

        Preconditions:
        - src in self._vertices
        """

        minimum = 2 * (sum(self.weightage_list) / len(self.weightage_list))
        pq = []
        heapq.heappush(pq, (0, src))
        dist = {a: math.inf for a in self._vertices}
        dist[src] = 0

        while pq:
            _, u = heapq.heappop(pq)
            for v, weight in self._vertices[u].neighbours.items():
                if dist[v.item] > dist[u] + weight:
                    dist[v.item] = dist[u] + weight
                    heapq.heappush(pq, (dist[v.item], v.item))

        set_so_far = set()
        for i in dist:
            if dist[i] < minimum and i != src:
                set_so_far.add(i)

        return set_so_far


def generate_graph(graph_so_far: Graph, url: str, depth: int) -> Graph:
    """
    Generates a WikiLink graph from the given starting URL to a certain depth.

    Preconditions:
    - The graph_so_far parameter is a Graph object that represents the graph generated so far.
    - The url parameter is a string that represents a valid URL for a Wikipedia article.
    - depth >= 0
    """

    if depth == 0:
        return graph_so_far

    else:
        linkdict = web_scraper.get_url(url)
        depth = depth - 1
        for entry in linkdict:
            graph_so_far.add_vertex(entry)
            graph_so_far.add_edge(url, entry, linkdict[entry])
            graph_so_far.weightage_list.append(1 / linkdict[entry])
            generate_graph(graph_so_far, entry, depth)
