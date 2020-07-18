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


class Graph:
    # constructor
    def __init__(self, proto_graph, timestep, x_axis, y_axis, node_vectors):
        #set the instance variables
        self.proto_graph = proto_graph
        self.timestep = timestep
        self.x_axis = x_axis
        self.y_axis = y_axis

        self.not_visited = set()
        self.visited = set()
#         self.node_vectors = {}
        self.node_vectors_projection = {}
        self.links = {}
        self.graph_data = {}
        
        # This method creates the graph and stores the node and edge information
#         def _create_graph(self):
#             """! \brief Creates a graph

#             Exports a graph from protobuf, and gets the edge and node information
#             \param Takes in a graph
#             \param Takes in x_axis and y_axis for plotting
#             \param Takes in a set which represents the nodes that have been visited
#             \param Takes in 2 lookup for node_id to to node_vector.
#             """
#         def _create_graph(self):
        graph = self.proto_graph
        vertices = graph.state[self.timestep].nodes
        edges = graph.state[self.timestep].links
        g = {}
#         node_vectors = {}
        
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
            node_vectors[node_id] = node_3d
#             print(type(node_vectors))

            node_x = self.x_axis.dot(node_3d)
            node_y = self.y_axis.dot(node_3d)
            self.node_vectors_projection[node_id] = (node_x, node_y)
#         print(self.not_visited)
        self.graph_data = g
#         self.node_vectors = node_vectors
#         print(node_vectors)
                
    def dfs(self, node_vectors):
        """! \brief Searches graph.

        Search the provided graph using depth first search, returns a bunch of lines.
        \param Takes in hashmap representing graph.
        \param Takes in a lookup for node_id to to node_vector.
        \param Takes in a set representing not_visited nodes
        \param Takes in an empty set representing nodes that have already been visited

        Returns: Lines, which is a bunch of lines we can plot
            """
        lines = []
        color = []
        color_lookup = {0: "red", 1: "blue", 2: "green", 3: "purple", 4: "orange"}

        def search(node_vectors, current, previous, line, previous_slip, color):
#             print(current)
#             print("nV")
#             print()
#             print(node_vectors)
#             print()
            neighbors = self.graph_data[current]
#             print("neighbors")
#             print()
#             print(neighbors)
#             print()
            #error is saying that they can't find current in node_vectors, but when I print node_vectors, the current node id is there
            here = node_vectors[current]
#             print("here")
#             print(here)
#             print()
            branch = line
            branch.append(here)
#             print(type(branch))
#             print(":Branch")
#             print(branch)
#             print()

            first_visit = current not in self.visited
            end_of_line = (len(neighbors) == 1 and neighbors[0] == previous)

            self.visited.add(current)
            if current in self.not_visited:
                self.not_visited.remove(current)

            if not first_visit or end_of_line:
                lines.append(branch)
                color.append(color_lookup[previous_slip])
                return

            first_iteration = True
#             print(neighbors)
            for node in neighbors:
#                 print("NODE")
#                 print(node)
                slip = self.links[current][node]
                if slip != previous_slip:
                    if first_iteration:
                        lines.append(branch)
                        color.append(color_lookup[slip])
                    branch = [here]
#                 print("previos")
#                 print(previous)
                if node != previous:
                    search(node_vectors, node, current, branch, slip, color)
                    branch = [here]
                first_iteration = False
            
        while len(self.not_visited) > 0:
            start_node = self.not_visited.pop()
            search(node_vectors, start_node, None, [], None, color)
        
        return lines, color