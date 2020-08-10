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
    def __init__(self, proto_graph, timestep, color_scheme, num_colors):

        self.proto_graph = proto_graph
        self.timestep = timestep
        self.not_visited = set()
        self.visited = set()
        self.links = {}
        self.graph_data = {}
        self.node_vectors = {}
        self.color_scheme = color_scheme
        self.num_colors = num_colors

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

    def dfs(self, lines=None, color=None):
        """! \brief Searches graph.

        Search the provided graph using depth first search, returns lines.
        \param Takes in an empty list representing the lines
        \param Takes in an empty list representing colors

        Returns: lines, bunch of lines we can plot
        Returns: colors, colors corresponding to the slip planes of the lines
        """

        if lines is None:
            lines = []

        if color is None:
            color = []

        color_lookup = {}
        for num, colors in enumerate(
                sns.color_palette(self.color_scheme, self.num_colors)):
            color_lookup.update({num: colors})

        def search(current, previous, line, previous_slip, first):

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
                color.append(color_lookup[previous_slip % self.num_colors])
                return

            taken_branch = None
            for node in neighbors:
                slip = self.links[current][node]
                # For our very first progression, we just want to choose any
                # branch to progress down. Or we continue a branch witht the
                # same slip.
                if first or (slip == previous_slip and node != previous):
                    search(node, current, branch, slip, False)
                    taken_branch = node
                    break

            for node in neighbors:
                slip = self.links[current][node]
                if node not in (previous, taken_branch):
                    branch = [here]
                    search(node, current, branch, slip, False)

            # If the line is not continued, then we need to record it.
            if taken_branch is None:
                lines.append(line)
                color.append(color_lookup[previous_slip % self.num_colors])

        while len(self.not_visited) > 0:
            start_node = self.not_visited.pop()
            search(start_node, None, [], None, True)

        return np.array(lines), color
