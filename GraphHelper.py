from __future__ import annotations

import heapq
import math
from typing import Any

import web_scraper

sum_weightage = []

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
        return self.neighbours

    def get_item(self) -> str:
        return self.item


class Graph:
    """A graph.
    Representation Invariants:
    - all(item == self._vertices[item].item for item in self._vertices)
    """
    # Private Instance Attributes:
    #     - _vertices: A collection of the vertices contained in this graph.
    #                  Maps item to _Vertex instance.
    center: str
    _vertices: dict[str, _Vertex]
    items: set[str]
    sum_weightage: list[float]
    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}
        self.items = set()
        self.center = ''
        self.sum_weightage = []
    def add_vertex(self, item: Any) -> None:
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

    def num_connections(self, item: Any) -> int:
        """Return a set of the neighbours of the given item.
        Note that the *items* are returned, not the _Vertex objects themselves.
        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return len(v.neighbours)
        else:
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.
        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_vertices(self) -> dict:
        """
        returns dict of vertices
        """
        return self._vertices

    def get_vertex(self, item) -> _Vertex:
        """
        returns vertex with item
        """
        return self._vertices[item]

    def closestNodesToEachNode(self, src: str) -> set[str]:
        minimum = 2 * (sum(self.sum_weightage) / len(self.sum_weightage))
        print(minimum)
        pq = []
        heapq.heappush(pq, (0, src))
        dist = {a: math.inf for a in self._vertices}
        dist[src] = 0

        while pq:
            d, u = heapq.heappop(pq)
            for v, weight in self._vertices[u].neighbours.items():
                if dist[v.item] > dist[u] + weight:
                    dist[v.item] = dist[u] + weight
                    heapq.heappush(pq, (dist[v.item], v.item))

        set_so_far = set()
        for i in dist:
            print(f"{i} \t\t {dist[i]}")
            if dist[i] < minimum and i != src:
                set_so_far.add(i)

        return set_so_far


def generate_graph(graph_so_far: Graph, url: str, depth: int) -> Graph:
    """
    Generates a WikiLink graph
    """

    if depth == 0:
        return graph_so_far

    else:
        linkdict = web_scraper.get_url(url)
        depth = depth - 1
        for entry in linkdict:
            graph_so_far.add_vertex(entry)
            graph_so_far.add_edge(url, entry, linkdict[entry])
            graph_so_far.sum_weightage.append(1 / linkdict[entry])
            generate_graph(graph_so_far, entry, depth)

# graph1 = Graph()
# graph1.add_vertex('https://en.wikipedia.org/wiki/Canada')
# generate_graph(graph1, 'https://en.wikipedia.org/wiki/Canada', 2)
# graph1.shortestPath('https://en.wikipedia.org/wiki/Canada')
