import pd3
from pd3.proto.study_pb2 import IMMOBILE
import matplotlib.pyplot as plt
import ipyvolume as ipv
import numpy as np
import matplotlib.cm as cm
from matplotlib import collections as mc
import pylab as pl


def normalize(a, b, c):
    """Creates a unit vector from a, b, c"""
    vector = np.array([a, b, c])
    return vector / np.linalg.norm(vector)


def create_graph(study, timestep, x_axis, y_axis, not_visited, node_vectors, node_vectors_2d):
    """! \brief Creates a graph
    
    Exports a graph from protobuf, and gets the edge and node information
    \param Takes in a graph
    \param Takes in x_axis and y_axis for plotting
    \param Takes in a set which represents the nodes that have been visited
    \param Takes in 2 lookup for node_id to to node_vector.
    """
        
    graph = study.export_protobuf()
    vertices = graph.state[timestep].nodes
    edges = graph.state[timestep].links
    g = {}
   
    for edge in edges:
        not_visited.add(edge.leading)
        not_visited.add(edge.trailing)
        leading_neighbors = g.get(edge.leading, [])
        leading_neighbors.append(edge.trailing)
        trailing_neighbors = g.get(edge.trailing, [])
        trailing_neighbors.append(edge.leading)
        g[edge.leading] = leading_neighbors
        g[edge.trailing] = trailing_neighbors

    for node_id in vertices:
        node = vertices[node_id]
        node_3d = np.array([node.x, node.y, node.z])
        node_vectors[node_id] = node_3d
        
        node_x = x_axis.dot(node_3d)
        node_y = y_axis.dot(node_3d)
        node_vectors_2d[node_id] = (node_x, node_y)
        
    return g

def collect_data(lines):
    """! \brief Collects data for lines
    
    Goes through the lines array and collects the x, y, and z values needed to plot
    \param Takes in an array of node information (x, y, z)
    
    Returns: xs, ys, and zs which are points to plot on the graph
    """
    
    lines = np.array(lines)
    length = len(lines)
    fig = ipv.figure()
    for line in lines:
        x = []
        y = []
        z = []
        for array in line:
            x.append(array[0])
            y.append(array[1])
            z.append(array[2])
        xs += x
        ys += y
        zs += z
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        ipv.pylab.plot(x, y, z, color = 'blue')
    xs = np.array(xs)
    ys = np.array(ys)
    zs = np.array(zs)
    
    return xs, ys, zs, x, y, zs

def dfs(graph, node_vectors, not_visited, visited):
    """! \brief Searches graph.
    
    Search the provided graph using depth first search, returns a bunch of lines.
    \param Takes in hashmap representing graph.
    \param Takes in a lookup for node_id to to node_vector.
    \param Takes in a set representing not_visited nodes
    \param Takes in an empty set representing nodes that have already been visited
    
    Returns: Lines, which is a bunch of lines we can plot
    """
    lines = []
    
    def search(graph, node_vectors, current, previous, line):
        neighbors = graph[current]
        here = node_vectors[current]
        branch = line
        branch.append(here)

        first_visit = current not in visited
        end_of_line = (len(neighbors) == 1 and neighbors[0] == previous)

        visited.add(current)
        if current in not_visited:
            not_visited.remove(current)

        if not first_visit or end_of_line:
            lines.append(branch)
            return

        for node in neighbors:
            if node != previous:
                search(graph, node_vectors, node, here, branch)
                branch = [node_vectors[current]]
    while len(not_visited) > 0:
        start_node = not_visited.pop()
        search(graph, node_vectors, start_node, None, [])
        
    return lines           
                
def plot_study3D(study, timestep = 0, do_scatter=False):
    """! \brief Plots the dislocation system in 3D at the given timestep.

    Plots a given dislocation system with orthogonal axes.
    \param study Self instance.
    \param timestep The timestep to plot.
    \param do_scatter Whether to plot dislocation nodes or not.
    """

    not_visited = set()
    visited = set()
    node_vectors = {}
    node_vectors_2d = {}
    
    #create the graph
    g = create_graph(study, timestep, x_axis, y_axis, not_visited, node_vectors, node_vectors_2d)  
    
    #collect plotting informatoin
    lines = dfs(g, node_vectors_2d, not_visited, visited)
    
    xs = []
    ys = []
    zs = []    
    #organize plotting information and draw lines
    xs, ys, zs = collect_data(lines)
    
    #draw dots
    if do_scatter:
        scatter = ipv.scatter(xs, ys, zs)
    ipv.show()


def plot_study(study, timestep = 0, x_axis=(1, 0, 0), y_axis=(0, 1, 0)):
    """! \brief Plots the dislocation system at the given timestep.

    Plots a given dislocation system with orthogonal axes.
    \param study Self instance.
    \param x_axis The x axis to project the system on.
    \param y_axis The y axis to projec the system on.
    \param timestep The timestep to plot.
    """
    
    x_axis = np.array(x_axis)
    x_axis = x_axis / np.linalg.norm(x_axis)
    y_axis = np.array(y_axis)
    y_axis = y_axis / np.linalg.norm(y_axis)
    
    if x_axis.dot(y_axis) != 0:
        raise pd3.Pd3Exception("Provided axes are not normal.")

    not_visited = set()
    visited = set()
    node_vectors = {}
    node_vectors_2d = {}
    
    #creating the graph
    g = create_graph(study, timestep, x_axis, y_axis, not_visited, node_vectors, node_vectors_2d) 
    
    #collect the information to plot
    lines = dfs(g, node_vectors_2d, not_visited, visited)

    #Plots lines
    lc = mc.LineCollection(lines)
    fig, ax = pl.subplots()
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
    plt.title("Plot Study")
    plt.xlabel("x")
    plt.ylabel("y")
