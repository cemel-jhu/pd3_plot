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
    def __init__(self, protobuf, timestep, x_axis, y_axis):
        #set the instance variables
        self.protobuf = protobuf
        self.timestep = timestep
        self.x_axis = x_axis
        self.y_axis = y_axis

        self.not_visited = set()
        self.visited = set()
        self.node_vectors = {}
        self.node_vectors_projection = {}
        self.links = {}
        
    # This method creates the graph and stores the node and edge information
    def create_graph(self):
        """! \brief Creates a graph

        Exports a graph from protobuf, and gets the edge and node information
        \param Takes in a graph
        \param Takes in x_axis and y_axis for plotting
        \param Takes in a set which represents the nodes that have been visited
        \param Takes in 2 lookup for node_id to to node_vector.
        """

        graph = study.export_protobuf()
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

            node_x = self.x_axis.dot(node_3d)
            node_y = self.y_axis.dot(node_3d)
            self.node_vectors_projection[node_id] = (node_x, node_y)
            
        return g
# return g.create_graph()
    
