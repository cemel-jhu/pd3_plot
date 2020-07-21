import pd3
from pd3.proto.study_pb2 import IMMOBILE
import matplotlib.pyplot as plt
import ipyvolume as ipv
import numpy as np
import matplotlib.cm as cm
from matplotlib import colors as mcolors
from matplotlib.collections import LineCollection
from matplotlib import collections as mc
import pylab as pl
import importlib
import seaborn as sns


class Graph:
    # constructor
    def __init__(self, proto_graph, timestep, color_scheme):
        #set the instance variables
        self.proto_graph = proto_graph
        self.timestep = timestep
        self.not_visited = set()
        self.visited = set()
        self.links = {}
        self.graph_data = {}
        self.node_vectors = {}
        self.color_scheme = color_scheme

        graph = self.proto_graph
        vertices = graph.state[self.timestep].nodes
        edges = graph.state[self.timestep].links
        g = {}

        for edge in edges:
            self.not_visited.add(edge.leading)
            self.not_visited.add(edge.trailing)
            leading_neighbors = g.get(edge.leading, [])
            leading_neighbors.append(edge.trailing)
            trailing_neighbors = g.get(edge.trailing, [])
            trailing_neighbors.append(edge.leading)
            g[edge.leading] = leading_neighbors
            g[edge.trailing] = trailing_neighbors

        for edge in edges:
            if edge.leading not in self.links:
                self.links[edge.leading] = {}

            if edge.trailing not in self.links:
                self.links[edge.trailing] = {}

            self.links[edge.leading][edge.trailing] = edge.slip
            self.links[edge.trailing][edge.leading] = edge.slip

        for node_id in vertices:
            node = vertices[node_id]
            node_3d = np.array([node.x, node.y, node.z])
            self.node_vectors[node_id] = node_3d

        self.graph_data = g

    def dfs(self, lines, color):
        """! \brief Searches graph.

        Search the provided graph using depth first search, returns a bunch of lines.
        \param Takes in hashmap representing graph.
        \param Takes in a lookup for node_id to to node_vector.
        \param Takes in a set representing not_visited nodes
        \param Takes in an empty set representing nodes that have already been visited

        Returns: Lines, which is a bunch of lines we can plot
            """
        sns.set()
        num = 0
        color_lookup = {}
        for colors in sns.color_palette(self.color_scheme, 13):
            color_lookup.update({num: colors})
            num = num + 1
#         color_lookup = {0: "red", 1: "blue", 2: "green", 3: "purple", 4: "orange"}

        def search(current, previous, line, previous_slip, color, first_iteration):
            
            if len(self.visited) == 0:
                first_iteration = True
                
            neighbors = self.graph_data[current]

            here = self.node_vectors[current]

            branch = line
            branch.append(here)

            first_visit = current not in self.visited
            end_of_line = (len(neighbors) == 1 and neighbors[0] == previous)

            self.visited.add(current)
            if current in self.not_visited:
                self.not_visited.remove(current)

            if not first_visit or end_of_line:
                lines.append(branch)
                color.append(color_lookup[previous_slip])
                return

            for node in neighbors:
                slip = self.links[current][node]
                if slip != previous_slip:
                    if first_iteration:
                        lines.append(branch)
                        color.append(color_lookup[slip])
                        search(node, current, branch, slip, color, False)
                    branch = [here]

                if node != previous:
                    lines.append(branch)
                    color.append(color_lookup[slip])
                    search(node, current, branch, slip, color, False)
                    branch = [here]

        while len(self.not_visited) > 0:
            start_node = self.not_visited.pop()
            search(start_node, None, [], None, color, False)
        return lines, color
